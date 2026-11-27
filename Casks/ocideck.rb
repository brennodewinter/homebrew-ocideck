cask "ocideck" do
  version "0.7.19"
  sha256 "f672b4f1e58d0a8caee66240202a2ff86ba3d6e6db1053a7d8455055cb533f6e"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.19/ocideck-macos-0.7.19.zip"
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
