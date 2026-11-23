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

## Current version: 3.6.1

All commands accept **`/fs`**; `/feralsetup` remains supported.
**3.6.1 updates the levelling strategy guide and adds guide-only Mage/Rogue proposals. Controls are unchanged; existing 3.6.0 users only replace files and restart WoW.**

**3.6.0 switches to the v2 Q/E attack layout. Apply all three form pages using
the steps below, even when upgrading from 3.5.8.**

- Private level-up reminders: recommended current/next area and milestone training.
- `/fs guide`: current route, quest suggestions and training notes.
- `/fs guide on` or `off`: toggle reminders for this character.
- Explicit macro, action-bar and keybinding installation with local recovery snapshots.

The guide is a flexible reference, not completed-quest tracking; it ends at 30.

## HTML guides

The install ZIP includes **Guide.html** (controls, modifiers, installation, all
commands and a searchable macro reference) and **Leveling.html** (efficient levelling from 24 onward, route decisions, dungeon tradeoffs and professions). Open them in your browser from the extracted
FeralSetup folder; they work offline.

- [Download the controls guide](https://github.com/gitthail/feralsetup/releases/latest/download/Guide.html)
- [Download the levelling guide](https://github.com/gitthail/feralsetup/releases/latest/download/Leveling.html)
- [Guide source](docs/Guide.html) · [Levelling source](docs/Leveling.html)

Use `/fs guide` for current-area advice in-game, and
`/fs guide on` or `off` to control level-up reminders.

## Keybinding setup

**Mac Command and Windows Alt alternatives are included.** Every Cmd binding
has an Alt alternative, including self-casting and deliberate form re-shifts.
See the [complete key map](FeralSetup/KEYBINDS.txt).

| Key | Cat | Bear | Human |
| --- | --- | --- | --- |
| Q | Claw | Maul | Roots |
| E | Rake | Swipe | Moonfire |
| Shift+Q | Ferocious Bite | Primal Bite | Wrath |
| Shift+E | Rip | Lacerate | Starfire |
| R | Shred / stealthed Ravage | Demoralizing Roar | Soothe Animal |
| 1 | Dash / stealthed Pounce | Bash | Roots |
| 2 | Cat Charge | Bear Charge | Hibernate |
| 3 | Shifting Power | Enrage | Hurricane |
| 4 | Faerie Fire | Faerie Fire | Faerie Fire |

Shift+1/2 targets focus for the relevant controls; normal Cat Shift+1 is inactive.
T/X remain all-form Roots/Hibernate, with Shift-focus. Alt+Q remains Cat Dash,
including stealth. Alt+1 remains Barkskin. Z and Shift+R are freed.
Native mouseover handles normal spells; macro Cmd/Alt-self and selected
Shift-focus remain. Ctrl is available for user bindings. Shift+D toggles the
native damage meter enabled/disabled; its visibility follows the game settings.

**Install or upgrade to v2, out of combat:**

1. Replace addon files and restart WoW.
2. In humanoid form, main action page 1: `/fs setup`.
3. Enter Cat: `/fs form`.
4. Enter Bear: `/fs form`.
5. Check your bars, then `/fs save`.

Setup updates guide macros, fixed bars, bindings and targeting settings. Both
animal pages need applying for this layout change. Personal item slots are
preserved; unlearned spells leave empty slots. Native spell ranks remain manual.
Saved preferences and snapshots live separately in WoW's `WTF` directory.
See [addon instructions](FeralSetup/README.txt) for commands and recovery.

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
