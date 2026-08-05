# Homebrew tap voor OciDeck

De officiële [Homebrew](https://brew.sh/)-tap voor **OciDeck** — de macOS-cask.

```bash
brew tap brennodewinter/ocideck
brew install --cask ocideck
```

De cask is alleen een verwijzing: hij draagt de download-URL van de release en de
SHA-256 die rechtstreeks uit de gepubliceerde `SHA256SUMS` komt, zodat `brew` ons
eigen artefact ophaalt en verifieert. **macOS-only** — Homebrew Cask kent geen
Linux-equivalent; een Linux-installatieroute loopt langs een eigen spoor.

## Onderhoud

Deze repo is **canoniek op de eigen forge** (pawprint) en wordt naar GitHub
gespiegeld, zodat de `brennodewinter/ocideck`-shorthand werkt. `Casks/ocideck.rb` wordt
**automatisch bijgewerkt bij elke release** door de `homebrew-cask`-job in
`.forgejo/workflows/release.yml` van de OciDeck-repo. Werk dit bestand niet met de
hand bij, tenzij de automatische route uitvalt:

```bash
scripts/update_homebrew_cask.sh <tag> Casks/ocideck.rb
```

Zie `docs/BUILD.md` §"Homebrew cask" in de OciDeck-repo voor de volledige opzet.