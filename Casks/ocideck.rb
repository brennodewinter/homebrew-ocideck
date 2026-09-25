cask "ocideck" do
  version "0.6.12"
  sha256 "7229998138adddec8a54f5cce74238fcb68d8721e02c094beebb6f6bb0b73f48"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.6.12/ocideck-macos-0.6.12.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
