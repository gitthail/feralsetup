# FeralSetup

A personal WoW Forever Druid addon for explicit macro/keybinding setup, layout
snapshots and a lightweight Alliance levelling guide for levels 15–30.

## Download and install

**[Download FeralSetup.zip — ready to extract and move](https://github.com/gitthail/feralsetup/releases/latest/download/FeralSetup.zip)**

Extract the ZIP, then move the single extracted **FeralSetup** folder into AddOns.
No installer, extra nesting, renaming or build step is needed.
Use your WoW Forever installation's `Interface/AddOns` directory.
The resulting path must be `Interface/AddOns/FeralSetup/FeralSetup.toc`.
Restart WoW after installing new addon files.

The packaged addon runs directly; no build tools or Git installation are needed.
If downloading GitHub's source ZIP instead, copy only its inner `FeralSetup`
folder into `AddOns`.

## Current version: 3.5.5

- Private level-up reminders: recommended current/next area and milestone training.
- `/feralsetup guide`: current route, quest suggestions and training notes.
- `/feralsetup guide on` or `off`: toggle reminders for this character.
- Explicit macro, action-bar and keybinding installation with local recovery snapshots.

The guide is a flexible reference, not completed-quest tracking; it ends at 30.

## HTML guides

The install ZIP includes **Guide.html** (controls, modifiers, installation, all
commands and a searchable macro reference) and **Leveling.html** (the agreed
route and professions guide). Open them in your browser from the extracted
FeralSetup folder; they work offline.

- [Download the controls guide](https://github.com/gitthail/feralsetup/releases/latest/download/Guide.html)
- [Download the levelling guide](https://github.com/gitthail/feralsetup/releases/latest/download/Leveling.html)
- [Guide source](docs/Guide.html) · [Levelling source](docs/Leveling.html)

Use `/feralsetup guide` for current-area advice in-game, and
`/feralsetup guide on` or `off` to control level-up reminders.

## Keybinding setup

**Mac Command and Windows Alt alternatives are included.** Every Cmd binding
has an Alt alternative, including self-casting and deliberate form re-shifts.
See the [complete key map](FeralSetup/KEYBINDS.txt).

Current controls: numbered Cat direct/bleed and Bear single-target/AoE groups;
Cat Q selects Dash/Pounce, R selects Shred/Ravage; B toggles Prowl in Cat and
remains Challenging Roar in Bear. No combat macro automatically enters a form.
Faerie Fire is Shift+R; set focus is Shift+Space. Frenzied Regeneration is
Cmd/Alt+J in Bear. Cmd/Alt+Shift+Space clears focus.
Human Q is Roots and E is Hibernate, with Shift focus / Ctrl mouseover.
T Roots and X Hibernate remain available in every form.

**Setup replaces same-name guide macros and configured bar slots/keybindings.**
Use it deliberately, out of combat:

1. In humanoid form, main action page 1: `/feralsetup setup`.
2. Enter each learned Cat/Bear form and run `/feralsetup form`.
3. Check your bars, then `/feralsetup save` to snapshot and reload.

**Fresh installs and upgrades from before 3.5 require the setup steps above.**
From 3.5–3.5.4: replace files and `/reload`. Out of combat, in humanoid
form on main page 1, run `/feralsetup form`. Enter Cat and run it again.
This places human Q/E and swaps Cat 2/3. Then `/feralsetup save`.
Bear and fixed bars need no rebuild. If upgrading from before 3.5.4, also
run `/feralsetup update` and `/feralsetup bindings` for earlier fixes.
Attack spells on native buttons still need manual rank updates after training.
The two stealth-selecting macros naturally cast their named spells by rank.

See [addon instructions](FeralSetup/README.txt) for all commands and recovery.
Saved preferences and snapshots live separately in WoW's `WTF` directory;
installing this addon on another PC does not transfer them.

## Build the install package

```sh
python3 -m pip install lupa
python3 scripts/build_release.py
```

This regenerates `docs/Guide.html` from the addon and builds
`dist/FeralSetup.zip`. The archive contains exactly one top-level `FeralSetup`
folder, including both offline HTML guides. It does not install anything.
The HTML guide can also generate an offline ZIP of its bundled addon version.

## Validation

Offline Lua 5.1 tests use simulated WoW APIs, not a live game client:

```sh
python3 -m pip install lupa
python3 tests/test_leveling.py
python3 tests/test_bindings.py
node tests/test_guide.cjs
```

See [validation notes](FeralSetup/OFFLINE_TESTS.txt).
