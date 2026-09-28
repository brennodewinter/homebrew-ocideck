cask "ocideck" do
  version "0.6.13"
  sha256 "61627e9772ec9b235e526cead6214391957c15d1a6bf940a996f5b11361b5530"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.6.13/ocideck-macos-0.6.13.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
