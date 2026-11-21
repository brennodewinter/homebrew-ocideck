cask "ocideck" do
  version "0.7.15"
  sha256 "d99c6ca0f3797517cab4b0184660dc26c45be9b74fbd20b71e36a815f105231c"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.15/ocideck-macos-0.7.15.zip"
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
