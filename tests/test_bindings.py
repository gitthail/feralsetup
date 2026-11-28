"""Simulated Lua 5.1 binding setup and macro condition checks for the fixed v3.9.1 packages."""
from pathlib import Path
import itertools
import sys
import re
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
ADDON=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'FeralSetup'
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
SlashCmdList={}; messages={}; bindings={}; FeralSetupCharDB={leftKey='SECTION'}
function print(s) table.insert(messages,s) end
function SetBinding(k,v) assert(not k:find('CMD%-'));bindings[k]=v; return true end
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
for f in (ADDON/'FeralSetup.toc').read_text().splitlines():
 if f.endswith('.lua'): lua.execute((ADDON/f).read_text())
g=lua.globals();A=g.FeralSetup;layout=g.FeralSetupLayout
assert layout.edition in ('Numbers','QE') and layout.bindingProfiles is None
qe=layout.edition=='QE'
for k,v in [('N','MULTIACTIONBAR2BUTTON12'),('`','MULTIACTIONBAR1BUTTON9'),('SECTION','MULTIACTIONBAR1BUTTON9'),('ALT-F','OLD'),('META-R','MULTIACTIONBAR1BUTTON9'),('ALT-R','MULTIACTIONBAR1BUTTON9'),('SHIFT-META-R','MULTIACTIONBAR1BUTTON9'),('SHIFT-Q','OLD'),('F12','UNRELATED'),('Z','ACTIONBUTTON9'),('SHIFT-R','MULTIACTIONBAR1BUTTON9')]:g.bindings[k]=v
setup=g.findUp(g.findUp(g.SlashCmdList.FERALSETUP,'applySetup'),'setupBindings')
assert setup()
assert g.bindings['N'] is None and g.bindings['`'] is None and g.bindings['SECTION'] is None
assert g.bindings['F12']=='UNRELATED'
assert g.bindings['ALT-F'] is None and g.bindings['SHIFT-Q']==('ACTIONBUTTON3' if qe else 'ACTIONBUTTON7')
for k,v in layout.bindings.items():
 assert g.bindings[k]==v,(k,v)
 if 'META-' in k:
  alt=k.replace('META-','');alt='ALT-'+alt
  assert g.bindings[alt]==v,k
assert g.bindings['META-R']=='ACTIONBUTTON9' and g.bindings['ALT-R']=='ACTIONBUTTON9' and g.bindings['SHIFT-META-R'] is None
assert g.bindings['Z']=='MULTIACTIONBAR1BUTTON9'
assert g.bindings['SHIFT-R'] is None
assert g.bindings['4']==('MULTIACTIONBAR1BUTTON9' if qe else 'ACTIONBUTTON4')
assert g.bindings['CTRL-SHIFT-R'] is None
assert g.bindings['META-S']=='ACTIONBUTTON11'
assert g.bindings['META-J'] is None
assert g.bindings['SHIFT-W']=='MULTIACTIONBAR3BUTTON12'
assert g.bindings['SHIFT-SPACE']=='MULTIACTIONBAR2BUTTON12'
assert g.bindings['ALT-Q']=='ACTIONBUTTON7'
# Re-running migration must not remove an unrelated user assignment.
g.bindings['N']='OPENALLBAGS';assert setup();assert g.bindings['N']=='OPENALLBAGS'
# Windows rejects META keys: skip them without hiding genuine Alt failures.
lua.execute("""
local original=SetBinding
function IsWindowsClient() return true end
function SetBinding(k,v)
 assert(not k:match('^CMD%-'), 'Command key attempted on Windows')
 return original(k,v)
end
""")
assert setup()
for k,v in layout.bindings.items():
 if 'META-' not in k: assert g.bindings[k]==v,(k,v)
