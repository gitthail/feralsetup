"""Integration checks using simulated APIs; no live casting/timing claims."""
from pathlib import Path
from lupa.lua51 import LuaRuntime
root=Path(__file__).resolve().parents[1]
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute(r'''
SlashCmdList={}; messages={}; bindings={F12='PERSONAL'}; actions={}; installed={}
cvars={enableMouseoverCast='1',autoSelfCast='0',autoUnshift='0',lockActionBars='0',alwaysShowActionBars='0'}
modified={SELFCAST='ALT',FOCUSCAST='SHIFT',MOUSEOVERCAST='CTRL'}
current=0; combat=false; actionWrites=0; macroWrites=0; saveCalls=0
function print(s) table.insert(messages,s) end
function UnitClass() return 'Druid','DRUID' end
function UnitFactionGroup() return 'Alliance' end
function InCombatLockdown() return combat end
function CreateFrame() return {RegisterEvent=function() end,SetScript=function() end} end
function GetCVar(k) return cvars[k] end
function SetCVar(k,v) if k~=refusedSetting then cvars[k]=v end end
function GetModifiedClick(k) return modified[k] end
function SetModifiedClick(k,v) modified[k]=v end
function GetBindingAction(k) return bindings[k] or '' end
local function commands()
 local seen,out={},{}
 for _,v in pairs(bindings) do if not seen[v] then seen[v]=true;out[#out+1]=v end end
 table.sort(out);return out
end
function GetNumBindings() return #commands() end
function GetBinding(i) return commands()[i] end
function GetBindingKey(action)
 local keys={};for k,v in pairs(bindings) do if v==action then keys[#keys+1]=k end end
 return unpack(keys)
end
function SetBinding(k,v)
 if rejectKey==k then rejectKey=nil;return false end
 if windows and k:match('^CMD%-') then error('CMD attempted on Windows') end
 bindings[k]=v;return true
end
function SaveBindings(n) assert(n==2);saveCalls=saveCalls+1;return true end
function IsWindowsClient() return windows or false end
function GetNumMacros() return #installed,0 end
function GetMacroInfo(i) local m=installed[i];if m then return m.name,134400,m.body end end
function EditMacro(i,n,icon,body) macroWrites=macroWrites+1;installed[i]={name=n,body=body};return i end
function CreateMacro(n,icon,body) macroWrites=macroWrites+1;installed[#installed+1]={name=n,body=body};return #installed end
function GetActionInfo(i) local a=actions[i];if a then return a.kind,a.id end end
function GetCursorInfo() if cursor then return cursor.kind,cursor.id end end
function ClearCursor() cursor=nil end
function PickupAction(i) actionWrites=actionWrites+1;cursor=actions[i];actions[i]=nil end
function PlaceAction(i) actionWrites=actionWrites+1;actions[i],cursor=cursor,actions[i] end
function PickupMacro(i) assert(installed[i]);cursor={kind='macro',id=i} end
function PickupItem(i) cursor={kind='item',id=i} end
function PickupSpellBookItem(i) assert(spells[i]);cursor={kind='spell',id=i} end
function GetSpellInfo(i) return spells[i] end
function GetNumSpellTabs() return 1 end
function GetSpellTabInfo() return 'Druid',nil,0,#spells end
function GetSpellBookItemName(i) return spells[i] end
function GetSpellBookItemInfo(i) return 'SPELL',i end
function GetNumShapeshiftForms() return 3 end
function GetShapeshiftFormInfo(i)
 local forms={{'Bear Form',5487},{'Aquatic Form',1066},{'Cat Form',768}}
 return nil,forms[i][1],false,forms[i][2]
end
function GetShapeshiftForm() return current end
function setForm(n)
 current=n;local base=n==0 and 0 or n==3 and 72 or 84
 for i=1,12 do _G['ActionButton'..i]={action=base+i} end
end
for i=1,12 do
 _G['MultiBarBottomLeftButton'..i]={action=60+i}
 _G['MultiBarBottomRightButton'..i]={action=48+i}
 _G['MultiBarRightButton'..i]={action=24+i}
end
setForm(0)
''')
for f in (root/'FeralSetup/FeralSetup.toc').read_text().splitlines():
 if f.endswith('.lua'):lua.execute((root/'FeralSetup'/f).read_text())
g=lua.globals();layout=g.FeralSetupLayout
spells=set(['Shred','Cat Form','Bear Form'])
for group in [layout.main,layout.fixed]:
 for _,rows in group.items():
  for _,row in rows.items():
   if row.kind=='spell':spells.add(row.name)
