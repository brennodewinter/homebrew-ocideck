# Homebrew tap voor OciDeck

De officiële macOS-cask, canoniek op Pawprint en gespiegeld naar GitHub:

```sh
brew tap brennodewinter/ocideck
brew install --cask ocideck
```

De cask bevat uitsluitend de download-URL en de door minisign geauthenticeerde
SHA256 van het gepubliceerde macOS-archief. Linux en Windows hebben eigen
releasekanalen; hun publicatie verandert deze cask niet.

## Bijwerken en terugzetten

`update-cask.yml` draait elk half uur. De selector zoekt de hoogste stabiele,
niet verlaten, publieke release die daadwerkelijk een macOS-archief en complete
getekende metadata heeft: legacy `SHA256SUMS` of het afzonderlijke macOS-manifest
met kanaalchecksums. Een nieuwere Windows-only release wordt overgeslagen;
onvolledige macOS-metadata en ongeldige handtekeningen stoppen de update.

Voor een expliciete publicatie heeft de workflow deze inputs:

- `tag`: bestaande stabiele macOS-release, bijvoorbeeld `v0.7.6`.
- `operation_id`: unieke nonce van de aanroepende releasecontroller.
- `pin`: `false` voor normale publicatie, `true` voor expliciete rollback.

Een rollback met `pin=true` bewaart `channel-policy.json` in Git. De planning
respecteert dit doel ook als later een nieuwere macOS-release verschijnt.
De volgende expliciete normale publicatie met `pin=false` verwijdert die hold.
Tag of releasebestanden worden nooit overschreven. De aanroepende controller
controleert de huidige verwijzing en de getekende oudere doelversie vóór rollback.

Iedere run leest OciDeck-main eenmaal en haalt generator, sjabloon, controle en
verlaten-versiesbeleid uitsluitend bij die volledige commit-SHA op. De publieke
sleutel staat hier vast ingecheckt en moet bytegelijk zijn; code uit de gekozen
releasetag wordt niet uitgevoerd. Downloads zijn begrensd, uitsluitend HTTPS en
zonder redirects. Alleen cask en policy mogen veranderen; push mislukt wanneer
tap-main inmiddels is verplaatst. Een expliciete run bewaart het bewijsbestand
`homebrew-channel-<operation_id>/homebrew-channel.json` met de resulterende
Git-commit, caskhash, tag en pinstatus. Een groen uploadbewijs wordt door de
controller gevolgd door publieke URL/SHA256-controle.

## Controle

De gepinde Linux-workflow draait dezelfde lichte controles voor elke PR en
main-push; een push activeert uitsluitend validatie, geen pointerwijziging:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
ruby -c Casks/ocideck.rb
```

De tests omvatten echte minisign-handtekening/tampercontrole, Mac-selectie,
Windows-only releases, gedeeltelijke metadata, policy en het wissen van een pin.
De bestaande cask is met deze proceswijziging niet naar een andere versie gezet.