lua.execute("""
local original=SetBinding
function SetBinding(k,v)
 if k=='ALT-MOUSEWHEELDOWN' and v then return false end
 return original(k,v)
end
""")
assert not setup()
assert 'ALT-MOUSEWHEELDOWN' in g.messages[len(g.messages)]
lua.execute("function SetBinding(k,v) bindings[k]=v;return true end; IsWindowsClient=nil")
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

def run(name,mods=(),form=3,stealth=False,units=None,cast_blocked=False):
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
   if cast_blocked:continue
   if action=='Cat Form':state['form']=3
   elif action=='Bear Form':state['form']=1
   elif action=='Prowl':state['stealth']=not state['stealth']
  elif cmd in ('/focus','/clearfocus'):out.append((cmd,unit))
 return out,state

for mods in [(),('shift',),('ctrl',),('alt',),('cmd',)]:
 for stealth in [False,True]:
  out,_=run('Cat Q',mods=mods,stealth=stealth)
  expected=('Dash','target') if mods==('alt',) or (mods in [(),('ctrl',)] and not stealth) else ('Pounce','focus' if mods==('shift',) else 'mouseover') if stealth and mods in [(),('shift',),('ctrl',)] else None
  assert out==([expected] if expected else []),(mods,stealth,out)
assert run('Cat Q',form=1)[0]==[]
assert run('Cat Rear',stealth=True)[0]==[('Ravage','target')]
assert run('Cat Rear')[0]==[('Shred','target')]
assert run('Prowl')[1]['stealth'] is True
assert run('Prowl',stealth=True)[1]['stealth'] is False
assert run('Prowl',form=1)[0]==[]
for name,form in [('Cat Form',3),('Bear Form',1)]:
 for initial in [0,1,3]:
  _,state=run(name,form=initial)
  assert state['form']==form
  for _ in range(10):
   out,state=run(name,form=state['form'])
   assert out==[] and state['form']==form
 for mod in ['cmd','alt']:
  out,state=run(name,form=form,mods=[mod]);assert out==[(name,'target')] and state['form']==form
  out,state=run(name,form=0,mods=[mod]);assert out==[(name,'target')] and state['form']==form
# Failed re-casts must not first execute /cancelform and expose the player.
for name,form in [('Cat Form',3),('Bear Form',1)]:
 assert '/cancelform' not in macros[name]
 for mod in ['cmd','alt']:
  out,state=run(name,form=form,mods=[mod],cast_blocked=True)
  assert out==[(name,'target')] and state['form']==form
for mod in ['cmd','alt']:
 assert run('Set Focus',mods=[mod,'shift'])[0]==[('/clearfocus','target')]
assert run('Faerie Fire',mods=['shift'])[0]==[('Faerie Fire','focus')]
assert run('Faerie Fire',mods=['ctrl','shift'])[0]==[('Faerie Fire','focus')]
assert run('Set Focus',mods=['shift'])[0]==[('/focus','mouseover')]
# Both self modifiers must work identically, including with Shift/Ctrl held.
heals={'Rejuvenation','Regrowth','Healing Touch'}
friendly=['Rejuvenation','Regrowth','Healing Touch','Remove Curse','Poison Cleanse','Innervate','Thorns','Mark of the Wild']
for name in friendly:
 for mod in ['cmd','alt']:
  for extra in [(),('shift',),('ctrl',),('shift','ctrl')]:
   out,_=run(name,mods=(mod,)+extra)
   assert out[-1][1]=='player',(name,mod,extra,out)
 # Explicit friendly target, then player fallback when no friendly unit exists.
 assert run(name,mods=['ctrl'])[0]==([] if name in heals else [(name if name!='Poison Cleanse' else 'Cure Poison','player')])
 assert '@mouseover' in macros[name]
 assert run(name,mods=['shift'])[0]==[]
