cask "ocideck" do
  version "0.6.11"
  sha256 "34b1f72a6e70825f7f8cc57bf90a4a9ea1afea225a4633821442ba5850b13ecd"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.6.11/ocideck-macos-0.6.11.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
