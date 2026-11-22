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

## Current version: 3.5

- Private level-up reminders: recommended current/next area and milestone training.
- `/feralsetup guide`: current route, quest suggestions and training notes.
- `/feralsetup guide on` or `off`: toggle reminders for this character.
- Explicit macro, action-bar and keybinding installation with local recovery snapshots.

The guide is a flexible reference, not completed-quest tracking; it ends at 30.

## Keybinding setup

**Mac Command and Windows Alt alternatives are included.** Every Cmd binding
has an Alt alternative, including self-casting and deliberate form re-shifts.
See the [complete key map](FeralSetup/KEYBINDS.txt).

New in 3.5: numbered Cat builder/finisher and Bear single-target/AoE groups;
Cat Q selects Dash/Pounce, R selects Shred/Ravage; B toggles Prowl in Cat and
remains Challenging Roar in Bear. No combat macro automatically enters a form.
Faerie Fire is Cmd/Alt+R; set focus is Shift+Space. Frenzied Regeneration is
Cmd/Alt+J in Bear. Cmd/Alt+Shift+Space clears focus.

**Setup replaces same-name guide macros and configured bar slots/keybindings.**
Use it deliberately, out of combat:

1. In humanoid form, main action page 1: `/feralsetup setup`.
2. Enter each learned Cat/Bear form and run `/feralsetup form`.
3. Check your bars, then `/feralsetup save` to snapshot and reload.

**Upgrading to 3.5 requires the setup steps above** to install the new bindings
and refresh both form pages. Replacing files alone does not rewrite your bars.
Attack spells on native buttons still need manual rank updates after training.
The two stealth-selecting macros naturally cast their named spells by rank.

See [addon instructions](FeralSetup/README.txt) for all commands and recovery.
Saved preferences and snapshots live separately in WoW's `WTF` directory;
installing this addon on another PC does not transfer them.

## Validation

Offline Lua 5.1 tests use simulated WoW APIs, not a live game client:

```sh
python3 -m pip install lupa
python3 tests/test_leveling.py
python3 tests/test_bindings.py
```

See [validation notes](FeralSetup/OFFLINE_TESTS.txt).
