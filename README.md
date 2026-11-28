# FeralSetup

Personal WoW Forever Druid controls, recovery snapshots and levelling advice.

**[Download FeralSetup.zip](https://github.com/gitthail/feralsetup/releases/latest/download/FeralSetup.zip)** — extract and move the single **FeralSetup** folder into `Interface/AddOns`. No build step, renaming or extra nesting. Restart WoW. Use the release asset, not GitHub's automatic source archive.

## Version 3.8.0

B now uses Q → E for direct build/finish and Shift+Q → Shift+E for bleed build/finish. A retains 1 → 2 direct and 3 → 4 bleed, with Q/E controls. Both have Shift+W and Z for Faerie Fire; Shift+Z remains focus.

Alt/Cmd is the personal toolkit: D Barkskin, S Bear Frenzied Regeneration, E Nature's Grasp, R current-form resources (Cat Shifting Power / Bear Enrage / human self-Innervate). Existing Alt/Cmd self-heals, cures and trinket remain.

F/G/5 heals no longer automatically fall back to self while shapeshifted: a living friendly hover or selected target still works, and Alt/Cmd deliberately forces self. Human-form self fallback remains. Only H forcibly cancels form; client-side failed-cast form retention is not guaranteed.
R falls back to Shred until Ravage is learned. The Cat control button stays Dash until Pounce is learned; Dash must itself be learned. Run `/fs update` after training to refresh these choices.

## Upgrade from 3.6.x or 3.7.x

Replace files, restart WoW, then out of combat:

```text
/fs targeting
```

Check both layouts, Shift+W with a different focus, and the protected heal fallback, then `/fs save`. The existing form-page slots stay unchanged.

## Switch layouts immediately

```text
/fs a
/fs b
```

A uses numbers; B uses Q/E. These commands switch **bindings**, in any form while out of combat. They prepare missing direct-bound macros on upgrade but preserve existing macro bodies; `/fs targeting` is required once to apply the new heal behaviour. No per-form setup or reload is needed to switch. Character bindings are saved; `/fs save` also captures a recovery snapshot and flushes addon data to disk.

| Action | A | B |
| --- | --- | --- |
| Claw / Maul / human Roots | 1 | Q |
| Bite / Primal Bite / Wrath | 2 | E |
| Rake / Swipe / Moonfire | 3 | Shift+Q |
| Rip / Lacerate / Starfire | 4 | Shift+E |
| Dash/Pounce / Bash / Roots | Q | 1 |
| Charge / human Hibernate | E | 2 |
| Shifting Power / Enrage / self-Innervate | Alt/Cmd+R | Alt/Cmd+R |
| Faerie Fire, all forms | Shift+W or Z | Shift+W, Z or 4 |
| Focus Faerie Fire | Shift+Z | Shift+Z |

Shift modifies the original control keys for focus; Shift+W is explicitly normal hover/target Faerie Fire. Plain 3 in B and Shift+3 are free; old addon Alt/Cmd+1, +2 and +J shortcuts are retired. R is rear attack in Cat, Roar in Bear, Soothe Animal in human. T/X remain Roots/Hibernate in every form. See the [complete key map](FeralSetup/KEYBINDS.txt).

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
- `/fs restore` restores the saved snapshot, including directly bound macros; `/fs undo` restores pre-setup state. Follow with `/reload`.
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
