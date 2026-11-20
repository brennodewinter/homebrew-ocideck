cask "ocideck" do
  version "0.7.14"
  sha256 "20c5259a2b5efce11d3768d5fd45c354ace7af2fd8e52a2902ecc7b524de4fd1"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.14/ocideck-macos-0.7.14.zip"
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
