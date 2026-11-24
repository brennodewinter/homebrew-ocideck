cask "ocideck" do
  version "0.7.16"
  sha256 "275104d84f5f034db3df197f27562c0f50fb8513776b247c106bfb3cdf7b63a9"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.16/ocideck-macos-0.7.16.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  depends_on arch: :arm64

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
