import importlib.util
import json
from pathlib import Path
import tempfile
import shutil
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('channel', Path(__file__).with_name('update_channel.py'))
channel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(channel)


def release(tag, mode='macos'):
    names = ['ocideck-macos-' + tag[1:] + '.zip']
    names += ['SHA256SUMS', 'SHA256SUMS.minisig'] if mode == 'legacy' else [
        'SHA256SUMS.macos', 'SHA256SUMS.macos.minisig', 'channel-manifest-macos.json', 'channel-manifest-macos.json.minisig']
    return dict(tag_name=tag, draft=False, prerelease=False, assets=[{'name': name} for name in names])


class SelectionTest(unittest.TestCase):
    def test_windows_only_latest_does_not_hide_older_mac(self):
        windows = dict(tag_name='v0.7.8', draft=False, prerelease=False, assets=[{'name': 'ocideck-windows-x64-0.7.8.zip'}])
        self.assertEqual(channel.choose([windows, release('v0.7.6', 'legacy')], set()), ('v0.7.6', 'legacy'))

    def test_newest_mac_channel_wins(self):
        self.assertEqual(channel.choose([release('v0.7.6', 'legacy'), release('v0.7.7')], set()), ('v0.7.7', 'macos'))

    def test_abandoned_and_draft_never_selected(self):
        draft = release('v8.0.0')
        draft['draft'] = True
        self.assertEqual(channel.choose([draft, release('v1.2.1'), release('v0.7.6')], {'v1.2.1'}), ('v0.7.6', 'macos'))

    def test_pin_survives_scheduled_newer_release(self):
        values = [release('v0.7.6'), release('v0.7.7')]
        self.assertEqual(channel.choose(values, set(), pinned='v0.7.6')[0], 'v0.7.6')
        self.assertEqual(channel.choose(values, set(), explicit='v0.7.7', pinned='v0.7.6')[0], 'v0.7.7')

    def test_partial_or_duplicate_metadata_fails_closed(self):
        for mutate in (lambda value: value['assets'].pop(), lambda value: value['assets'].append(value['assets'][0])):
            value = release('v0.7.7')
            mutate(value)
            with self.assertRaises(ValueError):
                channel.choose([value, release('v0.7.6')], set())

    def test_explicit_windows_only_does_not_fall_back(self):
        value = release('v0.7.7')
        value['assets'] = []
        with self.assertRaisesRegex(ValueError, 'not macOS complete'):
            channel.choose([value, release('v0.7.6')], set(), explicit='v0.7.7')

    def test_invalid_tags_and_duplicate_policy_are_rejected(self):
        for tag in ('v01.2.3', 'v1.2.3-rc1', '1.2.3', 'v1.2.3/evil'):
            with self.assertRaises(ValueError):
                channel.version(tag)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'policy.json'
            path.write_text('{"schema":1,"pinned_tag":"v0.7.6","pinned_tag":"v0.7.7"}')
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                channel.read_policy(path)

    def test_policy_read_and_abandoned_source(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'policy.json'
            self.assertIsNone(channel.read_policy(path))
            path.write_text(json.dumps({'schema': 1, 'pinned_tag': 'v0.7.6'}))
            self.assertEqual(channel.read_policy(path), 'v0.7.6')
        self.assertEqual(channel.abandoned('local abandoned_tags=(\n v1.2.1 # reason\n )'), {'v1.2.1'})
        with self.assertRaises(ValueError):
            channel.abandoned('no policy')

    def test_changed_source_key_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(channel, 'data', return_value={'object': {'sha': 'a' * 40}}), patch.object(channel, 'fetch', return_value=b'changed'):
                with self.assertRaisesRegex(ValueError, 'key changed'):
                    channel.trusted_tools(root)

    def test_explicit_normal_publication_clears_pin_after_verified_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Casks').mkdir()
            policy = root / 'channel-policy.json'
            policy.write_text(json.dumps({'schema': 1, 'pinned_tag': 'v0.7.6'}))
            def generate(_directory, _tag, _mode, _release, output):
                output.write_text('verified cask')
                return 'a' * 64
            args = SimpleNamespace(tag='v0.7.7', operation_id='owned', pin=False, output=root / 'result.json')
            with patch.object(channel, 'ROOT', root), patch.object(channel, 'trusted_tools', return_value=('b' * 40, set())), patch.object(channel, 'data', return_value=release('v0.7.7')), patch.object(channel, 'verified_generate', side_effect=generate):
                channel.run(args)
            self.assertFalse(policy.exists())
            self.assertFalse(json.loads(args.output.read_text())['pinned'])

    @unittest.skipUnless(shutil.which('minisign'), 'minisign required for real signature fault test')
    def test_real_signature_rejects_tamper(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            public, secret, sums = root / 'public', root / 'secret', root / 'SHA256SUMS'
            subprocess.run(['minisign', '-G', '-W', '-p', str(public), '-s', str(secret)], check=True, capture_output=True)
            sums.write_text('checked archive digest')
            subprocess.run(['minisign', '-Sm', str(sums), '-s', str(secret)], check=True, capture_output=True)
            channel.verify_signature(sums, public)
            sums.write_text('tampered archive digest')
            with self.assertRaises(subprocess.CalledProcessError):
                channel.verify_signature(sums, public)

    def test_legacy_verifier_needs_no_new_channel_options(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'scripts').mkdir()
            (root / 'homebrew').mkdir()
            (root / 'homebrew/ocideck.rb.tmpl').write_text('unused')
            digest = 'a' * 64
            url = channel.RELEASES + 'v0.7.6/ocideck-macos-0.7.6.zip'
            generator = root / 'scripts/update_homebrew_cask.sh'
            generator.write_text('#!/bin/bash\nset -eu\ncat > "$2" <<EOF\n  version "0.7.6"\n  sha256 "' + digest + '"\n  url "' + url + '"\nEOF\n')
            (root / 'scripts/verify_homebrew_cask.sh').write_text('#!/bin/bash\ntest "$#" -eq 1 && test "$1" = v0.7.6\n')
            sums = (digest + '  ocideck-macos-0.7.6.zip\n').encode()
            with patch.object(channel, 'fetch', side_effect=lambda address: b'signature' if address.endswith('.minisig') else sums), patch.object(channel, 'verify_signature'):
                channel.verified_generate(root, 'v0.7.6', 'legacy', release('v0.7.6', 'legacy'), root / 'out.rb')
            with patch.object(channel, 'fetch', side_effect=lambda address: b'signature' if address.endswith('.minisig') else sums.replace(b'aaaa', b'bbbb', 1)), patch.object(channel, 'verify_signature'):
                with self.assertRaisesRegex(ValueError, 'identity differs'):
                    channel.verified_generate(root, 'v0.7.6', 'legacy', release('v0.7.6', 'legacy'), root / 'out.rb')

    def test_insecure_fetch_rejected_before_network(self):
        for url in ('http://example.org', 'https://user:secret@example.org'):
            with self.assertRaises(ValueError):
                channel.fetch(url)


if __name__ == '__main__':
    unittest.main()
