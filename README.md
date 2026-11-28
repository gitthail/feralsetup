# FeralSetup — A and B variants

Personal WoW Forever Druid controls, recovery snapshots and levelling advice.

Choose one package below. Each ZIP extracts to a single **FeralSetup** folder ready to move into `Interface/AddOns`, with its own offline guides. No build step or renaming. Both support Windows and Mac.

| Variant | Attack keys | Control keys | Download | Folder |
| --- | --- | --- | --- | --- |
| **A — Numbers** | 1/2 direct, 3/4 bleed | Q/E | [FeralSetup.zip](https://github.com/gitthail/feralsetup/raw/refs/heads/main/variants/A-numbers/FeralSetup.zip) | [A-numbers](variants/A-numbers) |
| **B — Q/E** | Q/E direct, Shift+Q/E bleed | 1/2 | [FeralSetup.zip](https://github.com/gitthail/feralsetup/raw/refs/heads/main/variants/B-qe/FeralSetup.zip) | [B-qe](variants/B-qe) |

Install only **one** variant at a time; both use the addon folder name **FeralSetup**. To change variants, replace that folder with the other package and follow the setup steps below. The GitHub source archive contains both variants and the project files; use the individual ZIP links above for installation.

## Version 3.9.2

Fixed a setup bug: `/fs form` could fill resource button 9 and report success while its keys stayed unbound. It now applies and verifies the package bindings before placing the page. A binding failure leaves the page and saved snapshot unchanged.

For this repair, replace the files, run `/reload`, then `/fs form` in your current form. Resource remains **Alt+R** on Windows and **Alt/Command+R** on Mac.

Both fixed variants are published in their own folders. The root `FeralSetup/` source and the existing release's default ZIP remain **A — Numbers**: attacks on 1–4, controls on Q/E. Runtime A/B switching and saved layout selection have been removed. Each package installs its own single key map.

The table below shows **A — Numbers**; [B's complete map](variants/B-qe/FeralSetup/KEYBINDS.txt) covers the Q/E variant.

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

Both offline HTML guides are inside each variant's ZIP. The matching `Guide.html` and `KEYBINDS.txt` are also in each variant's `FeralSetup/` folder. The existing release's standalone guides are:

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

An independent addon folder can be checked with `python3 tests/test_setup.py /absolute/path/FeralSetup`. The packaging script accepts `--addon-dir`, `--guide-output` and `--zip-output` paths; these do not add runtime switching to the addon.

Rebuild both published variant ZIPs and their matching guides:

```sh
for variant in A-numbers B-qe; do
  python3 scripts/build_release.py \
    --addon-dir "variants/$variant/FeralSetup" \
    --guide-output "variants/$variant/FeralSetup/Guide.html" \
    --zip-output "variants/$variant/FeralSetup.zip"
  cp docs/Leveling.html "variants/$variant/FeralSetup/Leveling.html"
done
```

Each published folder is a complete package. Keep shared fixes in both variants and the root source; preserve their distinct `Layout.lua`, title and key-map documentation. Validate each variant on both platforms before publishing.
