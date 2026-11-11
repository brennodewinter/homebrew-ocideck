cask "ocideck" do
  version "0.7.8"
  sha256 "37e9743a6196c68ad4e0ebc0a27c8af92c31fe47730f5e5f28806b741d4b5c4a"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.8/ocideck-macos-0.7.8.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
