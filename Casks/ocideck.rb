cask "ocideck" do
  version "0.6.8"
  sha256 "febe5d99c89998013fb6b9cf088c71a191b0b473ca79873a7b65724ebd5c1f05"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.6.8/ocideck-macos-0.6.8.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
