"""Integration checks using simulated APIs; no live casting/timing claims."""
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime
root=Path(__file__).resolve().parents[1]
addon=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'FeralSetup'
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
 if ignoreKey==k and v then ignoreKey=nil;return true end
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
for f in (addon/'FeralSetup.toc').read_text().splitlines():
 if f.endswith('.lua'):lua.execute((addon/f).read_text())
g=lua.globals();layout=g.FeralSetupLayout
spells=set(['Shred','Cat Form','Bear Form'])
for group in [layout.main,layout.fixed]:
 for _,rows in group.items():
  for _,row in rows.items():
   if row.kind=='spell':spells.add(row.name)
g.spells=lua.table_from(sorted(spells))
# Full setup must ignore stale A/B selection and place this package directly.
lua.execute("FeralSetupCharDB={profiles={['1']={layout='B',pages={}}}}; actions[54]={kind='item',id=12345}")
g.SlashCmdList.FERALSETUP('setup')
assert g.cvars.enableMouseoverCast=='0' and g.cvars.autoUnshift=='1'
assert g.actions[54].id==12345 and len(g.installed)==34
for form in [3,1]:g.setForm(form);g.SlashCmdList.FERALSETUP('form')
assert g.FeralSetupCharDB.profiles['1'].pages.cat[1]==73
assert g.FeralSetupCharDB.profiles['1'].pages.bear[1]==85
assert layout.bindingProfiles is None and layout.profileNames is None
qe=layout.edition=='QE'
assert qe or layout.edition=='Numbers'
start_writes=(g.actionWrites,g.macroWrites)

def bindings():return dict(g.bindings.items())
def action_name(form,key):
 cmd=g.bindings[key]
 if cmd.startswith('MACRO '):
  name=cmd[6:];assert g.FeralSetup.findMacro(name) is not None;return name
 if cmd.startswith('ACTIONBUTTON'):base={0:0,3:72,1:84}[form];slot=base+int(cmd[12:])
 else:
  assert cmd.startswith('MULTIACTIONBAR1BUTTON'),cmd
  slot=60+int(cmd[len('MULTIACTIONBAR1BUTTON'):])
 a=g.actions[slot]
 if not a:return None
 return g.installed[a.id].name if a.kind=='macro' else g.spells[a.id]
attack_keys=['Q','E','SHIFT-Q','SHIFT-E'] if qe else ['1','2','3','4']
control_keys=['1','2'] if qe else ['Q','E']
for form in [0,3,1]:
 g.setForm(form);g.SlashCmdList.FERALSETUP('bindings')
 assert (g.actionWrites,g.macroWrites)==start_writes
 expected={3:['Claw','Ferocious Bite','Rake','Rip'],1:['Maul','Primal Bite','Swipe','Lacerate'],0:['Roots','Wrath','Moonfire','Starfire']}[form]
 assert [action_name(form,k) for k in attack_keys]==expected
 assert [action_name(form,k) for k in control_keys]=={3:['Cat Q','Cat Charge'],1:['Bash','Bear Charge'],0:['Roots','Hibernate']}[form]
 assert action_name(form,'Z')=='Faerie Fire' and action_name(form,'SHIFT-Z')=='Faerie Fire'
 assert action_name(form,'SHIFT-W')=='Faerie Pull' and g.bindings['SHIFT-3'] is None
 for mod in ['ALT','CMD']:
  assert action_name(form,mod+'-R')=='Form Resource'
  assert g.bindings[mod+'-D']=='MULTIACTIONBAR2BUTTON1'
  assert g.bindings[mod+'-E']=='MULTIACTIONBAR2BUTTON2'
  assert g.bindings[mod+'-S']=='ACTIONBUTTON11'
 assert g.bindings['F12']=='PERSONAL'
 if qe:assert g.bindings['3'] is None
 else:assert g.bindings['SHIFT-1'] is None and g.bindings['SHIFT-2'] is None
