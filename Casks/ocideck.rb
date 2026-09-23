cask "ocideck" do
  version "0.6.10"
  sha256 "9890aef5087c0c6219c060e950fafd5a96839e6681a6738a5b1a977d1ad2f1a5"

  url "https://pawprint.vigilis.online/LibreKAT/Ocideck/releases/download/v0.6.10/ocideck-macos-0.6.10.zip"
  name "OciDeck"
  desc "Open-source presentation app for decks, notes, and collaborative sessions"
  homepage "https://ocideck.librekat.nl"

  app "OciDeck.app"

  # Zonder deze regel vervangt `brew upgrade` de bundel terwijl de app
  # draait. Dat levert half vervangen frameworks op en een app die pas bij
  # de volgende start met een dyld-fout stukloopt.
  uninstall quit: "com.dewinter.ocideck"
end
