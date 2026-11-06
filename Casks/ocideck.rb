cask "ocideck" do
  version "0.7.7"
  sha256 "bb79622f7103f2cf018f9051a78cafc000db25d36fdb3a8cc219e4a1372582f8"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.7/ocideck-macos-0.7.7.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
