"""Simulated Lua 5.1 binding setup and macro condition checks for v3.5."""
from pathlib import Path
import itertools
import re
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
SlashCmdList={}; messages={}; bindings={}; FeralSetupCharDB={leftKey='SECTION'}
function print(s) table.insert(messages,s) end
function SetBinding(k,v) bindings[k]=v; return true end
function SaveBindings(scope) assert(scope==2);return true end
function GetBindingAction(k) return bindings[k] or '' end
function GetBindingKey() return nil end
function UnitClass() return 'Druid','DRUID' end
function UnitFactionGroup() return 'Alliance' end
function CreateFrame() return {RegisterEvent=function() end,SetScript=function() end} end
function findUp(fn,name)
 for i=1,100 do
  local n,v=debug.getupvalue(fn,i)
  if not n then break end
  if n==name then return v end
 end
end
''')
for f in (ROOT/'FeralSetup/FeralSetup.toc').read_text().splitlines():
 if f.endswith('.lua'): lua.execute((ROOT/'FeralSetup'/f).read_text())
g=lua.globals();A=g.FeralSetup;layout=g.FeralSetupLayout
for k,v in [('N','MULTIACTIONBAR2BUTTON12'),('`','MULTIACTIONBAR1BUTTON9'),('SECTION','MULTIACTIONBAR1BUTTON9'),('ALT-F','OLD'),('CMD-R','MULTIACTIONBAR1BUTTON9'),('ALT-R','MULTIACTIONBAR1BUTTON9'),('CMD-SHIFT-R','MULTIACTIONBAR1BUTTON9'),('SHIFT-Q','OLD'),('F12','UNRELATED')]:g.bindings[k]=v
setup=g.findUp(g.findUp(g.SlashCmdList.FERALSETUP,'applySetup'),'setupBindings')
assert setup()
assert g.bindings['N'] is None and g.bindings['`'] is None and g.bindings['SECTION'] is None
assert g.bindings['F12']=='UNRELATED'
assert g.bindings['ALT-F'] is None and g.bindings['SHIFT-Q'] is None
for k,v in layout.bindings.items():
 assert g.bindings[k]==v,(k,v)
 if k.startswith('CMD-'): assert g.bindings['ALT-'+k[4:]]==v,k
assert g.bindings['CMD-R'] is None and g.bindings['ALT-R'] is None and g.bindings['CMD-SHIFT-R'] is None
assert g.bindings['SHIFT-R']=='MULTIACTIONBAR1BUTTON9'
assert g.bindings['CTRL-SHIFT-R']=='MULTIACTIONBAR1BUTTON9'
assert g.bindings['CMD-J']=='ACTIONBUTTON11'
assert g.bindings['SHIFT-SPACE']=='MULTIACTIONBAR2BUTTON12'
assert g.bindings['ALT-Q']=='ACTIONBUTTON7'
# Re-running migration must not remove an unrelated user assignment.
g.bindings['N']='OPENALLBAGS';assert setup();assert g.bindings['N']=='OPENALLBAGS'
macros={m.name:A.text(m.body,g.FeralSetupDefaults) for _,m in g.FeralSetupMacros.items()}
for config in ({'cat':'2','bear':'1','aquatic':'3','travel':'4','bearSpell':'Dire Bear Form','bearCharge':'Feral Charge','poison':'Abolish Poison','trinket':'13'},):
 c=lua.table_from(config)
 for _,m in g.FeralSetupMacros.items():assert len(A.text(m.body,c).encode())<=255 and len(m.name)<=16,m.name

# Evaluate only the secure macro predicates used by this addon; no game timing claims.
def match(group,state):
 unit=next((c[1:] for c in group.split(',') if c.startswith('@')),'target')
 for token in group.split(','):
  if not token or token.startswith('@'):continue
  key,_,value=token.partition(':');neg=key.startswith('no');key=key[2:] if neg else key
  if key=='mod':result=bool(state['mods'] & set(value.split('/'))) if value else bool(state['mods'])
  elif key=='form':result=str(state['form']) in value.split('/') if value else state['form']!=0
  elif key=='stealth':result=state['stealth']
  elif key in ('exists','help','harm','dead'):result=state['units'].get(unit,{}).get(key,False)
  else:raise AssertionError(token)
  if result==neg:return False,unit
 return True,unit

def select(text,state):
 for branch in text.split(';'):
  branch=branch.strip();groups=re.findall(r'\[([^]]*)\]',branch);action=re.sub(r'\[[^]]*\]','',branch).strip()
  if not groups:return action,'target'
  for group in groups:
   ok,unit=match(group,state)
   if ok:return action,unit
 return None

def run(name,mods=(),form=3,stealth=False,units=None):
 state={'mods':set(mods),'form':form,'stealth':stealth,'units':units or {'target':{'exists':True,'harm':True},'focus':{'exists':True,'harm':True},'mouseover':{'exists':True,'harm':True},'player':{'exists':True,'help':True}}}
 out=[]
 for line in macros[name].splitlines():
  if not line.startswith('/'):continue
  cmd,_,text=line.partition(' ');choice=select(text,state)
  if choice is None:continue
  action,unit=choice
  if cmd=='/stopmacro':break
  if cmd=='/cancelform':state['form']=0;out.append(('cancel',))
  elif cmd=='/cast':
   out.append((action,unit))
   if action=='Cat Form':state['form']=3
   elif action=='Bear Form':state['form']=1
   elif action=='Prowl':state['stealth']=not state['stealth']
  elif cmd in ('/focus','/clearfocus'):out.append((cmd,unit))
 return out,state

for mods in [(),('shift',),('ctrl',),('alt',),('cmd',)]:
 for stealth in [False,True]:
  out,_=run('Cat Q',mods=mods,stealth=stealth)
  expected=('Dash','target') if mods==('alt',) or (not mods and not stealth) else ('Pounce',{'shift':'focus','ctrl':'mouseover'}.get(mods[0] if mods else '', 'target')) if stealth and mods in [(),('shift',),('ctrl',)] else None
  assert out==([expected] if expected else []),(mods,stealth,out)
assert run('Cat Q',form=1)[0]==[]
assert run('Cat Rear',stealth=True)[0]==[('Ravage','target')]
assert run('Cat Rear')[0]==[('Shred','target')]
assert run('Prowl')[1]['stealth'] is True
assert run('Prowl',stealth=True)[1]['stealth'] is False
assert run('Prowl',form=1)[0]==[]
for name,form in [('Cat Form',3),('Bear Form',1)]:
 assert run(name,form=form)[0]==[]
 for mod in ['cmd','alt']:
  out,state=run(name,form=form,mods=[mod]);assert out==[('cancel',),(name,'target')] and state['form']==form
  out,state=run(name,form=0,mods=[mod]);assert out==[(name,'target')] and state['form']==form
for mod in ['cmd','alt']:
 assert run('Set Focus',mods=[mod,'shift'])[0]==[('/clearfocus','target')]
assert run('Faerie Fire',mods=['shift'])[0]==[('Faerie Fire','target')]
assert run('Faerie Fire',mods=['ctrl','shift'])[0]==[('Faerie Fire','mouseover')]
assert run('Set Focus',mods=['shift'])[0]==[('/focus','mouseover')]
# Both self modifiers must work identically, including with Shift/Ctrl held.
friendly=['Rejuvenation','Regrowth','Healing Touch','Remove Curse','Poison Cleanse','Innervate','Thorns','Mark of the Wild']
for name in friendly:
 for mod in ['cmd','alt']:
  for extra in [(),('shift',),('ctrl',),('shift','ctrl')]:
   out,_=run(name,mods=(mod,)+extra)
   assert out[-1][1]=='player',(name,mod,extra,out)
 for dead,helpful in itertools.product([False,True],repeat=2):
  units={'mouseover':{'exists':True,'help':helpful,'dead':dead},'player':{'help':True,'exists':True}}
  out,_=run(name,mods=['ctrl'],units=units)
  assert bool(out)==(helpful and not dead),(name,dead,helpful,out)
 assert run(name,mods=['shift'])[0]==[]
assert layout.main.cat[1].name=='Claw' and layout.main.cat[2].name=='Rake'
assert layout.main.cat[5].name=='Cat Rear' and layout.main.cat[7].name=='Cat Q'
assert layout.main.bear[5].name=='Lacerate' and layout.main.bear[10].name=='Challenging Roar'
assert layout.main.bear[11].name=='Frenzied Regeneration'
assert layout.main.cat[12].name=='Cower'
# Q/E macros must never shift or use castsequence.
for name in ['Cat Q','Pounce','Bash','Cat Charge','Bear Charge','Prowl']:
 assert 'castsequence' not in macros[name] and 'Cat Form' not in macros[name] and 'Bear Form' not in macros[name]
# Exercise the real macro updater against existing user/guide macros.
lua.execute("""
installed={{name='Prowl',body='#showtooltip Prowl\\n/cast !Prowl'},
 {name='Personal Macro',body='/say untouched'}}
function GetNumMacros() return #installed,0 end
function GetMacroInfo(i)
 local m=installed[i];if m then return m.name,134400,m.body end
end
function EditMacro(i,name,icon,body) installed[i]={name=name,body=body};return i end
function CreateMacro(name,icon,body) installed[#installed+1]={name=name,body=body};return #installed end
""")
assert A.macros(True) is not None
assert len(g.installed)==33  # 32 guide macros + one unrelated macro.
assert g.installed[1].body==macros['Prowl']
assert g.installed[2].body=='/say untouched'
assert len(g.FeralSetupCharDB.macroReplacements)==1
assert A.macros(True) is not None and len(g.installed)==33
print('PASS: binding migration/aliases, macro limits, stealth selection/toggle, focus, self/mouseover routing, single-press forms, Q/E no-autoshift, real macro updater and idempotence.')
