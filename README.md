# Snapset for Homebrew

[Snapset](https://snapset.co/) saves your window layouts — apps, window positions,
desktops and browser tabs — and puts them back with one shortcut.

```sh
brew install --cask snapset/tap/snapset
```

Requires macOS 14 Sonoma or later on Apple silicon. Snapset starts with a 14-day free
trial; see [snapset.co](https://snapset.co/) for plans.

Snapset updates itself, so `brew upgrade` leaves it alone unless you pass `--greedy`.

The cask also links the `snapset` command, for scripts and launchers:

```sh
snapset list --json      # saved layouts
snapset apply "Work"     # apply a layout
snapset save "Work"      # save the current arrangement as a new layout
```

To remove it, along with its saved layouts and settings:

```sh
brew uninstall --cask --zap snapset
```

## How this tap stays current

A daily job reads Snapset's update feed, downloads the new release, checks that it is
signed by Snapset (Team ID `Z6VHB3M4TY`) and notarized by Apple, installs and
uninstalls it, and only then updates the cask.
