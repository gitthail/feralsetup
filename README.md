# FeralSetup

A personal WoW Forever Druid addon for explicit macro/keybinding setup, layout
snapshots and a lightweight Alliance levelling guide for levels 15–30.

## Download and install

Download **FeralSetup.zip** from the [latest release](https://github.com/gitthail/feralsetup/releases/latest).
Extract it into your WoW Forever installation's `Interface/AddOns` directory.
The resulting path must be `Interface/AddOns/FeralSetup/FeralSetup.toc`.
Restart WoW after installing new addon files.

The packaged addon runs directly; no build tools or Git installation are needed.
If downloading GitHub's source ZIP instead, copy only its inner `FeralSetup`
folder into `AddOns`.

## Current version: 3.4

- Private level-up reminders: recommended current/next area and milestone training.
- `/feralsetup guide`: current route, quest suggestions and training notes.
- `/feralsetup guide on` or `off`: toggle reminders for this character.
- Explicit macro, action-bar and keybinding installation with local recovery snapshots.

The guide is a flexible reference, not completed-quest tracking; it ends at 30.

## Keybinding setup

The current preset is designed for **Mac Command modifiers**. A Windows preset
has not been implemented. The levelling guide does not depend on those bindings.

**Setup replaces same-name guide macros and configured bar slots/keybindings.**
Use it deliberately, out of combat:

1. In humanoid form, main action page 1: `/feralsetup setup`.
2. Enter each learned Cat/Bear form and run `/feralsetup form`.
3. Check your bars, then `/feralsetup save` to snapshot and reload.

Upgrading from 3.3 to 3.4 only requires replacing files and restarting WoW;
no setup or macro update is needed for the levelling guide.

See [addon instructions](FeralSetup/README.txt) for all commands and recovery.
Saved preferences and snapshots live separately in WoW's `WTF` directory;
installing this addon on another PC does not transfer them.

## Validation

Offline Lua 5.1 tests use simulated WoW APIs, not a live game client:

```sh
python3 -m pip install lupa
python3 tests/test_leveling.py
```

See [validation notes](FeralSetup/OFFLINE_TESTS.txt).
