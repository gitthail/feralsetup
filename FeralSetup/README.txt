FERAL SETUP 3.5.4 — MAC/WINDOWS BINDINGS AND CAT STEALTH ACTIONS

See KEYBINDS.txt for the full side-by-side layout and all modifiers.
Every Cmd shortcut also works with Alt. No automatic form change on Q/E/B.
B toggles Prowl in Cat; B remains Challenging Roar in Bear.
Shift+R = Faerie Fire; Cmd/Alt+J = Frenzied Regeneration in Bear.
Shift+Space = set focus; Cmd/Alt+Shift+Space = clear focus.
Alt+Q = Dash in Cat, including stealth.

INSTALL / UPGRADE TO 3.5.1
Replace the FeralSetup folder's files, then restart WoW.
Out of combat, in humanoid form on main page 1: /feralsetup setup
In Cat Form: /feralsetup form
In Bear Form: /feralsetup form
After checking your layout: /feralsetup save
Only populate forms you have learned. Setup replaces same-name guide macros
and configured bars/bindings. Personal slots marked KEEP are not overwritten.
Unlearned native spell slots remain empty. Train and place ranks manually.

UPGRADE FROM 3.5 ONLY
After /reload, run /feralsetup update, /feralsetup bindings, /feralsetup save.
No form-page rebuild is needed for this hotfix.

COMMANDS
/feralsetup bindings Apply keybindings only; leave action bars unchanged.
/feralsetup setup    Replace guide macros, fixed bars, bindings, humanoid page.
/feralsetup form     Place current form page; reuse existing macro bodies.
/feralsetup install  Replace/create guide macros only; no bar/binding changes.
/feralsetup update   Same as install; detect learned forms and poison upgrade.
/feralsetup save     Save recovery snapshot and reload to persist it.
/feralsetup restore  Restore saved layout, bindings and referenced macros.
/feralsetup undo     Restore original pre-setup layout and referenced macros.
/feralsetup status   Version, form pages, macro capacity and recovery status.
/feralsetup guide    Current recommended area, next area, quests and training.
/feralsetup guide on|off   Toggle private level-up reminders per character.
The legacy leftkey command remains optional; the layout no longer relies on it.

LEVEL GUIDE
The agreed Alliance Druid route covers levels 15-30; reminders default on.
It is a flexible reference, not completed-quest tracking. No login spam.
At level 30 it reports the end of the planned route; no later area is invented.
Saved preferences and recovery snapshots are local WoW SavedVariables data.

No automatic layout restoration, combat automation or spell execution.
All layout changes require explicit out-of-combat commands.
32 macro templates, using General Macros for new entries. Same-name guide
macros are updated; unrelated names are retained. No macros are deleted.
Offline simulated-API checks only; see OFFLINE_TESTS.txt.
