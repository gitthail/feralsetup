FERAL SETUP 3.7.0 — EXPLICIT MOUSEOVER AND A/B LAYOUTS

UPGRADE FROM 3.6.x
Replace files and restart WoW. Out of combat:
/fs targeting
Check your hover heal, Roots and Moonfire, then /fs save.
Existing v2 action slots remain unchanged; do not rebuild pages just to switch.

QUICK SWITCH (any form, out of combat)
/fs a       Numbers: Cat 1 Claw, 2 Bite, 3 Rake, 4 Rip; Q/E controls.
/fs b       Q/E attacks, Shift+Q/E finishers; 1/2 controls.
Z is Faerie Fire in BOTH; Shift+Z targets focus. B additionally keeps FF on 4.
Shift+3 is Shifting Power/Enrage/Hurricane in BOTH; B also keeps plain 3.
Switching changes only bindings, preserves items/macros/action pages, saves
character-specific bindings, and reports binding errors. A failed switch
attempts to restore the previous binding set. Run /fs save to capture a new
recovery snapshot and flush SavedVariables to disk after testing your choice.

FIRST INSTALL / UPGRADE FROM BEFORE 3.6.0
Start humanoid, main page 1, out of combat:
/fs setup b    (or /fs setup a; setupa/setupb also accepted)
Enter Cat: /fs form
Enter Bear: /fs form
Check all three pages, then /fs save.
Only this initial placement needs each form. Unlearned spell slots are empty.

TARGETING
Heals/cures/buffs: Cmd/Alt self; otherwise friendly living mouseover ->
friendly living target -> self. Shift alone does nothing.
CC/charge/FF: Shift hostile focus; otherwise hostile living mouseover ->
hostile living target. Invalid focus does not fall back.
Moonfire: hostile hover -> hostile target. Rebirth: dead ally hover -> target.
Native mouseover off; native modified self/focus NONE. Ctrl remains free.
Only H / Leave Form explicitly cancels form. Casting relies on the client's
autoUnshift=1, set out of combat. No mana/range/LOS-aware secure cancellation
is claimed. A valid target outside range stays the chosen target, not fallback.

STEALTH FALLBACKS
R: Shred until Ravage learned, then stealthed Ravage / normal Shred.
Control key (A Q / B 1): Dash until Pounce learned, then stealthed Pounce /
normal Dash. Dash must itself be learned. Alt+Q always selects Cat Dash.
/fs update refreshes learned-opener choices after training (no auto updates).
Native attack spell ranks still need manual replacement after training.

COMMANDS (both /fs and /feralsetup accepted)
/fs a | b              Quick binding-only layout switch.
/fs targeting          Refresh macros, targeting settings and selected bindings.
/fs setup [a|b]        Full setup, including humanoid and fixed bars.
/fs form               Place current page; reuse existing macro bodies.
/fs update | install   Replace same-name macros, detect learned forms/openers.
/fs bindings [a|b]     Binding-only switch/reapply.
/fs save               Snapshot and reload to persist data.
/fs restore            Restore saved actions/bindings/settings/layout; then /reload.
/fs undo               Restore pre-setup snapshot; then /reload.
/fs status             Version, layout, pages, targeting settings and spell checks.
/fs guide [on|off]     Current/next area or private reminder toggle, Alliance 15-30.

No automatic layout restoration, spell execution or combat decision scripts.
32 templates, new entries in General Macros. Same-name definitions replaced;
unrelated macros preserved. Nothing auto-installs just from copying files.
Mage/Rogue remain guide-only proposals. See Guide.html and Leveling.html.
See OFFLINE_TESTS.txt for checks and live-client limits.
