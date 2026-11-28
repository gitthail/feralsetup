"""Integration checks using simulated APIs; no live casting/timing claims."""
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime
root=Path(__file__).resolve().parents[1]
addon=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'FeralSetup'
platform=sys.argv[2] if len(sys.argv)>2 else 'mac'
assert platform in ('mac','windows')
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute(r'''
SlashCmdList={}; messages={}; bindings={F12='PERSONAL'}; actions={}; installed={}
cvars={enableMouseoverCast='1',autoSelfCast='0',autoUnshift='0',lockActionBars='0',alwaysShowActionBars='0'}
modified={SELFCAST='ALT',FOCUSCAST='SHIFT',MOUSEOVERCAST='CTRL'}
current=0; combat=false; actionWrites=0; macroWrites=0; saveCalls=0; metaWrites=0; invalidKeys={}
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
 for _,v in pairs(bindings) do if not v:match('^MACRO ') and not seen[v] then seen[v]=true;out[#out+1]=v end end
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
 if k:find('CMD%-') or k:find('META%-SHIFT%-') or k:find('META%-CTRL%-') or (windows and k:find('META%-')) then
  invalidKeys[#invalidKeys+1]=k;return false
 end
 if k:find('META%-') then metaWrites=metaWrites+1 end
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
 current=n;local base=n==0 and 0 or n==3 and 72 or 96
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
g=lua.globals();g.windows=platform=='windows';layout=g.FeralSetupLayout
spells=set(['Shred','Cat Form','Bear Form','Find Herbs','Test Mount'])
for group in [layout.main,layout.fixed]:
 for _,rows in group.items():
  for _,row in rows.items():
   if row.kind=='spell':spells.add(row.name)
g.spells=lua.table_from(sorted(spells))
# Use the key names, native form page and item mistakes observed in the game cache.
lua.execute("FeralSetupCharDB={profiles={['1']={layout='B',pages={}}}}; actions[54]={kind='item',id=12345}")
g.actions[34]=lua.table_from({'kind':'spell','id':list(g.spells.values()).index('Find Herbs')+1})
g.actions[35]=lua.table_from({'kind':'spell','id':list(g.spells.values()).index('Revive')+1})
lua.execute("function GetItemInfo(id) if id==12345 then return 'Healing Potion' end end")
if platform=='mac':
 for key,cmd in {'META-C':'MULTIACTIONBAR2BUTTON6','META-R':'ACTIONBUTTON11','META-1':'MULTIACTIONBAR2BUTTON1','META-2':'MULTIACTIONBAR2BUTTON2'}.items():g.bindings[key]=cmd
g.SlashCmdList.FERALSETUP('setup')
assert len(g.invalidKeys)==0,list(g.invalidKeys.values())
assert g.cvars.enableMouseoverCast=='0' and g.cvars.autoUnshift=='1'
assert g.actions[54].id==12345 and len(g.installed)==34
for form in [3,1]:g.setForm(form);g.SlashCmdList.FERALSETUP('form')
assert g.FeralSetupCharDB.profiles['1'].pages.cat[1]==73
assert g.FeralSetupCharDB.profiles['1'].pages.bear[1]==97
assert layout.bindingProfiles is None and layout.boundMacros is None
assert not any(v.startswith('MACRO ') for v in layout.bindings.values())
qe=layout.edition=='QE';assert qe or layout.edition=='Numbers'
start_writes=(g.actionWrites,g.macroWrites)

def bindings():return dict(g.bindings.items())
def action_name(form,key):
 cmd=g.bindings[key]
 if cmd.startswith('ACTIONBUTTON'):slot={0:0,3:72,1:96}[form]+int(cmd[12:])
 else:
  slot=None
  for prefix,base in [('MULTIACTIONBAR1BUTTON',60),('MULTIACTIONBAR2BUTTON',48),('MULTIACTIONBAR3BUTTON',24)]:
   if cmd.startswith(prefix):slot=base+int(cmd[len(prefix):]);break
  assert slot is not None,cmd
 a=g.actions[slot]
 if not a:return None
 return g.installed[a.id].name if a.kind=='macro' else g.spells[a.id]
attack_keys=['Q','E','SHIFT-Q','SHIFT-E'] if qe else ['1','2','3','4']
control_keys=['1','2'] if qe else ['Q','E']
mods=['ALT','META'] if platform=='mac' else ['ALT']
for form in [0,3,1]:
 g.setForm(form);g.SlashCmdList.FERALSETUP('bindings')
 assert (g.actionWrites,g.macroWrites)==start_writes
 expected={3:['Claw','Ferocious Bite','Rake','Rip'],1:['Maul','Primal Bite','Swipe','Lacerate'],0:['Moonfire','Wrath','Starfire','Hurricane']}[form]
 assert [action_name(form,k) for k in attack_keys]==expected
 assert [action_name(form,k) for k in control_keys]=={3:['Cat Q','Cat Charge'],1:['Bash','Bear Charge'],0:['Roots','Hibernate']}[form]
 assert action_name(form,'Z')=='Faerie Fire' and action_name(form,'SHIFT-Z')=='Faerie Fire'
 assert action_name(form,'SHIFT-W')=='Faerie Pull' and g.bindings['SHIFT-3'] is None
 assert action_name(form,'7')=='Moonfire'
 for mod in mods:
  assert action_name(form,mod+'-R')=='Form Resource'
  assert g.bindings[mod+'-D']=='MULTIACTIONBAR2BUTTON1'
  assert g.bindings[mod+'-E']=='MULTIACTIONBAR2BUTTON2'
  assert g.bindings[mod+'-S']=='ACTIONBUTTON11'
  for key in ['F','G','5','C','V','Y','8','9']:assert g.bindings[mod+'-'+key] is None
 assert g.bindings['F12']=='PERSONAL'
 if qe:assert g.bindings['3'] is None
 else:assert g.bindings['SHIFT-1'] is None and g.bindings['SHIFT-2'] is None
assert len(g.invalidKeys)==0
if platform=='mac':
 assert g.bindings['META-1'] is None and g.bindings['META-2'] is None
 assert g.bindings['SHIFT-META-SPACE']=='MULTIACTIONBAR2BUTTON12'
else:assert g.metaWrites==0 and not any('META-' in k for k in bindings())
# The item audit names actual contents, warns on wrong types, and never changes slots.
g.messages=lua.table();writes=g.actionWrites;g.SlashCmdList.FERALSETUP('items');messages='\n'.join(g.messages.values())
assert 'Healing Potion (item)' in messages and 'Healthstone' in messages and 'EMPTY' in messages
assert 'Find Herbs (spell)' in messages and 'VERIFY MOUNT' in messages
assert 'Revive (spell)' in messages and 'WRONG TYPE' in messages
assert g.actionWrites==writes and g.spells[g.actions[34].id]=='Find Herbs' and g.spells[g.actions[35].id]=='Revive'
# Removed switches and guards remain inert.
before=bindings()
for command in ['a','b','setupa','setupb','setup a','setup b','bindings a','bindings b']:
 g.SlashCmdList.FERALSETUP(command);assert bindings()==before and (g.actionWrites,g.macroWrites)==start_writes
 assert 'switching was removed' in g.messages[len(g.messages)]
g.combat=True;g.SlashCmdList.FERALSETUP('bindings');assert bindings()==before;g.combat=False
g.PickupItem(123);g.SlashCmdList.FERALSETUP('bindings');assert bindings()==before;g.ClearCursor()
for failure in ['rejectKey','ignoreKey']:
 setattr(g,failure,'E');g.SlashCmdList.FERALSETUP('bindings');assert bindings()==before
 assert 'Previous bindings restored' in g.messages[len(g.messages)]
# A form install must repair a missing/legacy resource key as well as fill slot 9.
# Previously /fs form reported success and saved the page with both keys unbound.
for form in [0,3,1]:
 for old_action in [None,'MACRO Form Resource']:
  for mod in mods:g.bindings[mod+'-R']=old_action
  g.setForm(form);g.messages=lua.table();g.SlashCmdList.FERALSETUP('form')
  for mod in mods:
   assert g.bindings[mod+'-R']=='ACTIONBUTTON9'
   assert action_name(form,mod+'-R')=='Form Resource'
   assert g.FeralSetupCharDB.profiles['1'].saved.bindings[mod+'-R']=='ACTIONBUTTON9'
  assert 'bindings applied and verified' in '\n'.join(g.messages.values())
assert bindings()==before
# Rejected/silently ignored bindings must not fill a page or replace its snapshot.
for command in ['form','setup']:
 for failure in ['rejectKey','ignoreKey']:
  g.setForm(0);g.bindings['ALT-R']=None
  original=bindings();writes=g.actionWrites
  lua.execute("savedBeforeBindingFailure=FeralSetupCharDB.profiles['1'].saved")
  setattr(g,failure,'ALT-R');g.messages=lua.table();g.SlashCmdList.FERALSETUP(command)
  assert bindings()==original and g.actionWrites==writes
  assert lua.eval("rawequal(savedBeforeBindingFailure,FeralSetupCharDB.profiles['1'].saved)")
  messages='\n'.join(g.messages.values())
  assert 'bindings failed' in messages and 'bindings applied and verified' not in messages
  g.SlashCmdList.FERALSETUP('bindings')
assert bindings()==before
# Resource and normal FF now recover through visible action slots, without enumeration of direct macros.
g.SlashCmdList.FERALSETUP('save');saved=g.FeralSetupCharDB.profiles['1'].saved
assert saved.edition==layout.edition and saved.version==7 and len(saved.boundMacros)==0
assert saved.actions[9].name=='Form Resource' and saved.actions[36].name=='Faerie Pull'
g.bindings['ALT-R']=None;g.bindings['SHIFT-W']=None
lua.execute("table.remove(installed,FeralSetup.findMacro('Faerie Pull'));table.remove(installed,FeralSetup.findMacro('Form Resource'))")
g.SlashCmdList.FERALSETUP('restore')
assert bindings()==before and action_name(1,'SHIFT-W')=='Faerie Pull' and action_name(1,'ALT-R')=='Form Resource'
assert [action_name(1,k) for k in attack_keys]==['Maul','Primal Bite','Swipe','Lacerate']
# Windows restoration of a Mac snapshot must never try to write Command bindings.
if platform=='windows':
 saved.bindings['META-D']='MULTIACTIONBAR2BUTTON1';saved.bindings['SHIFT-META-SPACE']='MULTIACTIONBAR2BUTTON12'
 g.SlashCmdList.FERALSETUP('restore');assert len(g.invalidKeys)==0 and g.metaWrites==0
 assert g.bindings['ALT-D']=='MULTIACTIONBAR2BUTTON1'
# No success message on refused settings; ordinary binding reapply preserves custom macro bodies.
g.refusedSetting='enableMouseoverCast';g.cvars.enableMouseoverCast='1';g.messages=lua.table()
g.SlashCmdList.FERALSETUP('targeting');messages='\n'.join(g.messages.values())
assert 'Could not verify targeting settings: enableMouseoverCast' in messages and 'Explicit mouseover macros installed' not in messages
g.refusedSetting=None
i=g.FeralSetup.findMacro('Form Resource');g.installed[i].body='/say personal resource edit'
writes=(g.actionWrites,g.macroWrites);g.SlashCmdList.FERALSETUP('bindings')
assert (g.actionWrites,g.macroWrites)==writes and g.installed[i].body=='/say personal resource edit'
g.SlashCmdList.FERALSETUP('form')
assert g.macroWrites==writes[1] and g.installed[i].body=='/say personal resource edit'
# Recover legacy direct bindings even though GetNumBindings omits them.
g.bindings['ALT-R']='MACRO Form Resource';g.bindings['SHIFT-W']='MACRO Faerie Pull'
g.FeralSetupCharDB.profiles['1'].before=None;g.setForm(0);g.SlashCmdList.FERALSETUP('setup')
legacy=g.FeralSetupCharDB.profiles['1'].before
assert legacy.bindings['ALT-R']=='MACRO Form Resource' and legacy.bindings['SHIFT-W']=='MACRO Faerie Pull'
assert {m.name for m in legacy.boundMacros.values()}=={'Faerie Pull','Form Resource'}
# Unknown personal replacements outside active keys survive retirement cleanup.
g.bindings['ALT-1']='PERSONAL_UTILITY';g.bindings['ALT-J']='ACTIONBUTTON11'
g.SlashCmdList.FERALSETUP('bindings')
assert g.bindings['ALT-1']=='PERSONAL_UTILITY' and g.bindings['ALT-J'] is None
assert len(g.invalidKeys)==0,list(g.invalidKeys.values())
print('PASS: '+layout.edition+' on '+platform+': form installs repair resource bindings; rejected bindings cannot change bars or snapshots; native modifier syntax/order, stale Cmd cleanup, visible macro recovery, legacy direct snapshots, item auditing and preserved personal slots.')
