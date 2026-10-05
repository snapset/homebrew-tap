#!/usr/bin/env python3
"""Point Casks/snapset.rb at the newest release in Snapset's appcast.

Picks the newest item the way Homebrew's Sparkle livecheck does (latest pubDate),
downloads its DMG and rewrites `version` and `sha256`. The appcast's `?v=` stamp is
the first 10 hex digits of the DMG's SHA-256, so a mismatch stops the bump: the
file on the server is not the one the appcast announced.

Writes `changed=true|false` and `version=...` to $GITHUB_OUTPUT.
"""
import email.utils
import hashlib
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

APPCAST = "https://snapset.co/appcast.xml"
CASK = "Casks/snapset.rb"
SPARKLE = "{http://www.andymatuschak.org/xml-namespaces/sparkle}"
# snapset.co turns away Python's default user agent (403).
HEADERS = {"User-Agent": "snapset-homebrew-tap"}


def fetch(url, timeout):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=timeout) as r:
        return r.read()


def output(**values):
    path = os.environ.get("GITHUB_OUTPUT")
    lines = "".join(f"{k}={v}\n" for k, v in values.items())
    if path:
        with open(path, "a") as f:
            f.write(lines)
    print(lines, end="")


def newest_item():
    root = ET.fromstring(fetch(APPCAST, 30))
    items = []
    for item in root.iter("item"):
        date = email.utils.parsedate_to_datetime(item.findtext("pubDate"))
        version = item.findtext(f"{SPARKLE}shortVersionString")
        # The full download is the enclosure without sparkle:deltaFrom.
        full = [e for e in item.iter("enclosure") if e.get(f"{SPARKLE}deltaFrom") is None]
        if version and full:
            items.append((date, version, full[0].get("url")))
    if not items:
        sys.exit("no release found in the appcast")
    return max(items)


def main():
    _, version, url = newest_item()
    base, _, query = url.partition("?")
    stamp = dict(p.split("=", 1) for p in query.split("&") if "=" in p).get("v", "")
    expected = f"https://snapset.co/download/Snapset-{version}.dmg"
    if base != expected:
        sys.exit(f"the appcast's DMG is {base}, the cask expects {expected}")

    cask = open(CASK).read()
    current_version = re.search(r'^  version "([^"]+)"', cask, re.M).group(1)
    current_sha = re.search(r'^  sha256 "([0-9a-f]{64})"', cask, re.M).group(1)
    if current_version == version and current_sha.startswith(stamp):
        output(changed="false", version=version)
        return

    sha = hashlib.sha256(fetch(base, 120)).hexdigest()
    if stamp and not sha.startswith(stamp):
        sys.exit(f"downloaded {base} hashes to {sha}, the appcast says it starts with {stamp}")

    cask = re.sub(r'^  version "[^"]+"', f'  version "{version}"', cask, count=1, flags=re.M)
    cask = re.sub(r'^  sha256 "[0-9a-f]{64}"', f'  sha256 "{sha}"', cask, count=1, flags=re.M)
    open(CASK, "w").write(cask)
    output(changed="true", version=version)


if __name__ == "__main__":
    main()
