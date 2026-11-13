cask "ocideck" do
  version "0.7.9"
  sha256 "6dfb02ce195e86385614e0555b6f660490a9bd98bcb2855ddfc6ef63af6350f1"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.9/ocideck-macos-0.7.9.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
