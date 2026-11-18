cask "ocideck" do
  version "0.7.11"
  sha256 "9c1f6dc8ffe28e09eff495b206da76deddca6a880f1e32004061c427d4f8122d"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.11/ocideck-macos-0.7.11.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