# Removed commands and layout arguments must neither switch nor silently install.
before=bindings()
for command in ['a','b','setupa','setupb','setup a','setup b','bindings a','bindings b']:
 g.SlashCmdList.FERALSETUP(command)
 assert bindings()==before and (g.actionWrites,g.macroWrites)==start_writes
 assert 'switching was removed' in g.messages[len(g.messages)]
# Combat/cursor guards and failed or silently ignored binding writes.
g.combat=True;g.SlashCmdList.FERALSETUP('bindings');assert bindings()==before;g.combat=False
g.PickupItem(123);g.SlashCmdList.FERALSETUP('bindings');assert bindings()==before;g.ClearCursor()
for failure in ['rejectKey','ignoreKey']:
 setattr(g,failure,'E');g.SlashCmdList.FERALSETUP('bindings');assert bindings()==before
 assert 'Previous bindings restored' in g.messages[len(g.messages)]
# Snapshots restore actions, keys and macros even when bound without a bar slot.
g.SlashCmdList.FERALSETUP('save');saved=g.FeralSetupCharDB.profiles['1'].saved
assert saved.edition==layout.edition and saved.layout is None
assert {m.name for m in saved.boundMacros.values()}=={'Faerie Pull','Form Resource'}
g.bindings['1']='PERSONAL_TEMP'
lua.execute("table.remove(installed,FeralSetup.findMacro('Faerie Pull'));table.remove(installed,FeralSetup.findMacro('Form Resource'))")
g.SlashCmdList.FERALSETUP('restore')
assert bindings()==before and action_name(1,'SHIFT-W')=='Faerie Pull'
assert action_name(1,'ALT-R')=='Form Resource'
assert [action_name(1,k) for k in attack_keys]==['Maul','Primal Bite','Swipe','Lacerate']
# Refused settings cannot produce a success message.
g.refusedSetting='enableMouseoverCast';g.cvars.enableMouseoverCast='1';g.messages=lua.table()
g.SlashCmdList.FERALSETUP('targeting');msgs='\n'.join(g.messages.values())
assert 'Could not verify targeting settings: enableMouseoverCast' in msgs
assert 'Explicit mouseover macros installed' not in msgs
# Windows uses the same fixed package but skips Command bindings.
g.refusedSetting=None;g.windows=True;g.SlashCmdList.FERALSETUP('bindings')
assert g.bindings['ALT-MOUSEWHEELDOWN']=='MULTIACTIONBAR2BUTTON9'
# Reapply creates missing direct macros without rewriting custom bodies or bars.
g.windows=False;lua.execute("table.remove(installed,FeralSetup.findMacro('Faerie Pull'))")
i=g.FeralSetup.findMacro('Form Resource');g.installed[i].body='/say personal resource edit'
writes=g.actionWrites;g.SlashCmdList.FERALSETUP('bindings')
assert g.actionWrites==writes and action_name(1,'SHIFT-W')=='Faerie Pull'
i=g.FeralSetup.findMacro('Form Resource');assert g.installed[i].body=='/say personal resource edit'
# Retired addon keys clear; unrelated personal replacements survive.
g.bindings['ALT-1']='MULTIACTIONBAR2BUTTON1';g.bindings['CMD-2']='MULTIACTIONBAR2BUTTON2'
g.bindings['ALT-J']='ACTIONBUTTON11';g.bindings['ALT-2']='PERSONAL_UTILITY'
g.SlashCmdList.FERALSETUP('bindings')
assert g.bindings['ALT-1'] is None and g.bindings['CMD-2'] is None and g.bindings['ALT-J'] is None
assert g.bindings['ALT-2']=='PERSONAL_UTILITY'
print('PASS: fixed '+layout.edition+' setup and form placement, stale selection ignored, removed switches inert, binding read-back/rollback, macro recovery, targeting, Windows aliases and personal edits.')