assert [layout.main.cat[i].name for i in range(1,5)]==['Claw','Ferocious Bite','Rake','Rip']
assert layout.main.human[7].name=='Roots' and layout.main.human[8].name=='Hibernate'
assert layout.fixed.support[7].name=='Roots' and layout.fixed.support[8].name=='Hibernate'
assert layout.bindings['T']=='MULTIACTIONBAR1BUTTON7' and layout.bindings['X']=='MULTIACTIONBAR1BUTTON8'
assert layout.main.cat[5].name=='Cat Rear' and layout.main.cat[7].name=='Cat Q'
assert layout.main.bear[5].name=='Demoralizing Roar' and layout.main.bear[10].name=='Challenging Roar'
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
assert len(g.installed)==35  # 34 guide macros + one unrelated macro.
assert g.installed[1].body==macros['Prowl']
assert g.installed[2].body=='/say untouched'
assert len(g.FeralSetupCharDB.macroReplacements)==1
assert A.macros(True) is not None and len(g.installed)==35
print('PASS: binding migration/aliases, macro limits, stealth selection/toggle, focus, self/mouseover routing, single-press forms, Q/E no-autoshift, real macro updater and idempotence.')

# Targeting migration uses explicit macros; native mouseover is disabled.
lua.execute("cvars={};modified={};function GetCVar(k) return cvars[k] or '0' end;function SetCVar(k,v) cvars[k]=v end;function SetModifiedClick(k,v) modified[k]=v end")
targeting=g.findUp(g.SlashCmdList.FERALSETUP,'setupTargetingSettings')
targeting()
assert g.cvars['enableMouseoverCast']=='0' and g.cvars['autoSelfCast']=='1' and g.cvars['autoUnshift']=='1'
assert all(g.modified[k]=='NONE' for k in ['SELFCAST','FOCUSCAST','MOUSEOVERCAST'])
# User Ctrl shortcuts must survive subsequent binding setup.
g.bindings['CTRL-Q']='USER_ACTION';g.bindings['CTRL-F']='USER_HEAL'
g.bindings['CTRL-SHIFT-R']='MULTIACTIONBAR1BUTTON9'
assert setup()
assert g.bindings['CTRL-Q']=='USER_ACTION' and g.bindings['CTRL-F']=='USER_HEAL'
assert g.bindings['CTRL-SHIFT-R'] is None
for name in ['Bash','Cat Charge','Bear Charge','Growl','Roots','Hibernate']:
 assert '@mouseover' in macros[name] and 'mod:ctrl' not in macros[name]
 out,_=run(name,mods=['shift'])
 assert out[-1][1]=='focus',name
print('PASS: native mouseover disabled, explicit self/focus routing, and freed Ctrl bindings. Client casting and form-validation behaviour is not simulated.')

# The installed package has one fixed map; all first-four slots are direct/bleed.
attack_keys=['Q','E','SHIFT-Q','SHIFT-E'] if qe else ['1','2','3','4']
control_keys=['1','2'] if qe else ['Q','E']
for form,attacks in {'cat':['Claw','Ferocious Bite','Rake','Rip'],
                     'bear':['Maul','Primal Bite','Swipe','Lacerate'],
                     'human':['Moonfire','Wrath','Starfire','Hurricane']}.items():
 for index,(key,name) in enumerate(zip(attack_keys,attacks),1):
  assert layout.bindings[key]=='ACTIONBUTTON'+str(index),(form,key)
  assert layout.main[form][index].name==name,(form,key,name)
 for key,name in zip(control_keys,{'cat':['Cat Q','Cat Charge'],'bear':['Bash','Bear Charge'],'human':['Roots','Hibernate']}[form]):
  slot=int(layout.bindings[key].replace('ACTIONBUTTON',''))
  assert layout.main[form][slot].name==name,(form,key,name)
for key in ['SHIFT-'+k for k in control_keys]+['SHIFT-T','SHIFT-X','SHIFT-6']:
 assert g.bindings[key] is not None,key
