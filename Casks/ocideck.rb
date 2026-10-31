cask "ocideck" do
  version "0.7.5"
  sha256 "6b2ba4c24254567956f534765a31d91654e50cc9bbbddfca022b4f544f1bd37c"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.5/ocideck-macos-0.7.5.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
