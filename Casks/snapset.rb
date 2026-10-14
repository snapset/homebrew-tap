cask "snapset" do
  version "1.6.1"
  sha256 "b69f209988aea1990cb08452a692dff9fbfff107bec9966704c264f582f2c9c2"

  url "https://snapset.co/download/Snapset-#{version}.dmg"
  name "Snapset"
  desc "Save and restore window layouts, apps and browser tabs"
  homepage "https://snapset.co/"

  livecheck do
    url "https://snapset.co/appcast.xml"
    strategy :sparkle, &:short_version
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "Snapset.app"
  binary "#{appdir}/Snapset.app/Contents/MacOS/Snapset", target: "snapset"

  uninstall quit: "com.snapset.Snapset"

  # The license copy in the login keychain ("com.snapset.Snapset.license") is not
  # removed by zap; delete it in Keychain Access if needed.
  zap trash: [
    "~/Library/Application Support/Snapset",
    "~/Library/Caches/com.snapset.Snapset",
    "~/Library/HTTPStorages/com.snapset.Snapset",
    "~/Library/HTTPStorages/com.snapset.Snapset.binarycookies",
    "~/Library/Preferences/com.snapset.Snapset.plist",
  ]
end
