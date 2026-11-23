FERAL SETUP 3.5.6 — MAC/WINDOWS BINDINGS AND CAT STEALTH ACTIONS

Use /fs for every command. /feralsetup remains supported.
From 3.5.5: replace files and /reload; no layout changes needed.

See KEYBINDS.txt for the full side-by-side layout and all modifiers.
Every Cmd shortcut also works with Alt. No automatic form change on Q/E/B.
B toggles Prowl in Cat; B remains Challenging Roar in Bear.
Shift+R = Faerie Fire; Cmd/Alt+J = Frenzied Regeneration in Bear.
Shift+Space = set focus; Cmd/Alt+Shift+Space = clear focus.
Alt+Q = Dash in Cat, including stealth.

FRESH INSTALL / UPGRADE FROM BEFORE 3.5
Replace the FeralSetup folder's files, then restart WoW.
Out of combat, in humanoid form on main page 1: /fs setup
In Cat Form: /fs form
In Bear Form: /fs form
After checking your layout: /fs save
Only populate forms you have learned. Setup replaces same-name guide macros
and configured bars/bindings. Personal slots marked KEEP are not overwritten.
Unlearned native spell slots remain empty. Train and place ranks manually.

UPGRADE FROM 3.5–3.5.4
Replace files, /reload. Out of combat in humanoid form, main page 1:
/fs form
Then enter Cat and run /fs form again, followed by /fs save.
Cat 1/2 = Claw/Bite; 3/4 = Rake/Rip. Human Q/E = Roots/Hibernate.
Human Q/E support Shift focus and Ctrl mouseover. T/X still work in every form.
Bear and fixed bars need no rebuild. If coming from before 3.5.4, also run
/fs update and /fs bindings to apply earlier fixes.

COMMANDS
/fs bindings Apply keybindings only; leave action bars unchanged.
/fs setup    Replace guide macros, fixed bars, bindings, humanoid page.
/fs form     Place current form page; reuse existing macro bodies.
/fs install  Replace/create guide macros only; no bar/binding changes.
/fs update   Same as install; detect learned forms and poison upgrade.
/fs save     Save recovery snapshot and reload to persist it.
/fs restore  Restore saved layout, bindings and referenced macros.
/fs undo     Restore original pre-setup layout and referenced macros.
/fs status   Version, form pages, macro capacity and recovery status.
/fs guide    Current recommended area, next area, quests and training.
/fs guide on|off   Toggle private level-up reminders per character.
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