assert layout.bindings['ALT-Q']=='ACTIONBUTTON7'
assert layout.bindings['ALT-D']=='MULTIACTIONBAR2BUTTON1'
assert layout.bindings['ALT-E']=='MULTIACTIONBAR2BUTTON2'
assert layout.bindings['SHIFT-3'] is None
if qe:assert layout.bindings['3'] is None
else:assert g.bindings['SHIFT-1'] is None and g.bindings['SHIFT-2'] is None
print('PASS: fixed '+layout.edition+' keys match physical page slots in every form.')

# Mouseover selection is explicit: live ally/enemy, dead, wrong faction, focus override.
ally={'exists':True,'help':True};enemy={'exists':True,'harm':True}
for name in friendly:
 spell='Cure Poison' if name=='Poison Cleanse' else name
 for hover,want in [(ally,'mouseover'),(enemy,'target'),({'exists':True,'help':True,'dead':True},'target'),({},'target')]:
  units={'mouseover':hover,'target':ally,'player':ally,'focus':enemy}
  assert run(name,units=units)[0]==[(spell,want)],(name,hover)
  assert run(name,mods=['alt'],units=units)[0]==[(spell,'player')]
 assert run(name,units={'target':enemy,'mouseover':enemy,'player':ally})[0]==([] if name in heals else [(spell,'player')])
for name in ['Bash','Cat Charge','Bear Charge','Growl','Roots','Hibernate','Pounce','Faerie Fire','Moonfire']:
 spell={'Roots':'Entangling Roots','Cat Charge':'Feral Charge (Cat)','Bear Charge':'Feral Charge'}.get(name,name)
 for hover,want in [(enemy,'mouseover'),(ally,'target'),({'exists':True,'harm':True,'dead':True},'target'),({},'target')]:
  assert run(name,units={'mouseover':hover,'target':enemy,'focus':enemy})[0]==[(spell,want)],(name,hover)
 assert run(name,units={'mouseover':ally,'target':ally})[0]==[]
 if name!='Moonfire':
  assert run(name,mods=['shift'],units={'mouseover':enemy,'target':enemy,'focus':{}})[0]==[]
  assert run(name,mods=['shift'],units={'mouseover':enemy,'target':enemy,'focus':enemy})[0]==[(spell,'focus')]
assert run('Rebirth',units={'mouseover':dict(ally,dead=True),'target':ally})[0]==[('Rebirth','mouseover')]
assert run('Rebirth',units={'mouseover':ally,'target':ally})[0]==[]
# A failed cast must not have a separate form-cancel command in front of it.
# This proves macro structure, NOT the client's own autoUnshift failure behaviour.
for name,body in macros.items():
 if name!='Leave Form':assert '/cancelform' not in body,name
for name in friendly+['Roots','Hibernate','Moonfire','Rebirth','Tranquility']:
 _,state=run(name,cast_blocked=True);assert state['form']==3,name
# Render the actual learned/unlearned variants and exercise their selectors.
learned=dict(macros)
for trained in [False,True]:
 cfg=lua.table_from(dict(g.FeralSetupDefaults.items()));cfg.hasRavage=trained;cfg.hasPounce=trained
 for _,m in g.FeralSetupMacros.items():
  macros[m.name]=A.renderMacro(m,cfg);assert len(macros[m.name].encode())<=255,m.name
 assert run('Cat Rear',stealth=True)[0]==[('Ravage' if trained else 'Shred','target')]
 assert run('Cat Rear',stealth=False)[0]==[('Shred','target')]
 assert run('Cat Q',stealth=True)[0]==([('Pounce','mouseover')] if trained else [('Dash','target')])
 assert run('Cat Q',stealth=True,mods=['shift'],units={'focus':{},'target':enemy,'mouseover':enemy})[0]==[]
 assert run('Cat Q',stealth=True,mods=['alt'])[0]==[('Dash','target')]
