# FeralSetup — Numbers version

Personal WoW Forever Druid controls, recovery snapshots and levelling advice.

**[Download FeralSetup.zip](https://github.com/gitthail/feralsetup/releases/latest/download/FeralSetup.zip)** — extract and move the single **FeralSetup** folder into `Interface/AddOns`. No build step, renaming or extra nesting. Use the release asset, not GitHub's automatic source archive.

## Version 3.9.1

This repository and release contain the fixed **Numbers** version: attacks on 1–4, controls on Q/E. Runtime A/B switching and saved layout selection have been removed. The separate Q/E package is kept locally and is not included in this release.

| Key | Cat | Bear | Human |
| --- | --- | --- | --- |
| 1 | Claw | Maul | Moonfire |
| 2 | Ferocious Bite | Primal Bite | Wrath |
| 3 | Rake | Swipe | Starfire |
| 4 | Rip | Lacerate | Hurricane |
| Q | Dash / stealthed Pounce | Bash | Roots |
| E | Cat Charge | Bear Charge | Hibernate |

The first four physical bar buttons match 1–4 directly. Human Roots is on Q, with T retained as the shared shortcut; keyboard 7 remains Moonfire across forms. Shift+Q/E target focus for eligible controls. R remains the rear attack in Cat, Roar in Bear and Soothe Animal in human. T/X remain Roots/Hibernate in every form.

- **Shift+W or Z:** hover/target Faerie Fire; **Shift+Z:** focus.
- **Alt/Cmd+D:** Barkskin; **+S:** Bear Frenzied Regeneration; **+E:** Nature's Grasp.
- **Alt/Cmd+R:** Cat Shifting Power / Bear Enrage / human self-Innervate, visible on main bar button 9. Shift+W has its own visible Faerie Fire macro on right-bar button 12. Both recover through normal bar snapshots.
- **F/G/5 heals:** living friendly hover or selected target; self fallback only in human. Alt/Cmd deliberately forces self. Cures/buffs retain their previous self fallback.

Only H forcibly cancels form. Client-side failed-cast form retention is not guaranteed. R uses Shred until Ravage is learned; the Cat control key uses Dash until Pounce is learned. Run `/fs update` after training to refresh these choices. See the [complete key map](FeralSetup/KEYBINDS.txt).

## Install or upgrade — including from 3.9.0

Replace the addon files, restart WoW, then out of combat:

1. Human form, main action page 1: `/fs setup`.
2. Enter Cat: `/fs form`.
3. Enter Bear: `/fs form`.
4. Check all pages, then `/fs save`.

**Rebuild all three pages once:** the human attack row and visible resource/Faerie Fire positions have changed. `/fs targeting` or `/fs bindings` alone cannot migrate the old arrangement. Copying files does not update existing bars or macros. Old `/fs a`, `/fs b` and setup/bindings layout arguments now explain that switching was removed and make no changes.

Personal item slots are preserved. Unlearned native spell slots are empty; native spell-rank upgrades remain manual. The same package supports Windows and Mac: Windows installs Alt bindings; Mac installs those plus Command equivalents. Native Mac binding names/order are used, and stale Command conflicts are removed. Snapshots and preferences live separately in WoW's WTF folder.

## Guides and recovery

Both offline HTML guides are inside the ZIP and separately downloadable:

- [Guide.html](https://github.com/gitthail/feralsetup/releases/latest/download/Guide.html): the installed Numbers layout, targeting, commands and searchable macros; Mage/Rogue proposals only.
- [Leveling.html](https://github.com/gitthail/feralsetup/releases/latest/download/Leveling.html): efficient sessions from level 24 onward, dungeon/route decisions and professions.
- `/fs guide` displays the Alliance 15–30 checkpoints; `/fs guide on|off` toggles reminders.
- `/fs bindings` reapplies this package's single key map without changing bars.
- `/fs items` reports actual preserved item-slot contents. Empty slots, wrong action types and custom macros/unrecognised mount actions are flagged. Check the displayed item name matches the intended consumable; nothing is auto-filled or silently replaced.
- `/fs restore` restores the saved snapshot; `/fs undo` restores pre-setup state. Follow with `/reload`.
- `/fs status` displays the package edition and targeting settings.

## Build and validation

```sh
python3 -m pip install lupa
python3 tests/test_bindings.py
python3 tests/test_setup.py FeralSetup mac
python3 tests/test_setup.py FeralSetup windows
python3 tests/test_leveling.py
python3 scripts/build_release.py
node tests/test_guide.cjs
```

The build generates `docs/Guide.html` and `dist/FeralSetup.zip`. The guide can also generate an offline ZIP. Tests reject invalid Mac key names and model the client’s exclusion of direct macros from binding enumeration. Both platforms are tested. Live key delivery and casting are not verified. See [validation notes](FeralSetup/OFFLINE_TESTS.txt).

An independent local addon folder can be checked with `python3 tests/test_setup.py /absolute/path/FeralSetup`. The packaging script accepts `--addon-dir`, `--guide-output` and `--zip-output` paths; these do not add runtime switching to the addon.
