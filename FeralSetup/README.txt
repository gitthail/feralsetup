FERAL SETUP 3.6.1 — V2 Q/E ATTACK LAYOUT

Use /fs for every command; /feralsetup remains supported.
See KEYBINDS.txt and Guide.html for all forms, modifiers and utility keys.

Cat: Q Claw, E Rake, Shift+Q Bite, Shift+E Rip, R Shred/Ravage.
Bear: Q Maul, E Swipe, Shift+Q Primal Bite, Shift+E Lacerate, R Roar.
Human: Q Roots, E Moonfire; Shift+Q Wrath, Shift+E Starfire, 3 Hurricane.
1 = Cat Dash/Pounce, Bear Bash, human Roots. 2 = Charge / human Hibernate.
Shift+1/2 = focus control. 3 = Cat Shifting Power / Bear Enrage.
4 = Faerie Fire in every form. T/X remain Roots/Hibernate in every form.
Alt+Q remains stealth Dash; Alt+1 remains Barkskin. Z and Shift+R are freed.
Native mouseover handles normal spells. Cmd/Alt-self and selected Shift-focus
remain macro-controlled. Ctrl is available for your own bindings.
Shift+D toggles the native damage meter; use visibility Always outside combat.

UPGRADE FROM 3.6.0
Replace files and restart WoW; no setup or bar changes needed.
Guide-only Mage/Rogue proposals are not addon profiles.
Leveling.html now explains efficient sessions from level 24 onward.

FIRST INSTALL / SWITCH TO V2
Replace files and restart WoW. Out of combat, humanoid form on main page 1:
/fs setup
Enter Cat: /fs form
Enter Bear: /fs form
Check your bars, then /fs save. Both animal pages need rebuilding for v2.
Setup updates macros, fixed bars, bindings and native targeting settings.
Personal item slots are preserved. Unlearned spells leave empty slots.
Train and update native spell ranks manually.

COMMANDS
/fs targeting       Update macros/bindings, enable native mouseover and auto-self
                    fallback, disable native self/focus modifiers; keep bars.
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
