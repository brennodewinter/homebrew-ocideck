cask "ocideck" do
  version "0.7.0"
  sha256 "2551f18f35da4a97e25fa128afc0a8b9cdc98143862254c34ddb6eece1415e55"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.0/ocideck-macos-0.7.0.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
