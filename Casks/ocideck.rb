cask "ocideck" do
  version "0.7.10"
  sha256 "fd88df46a764c36285d6f49bcffc686b6f07ae8401f689106b7ae6de6d225637"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.10/ocideck-macos-0.7.10.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
