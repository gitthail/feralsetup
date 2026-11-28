FERAL SETUP 3.9.0 — FIXED NUMBERS VERSION

This package contains only the Numbers key map. No in-game layout switch.
Replacing the addon files does not change saved bars or bindings by itself.
Install only one FeralSetup folder at a time.

INSTALL OR UPGRADE (including from 3.8.x)
Replace the FeralSetup folder and restart WoW. Out of combat:
1. Human form, main action page 1: /fs setup
2. Enter Cat: /fs form
3. Enter Bear: /fs form
4. Check all three pages, then: /fs save

The first four bar slots have been reordered to direct build/finish then
bleed build/finish. Rebuild all three pages once; /fs targeting or /fs bindings
alone cannot migrate the old arrangement. Personal item slots are preserved.
Unlearned native spell slots are empty. See KEYBINDS.txt for this version.

Shift+W and Z = normal hover/target Faerie Fire; Shift+Z = focus.
Alt/Cmd+D Barkskin; +S Bear regeneration; +E Nature's Grasp; +R resources
(Cat Shifting Power / Bear Enrage / human self-Innervate).

TARGETING
Heals/cures/buffs: Cmd/Alt self; otherwise friendly living mouseover ->
friendly living target. Heals F/G/5 fall back to self ONLY in human form;
no friendly recipient while shapeshifted means no heal cast. Deliberate ally
healing can still leave form. Cures/buffs keep their existing self fallback.
Shift alone does nothing on friendly macros.
CC/charge/FF: Shift hostile focus (except Shift+W, always normal targeting); otherwise hostile living mouseover ->
hostile living target. Invalid focus does not fall back.
Moonfire: hostile hover -> hostile target. Rebirth: dead ally hover -> target.
Native mouseover off; native modified self/focus NONE. Ctrl remains free.
Only H / Leave Form explicitly cancels form. Casting relies on the client's
autoUnshift=1, set out of combat. No mana/range/LOS-aware secure cancellation
is claimed. A valid target outside range stays the chosen target, not fallback.

STEALTH FALLBACKS
R: Shred until Ravage learned, then stealthed Ravage / normal Shred.
Q: Dash until Pounce learned, then stealthed Pounce / normal Dash.
Dash must itself be learned. Alt+Q always selects Cat Dash.
/fs update refreshes learned-opener choices after training.
Native attack spell ranks still need manual replacement after training.

COMMANDS (both /fs and /feralsetup accepted)
/fs setup              Install this version's human page, fixed bars and bindings.
/fs form               Place current form page; reuse existing macro bodies.
/fs targeting          Refresh macros, targeting settings and fixed bindings.
/fs bindings           Reapply this version's bindings; leave bars unchanged.
/fs update | install   Replace same-name macros, detect learned forms/openers.
/fs save               Snapshot and reload to persist data.
/fs restore            Restore saved actions/bindings/settings/macros; then /reload.
/fs undo               Restore pre-setup snapshot; then /reload.
/fs status             Package edition, pages, targeting settings and spell checks.
/fs guide [on|off]     Current/next area or private reminder toggle, Alliance 15-30.

The old /fs a, /fs b and setup/bindings layout arguments are disabled.
An old saved A/B preference cannot change this package's installation.
No automatic layout restoration, spell execution or combat decision scripts.
34 templates, new entries in General Macros. Same-name definitions replaced;
unrelated macros preserved. Nothing auto-installs just from copying files.
Mage/Rogue remain guide-only proposals. See Guide.html and Leveling.html.
See OFFLINE_TESTS.txt for checks and live-client limits.
