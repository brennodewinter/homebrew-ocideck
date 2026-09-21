cask "ocideck" do
  version "0.6.7"
  sha256 "7e6cc93ef587b1298efc43b730772c2899bd17636435287677310a7d6c934241"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.6.7/ocideck-macos-0.6.7.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