macros=learned
# The real config uses learned spellbook entries, including higher spell ranks.
lua.execute("""
spells={'Shred'}
function GetNumSpellTabs() return 1 end
function GetSpellTabInfo() return 'Druid',nil,0,#spells end
function GetSpellBookItemName(i) return spells[i] end
function GetSpellBookItemInfo(i) return 'SPELL',i end
""")
cfg,_=A.config();assert not cfg.hasRavage and not cfg.hasPounce
lua.execute("spells={'Shred','Ravage','Pounce'}")
cfg,_=A.config();assert cfg.hasRavage and cfg.hasPounce
# All rank-independent fallbacks update on /fs update; unrelated macros survive.
assert A.macros(True)
i=A.findMacro('Cat Rear',None,None);assert 'Ravage' in g.installed[i].body
lua.execute("spells={'Shred'}")
assert A.macros(True)
i=A.findMacro('Cat Rear',None,None);assert 'Ravage' not in g.installed[i].body
assert g.installed[2].body=='/say untouched'
print('PASS: explicit hover/self/focus priority, invalid targets, learned/unlearned opener fallbacks and no forced cancellation before casts.')
# Modern spellbook API: a visible but unlearned FUTURESPELL is not an opener.
lua.execute("""
GetNumSpellTabs=nil;GetSpellTabInfo=nil;GetSpellBookItemName=nil
Enum={SpellBookSpellBank={Player=0},SpellBookItemType={Spell=1,FutureSpell=2}}
C_Spell={GetSpellName=function(id) return id==100 and 'Ravage' or 'Pounce' end}
C_SpellBook={
 GetNumSpellBookSkillLines=function() return 1 end,
 GetSpellBookSkillLineInfo=function() return {itemIndexOffset=0,numSpellBookItems=2} end,
 GetSpellBookItemInfo=function(i) return {spellID=i==1 and 100 or 101,itemType=i==1 and 2 or 1} end
}
""")
cfg,_=A.config();assert not cfg.hasRavage and cfg.hasPounce
print('PASS: modern spellbook future-spell entries cannot enable an unlearned opener.')

# A stray heal key against an enemy/empty/dead target must not request a cast
# in any animal form, even with autoSelfCast enabled by the addon.
for name in heals:
 for form in [0,1,2,3,4]:
  for hover,target in itertools.product([{},enemy,dict(ally,dead=True)],repeat=2):
   units={'mouseover':hover,'target':target,'player':ally}
   for mods in [(),('ctrl',)]:
    out,state=run(name,form=form,units=units,mods=mods)
    assert out==([(name,'player')] if form==0 else []),(name,form,mods,out)
    assert state['form']==form
   for mod in ['alt','cmd']:
    assert run(name,form=form,units=units,mods=[mod])[0]==[(name,'player')]
  assert run(name,form=form,units={'mouseover':ally,'target':enemy})[0]==[(name,'mouseover')]
  assert run(name,form=form,units={'target':ally})[0]==[(name,'target')]
# Shift+W must never follow Shift+Z's focus branch (including missing focus).
for form in [0,1,2,3,4]:
 for focus in [enemy,{}]:
  for hover,want in [(enemy,'mouseover'),(ally,'target'),({},'target')]:
   units={'mouseover':hover,'target':enemy,'focus':focus}
   assert run('Faerie Pull',form=form,mods=['shift'],units=units)[0]==[('Faerie Fire',want)]
  assert run('Faerie Pull',form=form,mods=['shift'],units={'target':ally,'focus':focus})[0]==[]
 assert run('Faerie Pull',form=form,mods=['shift','alt'])[0]==[]
for mod in ['alt','cmd']:
 for form,want in [(0,[('Innervate','player')]),(1,[('Enrage','target')]),(3,[('Shifting Power','target')]),(2,[]),(4,[])]:
  out,state=run('Form Resource',form=form,mods=[mod])
  assert out==want and state['form']==form,(form,mod,out)
assert 'Form' not in macros['Form Resource'].replace('Shifting Power','')
print('PASS: accidental-heal guards in every form, deliberate ally/self healing, Shift+W normal targeting, and form-specific personal resources.')
