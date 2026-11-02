cask "ocideck" do
  version "0.7.6"
  sha256 "15c0592ceb1a5ab0274fefda19f19022f8a3a3f67857eb288f949a8d69074c97"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.7.6/ocideck-macos-0.7.6.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