g.spells=lua.table_from(sorted(spells))
# Full initial setup on B, then each page once. Personal item slots survive.
lua.execute("actions[54]={kind='item',id=12345}")
g.SlashCmdList.FERALSETUP('setup b')
assert g.cvars.enableMouseoverCast=='0' and g.cvars.autoUnshift=='1'
assert g.actions[54].id==12345
assert len(g.installed)==32
for form in [3,1]:g.setForm(form);g.SlashCmdList.FERALSETUP('form')
assert g.FeralSetupCharDB.profiles['1'].layout=='B'
assert g.FeralSetupCharDB.profiles['1'].pages.cat[1]==73
assert g.FeralSetupCharDB.profiles['1'].pages.bear[1]==85
start_writes=(g.actionWrites,g.macroWrites)

def bindings():return dict(g.bindings.items())
def action_name(form,key):
 cmd=g.bindings[key]
 if cmd.startswith('ACTIONBUTTON'):base={0:0,3:72,1:84}[form];slot=base+int(cmd[12:])
 else:
  assert cmd.startswith('MULTIACTIONBAR1BUTTON'),cmd
  slot=60+int(cmd[len('MULTIACTIONBAR1BUTTON'):])
 a=g.actions[slot]
 if not a:return None
 return g.installed[a.id].name if a.kind=='macro' else g.spells[a.id]
for form in [0,3,1]:
 g.setForm(form)
 for profile in ['a','b','a','b']:
  g.SlashCmdList.FERALSETUP(profile)
  assert (g.actionWrites,g.macroWrites)==start_writes
  assert g.FeralSetupCharDB.profiles['1'].layout==profile.upper()
  assert action_name(form,'Z')=='Faerie Fire'
  assert action_name(form,'SHIFT-Z')=='Faerie Fire'
  if profile=='a':
   assert g.bindings['SHIFT-Q']=='ACTIONBUTTON7' and g.bindings['SHIFT-E']=='ACTIONBUTTON8'
   assert g.bindings['SHIFT-1'] is None and g.bindings['SHIFT-2'] is None
   expected={3:['Claw','Ferocious Bite','Rake','Rip'],1:['Maul','Primal Bite','Swipe','Lacerate'],0:['Roots','Wrath','Moonfire','Starfire']}[form]
   assert [action_name(form,k) for k in ['1','2','3','4']]==expected
  else:
   assert g.bindings['SHIFT-Q']=='ACTIONBUTTON3' and g.bindings['SHIFT-E']=='ACTIONBUTTON4'
   expected={3:['Claw','Rake','Ferocious Bite','Rip'],1:['Maul','Swipe','Primal Bite','Lacerate'],0:['Roots','Moonfire','Wrath','Starfire']}[form]
   assert [action_name(form,k) for k in ['Q','E','SHIFT-Q','SHIFT-E']]==expected
  assert g.bindings['F12']=='PERSONAL'
  assert g.bindings['SHIFT-3']=='ACTIONBUTTON9'
  assert g.bindings['ALT-Q']=='ACTIONBUTTON7'
# Switching in combat / with an occupied cursor has zero side effects.
before=bindings();g.combat=True;g.SlashCmdList.FERALSETUP('a');assert bindings()==before
g.combat=False;g.PickupItem(123);g.SlashCmdList.FERALSETUP('a');assert bindings()==before;g.ClearCursor()
# Invalid layout is rejected, not silently treated as B.
g.SlashCmdList.FERALSETUP('bindings nonsense');assert bindings()==before
# Failed SetBinding rolls back the complete previous binding set and profile.
g.rejectKey='E';g.SlashCmdList.FERALSETUP('a');assert bindings()==before
assert g.FeralSetupCharDB.profiles['1'].layout=='B'
assert 'Previous bindings restored' in g.messages[len(g.messages)]
# Saves/restores retain selected profile metadata as well as keys.
g.SlashCmdList.FERALSETUP('a');g.SlashCmdList.FERALSETUP('save')
g.SlashCmdList.FERALSETUP('b');g.SlashCmdList.FERALSETUP('restore')
assert g.FeralSetupCharDB.profiles['1'].layout=='A' and g.bindings['Q']=='ACTIONBUTTON7'
# Refused settings cannot produce the former false success message.
g.refusedSetting='enableMouseoverCast';g.cvars.enableMouseoverCast='1';g.messages=lua.table()
g.SlashCmdList.FERALSETUP('targeting');msgs='\n'.join(g.messages.values())
assert 'Could not verify targeting settings: enableMouseoverCast' in msgs
assert 'Explicit mouseover macros installed' not in msgs
# Windows profile switching avoids all CMD API calls, with Alt aliases intact.
g.refusedSetting=None;g.windows=True
g.SlashCmdList.FERALSETUP('b');assert g.bindings['ALT-MOUSEWHEELDOWN']=='MULTIACTIONBAR2BUTTON9'
assert g.FeralSetupCharDB.profiles['1'].layout=='B'
print('PASS: actual setup/form/profile commands, both key maps in all forms, stable bars/macros/items, focus-key cleanup, combat/cursor guards, rollback, restore metadata, setting refusal and Windows aliases.')
