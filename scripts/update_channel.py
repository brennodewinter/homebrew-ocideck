#!/usr/bin/env python3
"""Select authenticated macOS releases and keep an explicit rollback pin."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, build_opener

API = 'https://pawprint.vigilis.online/api/v1/repos/LibreKAT/Ocideck'
RELEASES = 'https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/'
ROOT = Path(__file__).resolve().parents[1]


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON field')
        result[key] = value
    return result


def version(tag):
    if not isinstance(tag, str) or not re.fullmatch(r'v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)', tag):
        raise ValueError('canonical stable release tag required')
    return tuple(map(int, tag[1:].split('.')))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *_args, **_kwargs):
        raise ValueError('redirect refused')


def fetch(url, limit=2 * 1024 * 1024):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.username or parsed.password or parsed.fragment:
        raise ValueError('credential-free HTTPS required')
    with build_opener(NoRedirect).open(url, timeout=30) as response:
        if response.status != 200:
            raise ValueError('public source must return HTTP 200')
        content = response.read(limit + 1)
    if len(content) > limit:
        raise ValueError('public source exceeds size bound')
    return content


def data(url):
    return json.loads(fetch(url), object_pairs_hook=unique)


def abandoned(text):
    match = re.search(r'local abandoned_tags=\((.*?)\n\s*\)', text, re.S)
    if not match:
        raise ValueError('trusted abandoned release policy missing')
    tags = []
    for line in match[1].splitlines():
        item = line.split('#', 1)[0].strip()
        if item:
            version(item)
            tags.append(item)
    return set(tags)


def read_policy(path):
    if path.is_symlink():
        raise ValueError('policy must not be a symlink')
    if not path.exists():
        return None
    policy = json.loads(path.read_text(), object_pairs_hook=unique)
    if not isinstance(policy, dict) or set(policy) != {'schema', 'pinned_tag'} or type(policy['schema']) is not int or policy['schema'] != 1:
        raise ValueError('invalid channel policy')
    version(policy['pinned_tag'])
    return policy['pinned_tag']


def candidate(release, exclusions):
    if not isinstance(release, dict) or release.get('draft') is not False or release.get('prerelease') is not False:
        return None
    tag = release.get('tag_name')
    try:
        version(tag)
    except ValueError:
        return None
    if tag in exclusions:
        return None
    assets = release.get('assets')
    if not isinstance(assets, list) or not all(isinstance(item, dict) for item in assets):
        raise ValueError('invalid release assets')
    names = [item.get('name') for item in assets]
    if not all(isinstance(name, str) for name in names) or len(names) != len(set(names)):
        raise ValueError('duplicate or invalid release asset names')
    required = {'ocideck-macos-' + tag[1:] + '.zip'}
    channel = {'channel-manifest-macos.json', 'channel-manifest-macos.json.minisig', 'SHA256SUMS.macos', 'SHA256SUMS.macos.minisig'}
    if names and required <= set(names):
        if channel <= set(names):
            return tag, 'macos'
        if channel & set(names):
            raise ValueError('partial macOS channel metadata')
        if {'SHA256SUMS', 'SHA256SUMS.minisig'} <= set(names):
            return tag, 'legacy'
    return None


def choose(releases, exclusions, explicit='', pinned=None):
    requested = explicit or pinned
    if requested:
        version(requested)
        matches = [release for release in releases if release.get('tag_name') == requested]
        if len(matches) != 1:
            raise ValueError('requested macOS release unavailable or ambiguous')
        selected = candidate(matches[0], exclusions)
        if selected is None:
            raise ValueError('requested release is not macOS complete')
        return selected
    selected = [value for release in releases if (value := candidate(release, exclusions))]
    if not selected:
        raise ValueError('no stable macOS-complete public release')
    return max(selected, key=lambda value: version(value[0]))


def trusted_tools(directory):
    response = data(API + '/git/refs/heads/main')
    refs = response if isinstance(response, list) else [response]
    if len(refs) != 1 or not isinstance(refs[0], dict) or refs[0].get('ref') != 'refs/heads/main':
        raise ValueError('trusted source exact main ref unavailable or ambiguous')
    source = refs[0].get('object', {}).get('sha', '')
    if not re.fullmatch('[0-9a-f]{40}', source) or source == '0' * 40:
        raise ValueError('trusted source main SHA unavailable')
    for name in ('scripts/update_homebrew_cask.sh', 'scripts/verify_homebrew_cask.sh',
                 'scripts/release.sh', 'homebrew/ocideck.rb.tmpl', 'minisign.pub'):
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(fetch(API + '/raw/' + name + '?ref=' + source))
    if (directory / 'minisign.pub').read_bytes() != (ROOT / 'minisign.pub').read_bytes():
        raise ValueError('trusted source signing key changed; review tap key explicitly')
    return source, abandoned((directory / 'scripts/release.sh').read_text())


def verify_signature(path, public_key):
    subprocess.run(['minisign', '-Vm', str(path), '-x', str(path) + '.minisig',
                    '-p', str(public_key), '-q'], check=True, capture_output=True, timeout=30)


def verified_generate(directory, tag, mode, release, output):
    names = ['SHA256SUMS', 'SHA256SUMS.minisig'] if mode == 'legacy' else [
        'SHA256SUMS.macos', 'SHA256SUMS.macos.minisig',
        'channel-manifest-macos.json', 'channel-manifest-macos.json.minisig']
    for name in names:
        (directory / name).write_bytes(fetch(RELEASES + tag + '/' + name))
    sums = directory / names[0]
    verify_signature(sums, directory / 'minisign.pub')
    if mode == 'macos':
        verify_signature(directory / 'channel-manifest-macos.json', directory / 'minisign.pub')
    env = dict(os.environ, SHA256SUMS_FILE=str(sums), SHA256SUMS_SIGNATURE_FILE=str(directory / names[1]),
               TEMPLATE_FILE=str(directory / 'homebrew/ocideck.rb.tmpl'))
    command = ['bash', str(directory / 'scripts/update_homebrew_cask.sh'), tag, str(output)]
    if mode == 'macos':
        env['CHANNEL_MANIFEST_FILE'] = str(directory / 'channel-manifest-macos.json')
        command += ['--channel', 'macos']
    subprocess.run(command, env=env, check=True, timeout=120)
    # The generator authenticates the signed list. Bind its unique cask hash to
    # the actual public release metadata too, rather than accepting a stale row.
    cask = output.read_text()
    hashes = re.findall(r'^\s*sha256 "([0-9a-f]{64})"$', cask, re.M)
    urls = re.findall(r'^\s*url "([^"\n]+)"$', cask, re.M)
    expected_url = RELEASES + tag + '/ocideck-macos-' + tag[1:] + '.zip'
    asset = 'ocideck-macos-' + tag[1:] + '.zip'
    expected_hashes = []
    for line in sums.read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].removeprefix('./') == asset:
            expected_hashes.append(parts[0].lower())
    if len(hashes) != 1 or hashes != expected_hashes or urls != [expected_url]:
        raise ValueError('generated cask identity differs')
    subprocess.run(['bash', str(directory / 'scripts/verify_homebrew_cask.sh'), tag],
                   env=dict(env, CASK_FILE=str(output)), check=True, timeout=120)
    return hashlib.sha256(output.read_bytes()).hexdigest()


def run(args):
    explicit = args.tag or ''
    if explicit:
        version(explicit)
        if not re.fullmatch('[A-Za-z0-9_-]{1,80}', args.operation_id):
            raise ValueError('explicit update requires durable operation ID')
    elif args.operation_id or args.pin:
        raise ValueError('operation ID and pin require an explicit tag')
    policy = ROOT / 'channel-policy.json'
    pinned = read_policy(policy)
    with tempfile.TemporaryDirectory(prefix='tap-channel-') as temporary:
        directory = Path(temporary)
        source, exclusions = trusted_tools(directory)
        releases = []
        if explicit or pinned:
            releases = [data(API + '/releases/tags/' + quote(explicit or pinned, safe=''))]
        else:
            for page in range(1, 21):
                values = data(API + f'/releases?limit=100&page={page}')
                if not isinstance(values, list):
                    raise ValueError('invalid release listing')
                releases.extend(values)
                if len(values) < 100:
                    break
            else:
                raise ValueError('release listing exceeds inspection bound')
        tag, mode = choose(releases, exclusions, explicit, pinned)
        release = next(value for value in releases if value['tag_name'] == tag)
        pending = directory / 'ocideck.rb'
        digest = verified_generate(directory, tag, mode, release, pending)
        (ROOT / 'Casks/ocideck.rb').write_bytes(pending.read_bytes())
        if explicit:
            if args.pin:
                policy.write_text(json.dumps({'schema': 1, 'pinned_tag': tag}, sort_keys=True) + '\n')
            else:
                policy.unlink(missing_ok=True)
        args.output.write_text(json.dumps({'tag': tag, 'operation_id': args.operation_id,
            'source_controller': source, 'cask_sha256': digest, 'pinned': bool(args.pin if explicit else pinned)}, sort_keys=True) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag', default='')
    parser.add_argument('--operation-id', default='')
    parser.add_argument('--pin', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        run(args)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
