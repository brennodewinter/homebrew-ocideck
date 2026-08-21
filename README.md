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
gespiegeld, zodat de `brennodewinter/ocideck`-shorthand werkt.

`Casks/ocideck.rb` wordt **door deze repo zelf bijgewerkt**, niet door de
releaseketen van OciDeck. `.forgejo/workflows/update-cask.yml` draait elk half
uur, leest de nieuwste stabiele release publiek uit, haalt
`scripts/update_homebrew_cask.sh` en `homebrew/ocideck.rb.tmpl` op bij díe tag,
genereert de cask en pusht — met het token dat Forgejo per run voor deze
repository aanmaakt. Staat de cask al goed, dan committeert hij niets.

Daardoor is er **geen enkel geheim** in het spel. Tot v0.4.8 duwde de OciDeck-repo
de cask hierheen met een persoonlijk toegangstoken; dat token werd na een
Forgejo-upgrade geweigerd en de tap stond drie releases achter voordat iemand het
merkte. De keerzijde van de huidige opzet is dat de cask maximaal een half uur
achterloopt op een release — voor een tap betekenisloos, want `brew update` draait
op de klok van de gebruiker.

Werk `Casks/ocideck.rb` niet met de hand bij. Moet het toch — de werkstroom ligt
stil, of je wilt niet op de volgende ronde wachten — draai hem dan met de hand af
(*Actions → Cask bijhouden → Run workflow*), of genereer met hetzelfde script:

```bash
scripts/update_homebrew_cask.sh <tag> Casks/ocideck.rb
```

Zie `docs/BUILD.md` §"Homebrew cask" in de OciDeck-repo voor de volledige opzet,
en `docs/CHECKS.md` voor de dagelijkse controle die nakijkt of deze tap en zijn
spiegel werkelijk op de laatste release staan.