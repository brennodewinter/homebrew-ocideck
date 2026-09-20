cask "ocideck" do
  version "0.6.6"
  sha256 "086d912423077ed64da823317acea9d1013a4b41803663518a05780f47f6eac3"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.6.6/ocideck-macos-0.6.6.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
