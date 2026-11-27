# FeralSetup

Personal WoW Forever Druid controls, recovery snapshots and levelling advice.

**[Download FeralSetup.zip](https://github.com/gitthail/feralsetup/releases/latest/download/FeralSetup.zip)** — extract and move the single **FeralSetup** folder into `Interface/AddOns`. No build step, renaming or extra nesting. Restart WoW. Use the release asset, not GitHub's automatic source archive.

## Version 3.7.0

Explicit mouseover replaces the native-mouseover trial. Heals, cures, buffs, CC, Faerie Fire and Moonfire select appropriate mouseover units through macros. Self/focus modifiers remain explicit. Spell macros no longer force-cancel form before casting; only H does. Setup enables the client's `autoUnshift`, but client-side failed-cast form retention is not guaranteed by the addon.

R falls back to Shred until Ravage is learned. The Cat control button stays Dash until Pounce is learned; Dash must itself be learned. Run `/fs update` after training to refresh these choices.

## Upgrade from 3.6.x

Replace files, restart WoW, then out of combat:

```text
/fs targeting
```

Test hover healing, Roots and Moonfire, then `/fs save`. The existing form-page slots stay unchanged.

## Switch layouts immediately

```text
/fs a
/fs b
```

A uses numbers; B uses Q/E. These commands change **bindings only**, in any form while out of combat. No per-form setup or reload is needed to switch. Character bindings are saved; `/fs save` also captures a recovery snapshot and flushes addon data to disk.

| Action | A | B |
| --- | --- | --- |
| Claw / Maul / human Roots | 1 | Q |
| Bite / Primal Bite / Wrath | 2 | Shift+Q |
| Rake / Swipe / Moonfire | 3 | E |
| Rip / Lacerate / Starfire | 4 | Shift+E |
| Dash/Pounce / Bash / Roots | Q | 1 |
| Charge / human Hibernate | E | 2 |
| Shifting Power / Enrage / Hurricane | Shift+3 | 3 or Shift+3 |
| Faerie Fire, all forms | Z | Z or 4 |
| Focus Faerie Fire | Shift+Z | Shift+Z |

Shift modifies the control keys for focus. R is rear attack in Cat, Roar in Bear, Soothe Animal in human. T/X remain Roots/Hibernate in every form. See the [complete key map](FeralSetup/KEYBINDS.txt).

## First installation or upgrading from before 3.6.0

1. Humanoid, main action page 1, out of combat: `/fs setup b` (or `a`).
2. Enter Cat: `/fs form`.
3. Enter Bear: `/fs form`.
4. Check all pages, then `/fs save`.

This initial placement is required once; subsequent A/B switches share those slots. Personal item slots are preserved. Unlearned native spell slots are empty; native spell-rank upgrades remain manual. Every Cmd shortcut has an Alt alternative for Windows. Snapshots/preferences are in WoW's WTF folder and do not transfer with the addon ZIP.

## Guides and recovery

Both offline HTML guides are inside the ZIP, and separately downloadable:

- [Guide.html](https://github.com/gitthail/feralsetup/releases/latest/download/Guide.html): both layouts, targeting, commands, searchable macros; Mage/Rogue proposals only.
- [Leveling.html](https://github.com/gitthail/feralsetup/releases/latest/download/Leveling.html): efficient sessions from level 24 onward, dungeon/route decisions and professions.
- `/fs guide` displays the existing Alliance 15–30 checkpoints. `/fs guide on|off` toggles reminders.
- `/fs restore` restores the saved snapshot; `/fs undo` restores pre-setup state. Follow with `/reload`.
- `/fs status` displays layout and targeting settings. `/fs targeting` reports settings it cannot verify instead of claiming success.

## Build and validation

```sh
python3 -m pip install lupa
python3 tests/test_bindings.py
python3 tests/test_profiles.py
python3 tests/test_leveling.py
python3 scripts/build_release.py
node tests/test_guide.cjs
```

The build generates `docs/Guide.html` and `dist/FeralSetup.zip`. The HTML guide can also generate an offline ZIP. Tests use simulated WoW APIs and macro conditions, not live spell timing, range or line-of-sight checks. See [validation notes](FeralSetup/OFFLINE_TESTS.txt).
