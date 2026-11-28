"""Run with lupa available on PYTHONPATH; simulated WoW APIs only."""
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime
root = Path(__file__).resolve().parents[1]
addon = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'FeralSetup'
lua = LuaRuntime()
lua.execute('''
messages={}; SlashCmdList={}; playerLevel=19; class='DRUID'; faction='Alliance'
function print(s) table.insert(messages,s) end
function UnitClass() return 'Druid',class end
function UnitFactionGroup() return faction end
function UnitLevel() return playerLevel end
function CreateFrame()
 frame={}
 function frame:RegisterEvent(e) assert(e=='PLAYER_LEVEL_UP') end
 function frame:SetScript(e,f) assert(e=='OnEvent'); self.handler=f end
 return frame
end
function fire(level) messages={};frame.handler(frame,'PLAYER_LEVEL_UP',level) end
function joined() return table.concat(messages,'\n') end
'''.replace("'\n'", "'\\n'"))
for filename in (addon/'FeralSetup.toc').read_text().splitlines():
    if filename.endswith('.lua'):
        lua.execute((addon/filename).read_text())
g = lua.globals()
expected = {15:'Darkshore',19:'Darkshore',20:'Ashenvale',22:'Ashenvale',23:'Wetlands',24:'Wetlands',25:'Duskwood',26:'Duskwood',27:'Wetlands return',29:'Wetlands return'}
for level, area in expected.items():
    g.fire(level)
    assert f'Recommended now: {area}' in g.joined(), (level,g.joined())
    assert 'Next:' in g.joined()
for level in (1,14,31,60):
    g.fire(level); assert g.joined()==''
g.fire(30); assert 'ends at 30' in g.joined() and 'Travel Form' in g.joined()
g.fire(20); assert 'Level 20' in g.joined() and 'Great Cat Spirit' in g.joined()
g.FeralSetupCharDB = lua.table_from({'sentinel':'preserved'})
g.SlashCmdList.FERALSETUP('guide off'); g.fire(24); assert g.joined()==''
assert g.FeralSetupCharDB.sentinel=='preserved'
g.playerLevel=24; g.SlashCmdList.FERALSETUP('guide'); assert 'Quests:' in g.joined() and 'Reminders: off' in g.joined()
g.SlashCmdList.FERALSETUP('guide on'); g.fire(24); assert 'Rake' in g.joined()
lua.execute("class='MAGE'"); g.fire(20); assert g.joined()==''
lua.execute("class='DRUID'; faction='Horde'"); g.fire(20); assert g.joined()==''
lua.execute("faction='Alliance'")
for level in (14,15,20,23,25,27,30,31):
    g.playerLevel=level; g.messages=lua.table(); g.SlashCmdList.FERALSETUP('guide'); assert g.joined()
print('PASS: all addon files load in Lua 5.1; route boundaries, event level, training, commands, character setting preservation, faction/class filtering, guide limits.')
