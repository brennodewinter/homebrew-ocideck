cask "ocideck" do
  version "0.6.9"
  sha256 "20c6748ba8dcfd2200ec38eb5ca4db6480991fb442cf29b306e585a9911e4b43"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.6.9/ocideck-macos-0.6.9.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
