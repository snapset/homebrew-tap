#!/bin/bash
# The app Homebrew installed is the one Snapset signed and Apple notarized.
set -euo pipefail
APP=/Applications/Snapset.app
codesign --verify --deep --strict "$APP"
codesign -dv "$APP" 2>&1 | grep -q '^TeamIdentifier=Z6VHB3M4TY$'
spctl --assess --type execute "$APP"
xcrun stapler validate "$APP"
echo "signed by Z6VHB3M4TY, accepted by Gatekeeper, ticket stapled"
