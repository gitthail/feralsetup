FERAL SETUP 3.4 — LEVEL-UP GUIDE

Private chat reminders are enabled by default for Alliance Druids, levels 15-30.
Each level-up shows the recommended current and next area, plus training notes
on milestone levels. No login spam; no messages beyond level 30.
/feralsetup guide       Show current area, next area, quests and training notes.
/feralsetup guide off   Disable automatic reminders for this character.
/feralsetup guide on    Enable them again. Manual guide works while disabled.
The saved route is a flexible reference, not completed-quest tracking.
Source: Feral_Leveling_and_Professions.html (agreed 17 November 2026).

UPGRADE FROM 3.3
Replace the addon files and restart WoW so the new Lua file is loaded.
No setup, macro update or bar reset is needed for the guide.
Existing macro, binding and recovery behaviour is unchanged.

FERAL SETUP 3.3 — MARK OF THE WILD TARGETING

Mark on 8 now matches Thorns on 9: plain = friendly living mouseover,
friendly living target, then self; Cmd = always self; Ctrl = friendly living
mouseover only; Shift alone = inactive. Both leave form.
Setup clears conflicting Cmd/Ctrl/Shift+8 and +9 bindings.
Upgrade: replace addon, restart, humanoid/main page 1/out of combat,
/feralsetup setup then /feralsetup save. Existing Cat/Bear pages stay intact.

FRESH INSTALL / REBUILD
Out of combat, in humanoid, main page 1: /feralsetup setup
In each learned Cat/Bear form: /feralsetup form
After checking and placing any personal items: /feralsetup save
Use only forms you have learned. Empty/unlearned native spell slots stay reserved.
Personal consumable/item slots marked KEEP are not overwritten by setup.

MACROS AND COMMANDS
The pack now has 30 macros; new entries use General Macros. Existing character
copies are accepted. Same-name guide macros in both accessible pools are replaced
by setup/install/update. Unrelated macro names are left alone; nothing is deleted.
Keybindings and recovery snapshots remain character-specific.

/feralsetup setup    Replace same-name guide macros, fixed bars, bindings and
                    humanoid page. Start humanoid, main page 1.
/feralsetup form     Place current form page only; reuse existing macro bodies.
/feralsetup install  Replace/create guide macros only; no bar or binding changes.
/feralsetup update   Same macro-only replacement, with learned forms/poison detected.
/feralsetup save     Record current snapshot, then reload to persist it.
/feralsetup restore  Restore saved layout, bindings and referenced macro bodies.
                    Follow with /reload. Do not save a wiped layout first.
/feralsetup undo     Restore original pre-setup layout and its referenced macros.
/feralsetup status   Show version, form pages and macro capacity.
/feralsetup leftkey §  Choose your actual unmodified key immediately left of 1.

SCOPE
No automatic layout changes at login, no combat automation or spell execution.
Native action bars only. Layout changes require explicit out-of-combat commands.
This patch adds Mark targeting and modified-8 conflict handling; the
v3.1 same-name overwrite and form-only placement behaviour is retained.

Validation is offline with simulated APIs, not inside your live Mac WoW client.
See OFFLINE_TESTS.txt for checks executed for this version.
