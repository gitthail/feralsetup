"""Generate the HTML guide and one-folder install ZIP. Requires lupa."""
from pathlib import Path
import argparse
import html
import json
import re
import zipfile
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--addon-dir',type=Path,default=ROOT/'FeralSetup')
parser.add_argument('--guide-output',type=Path,default=ROOT/'docs/Guide.html')
parser.add_argument('--zip-output',type=Path,default=ROOT/'dist/FeralSetup.zip')
args=parser.parse_args()
ADDON=args.addon_dir.resolve()
lua=LuaRuntime()
for f in ['Data.lua','Layout.lua']:lua.execute((ADDON/f).read_text())
def native(x):
 if hasattr(x,'items'):
  data={k:native(v) for k,v in x.items()}
  if data and all(isinstance(k,int) for k in data):return [data[i] for i in range(1,len(data)+1)]
  return data
 return x
layout=native(lua.globals().FeralSetupLayout)
defaults=native(lua.globals().FeralSetupDefaults)
macros=native(lua.globals().FeralSetupMacros)
unlearned=native(lua.globals().FeralSetupUnlearnedMacros)
version=re.search(r'^## Version: (.+)$',(ADDON/'FeralSetup.toc').read_text(),re.M)[1]
def rows(data):return ''.join('<tr>'+''.join('<td>'+html.escape(str(c))+'</td>' for c in row)+'</tr>' for row in data)
def label(entry):return entry.get('name','—')
edition=layout['edition']
assert edition in ('Numbers','QE')
numbered=edition=='Numbers'
control,charge=('Q','E') if numbered else ('1','2')
def combat_rows():
 keys=(['1','2','3','4','Q','E'] if numbered else ['Q','E','SHIFT-Q','SHIFT-E','1','2','4'])+['R','ALT-R','Z','SHIFT-W','6','B','J','ALT-S']
 result=[]
 for key in keys:
  action=layout['bindings'][key]
  if action.startswith('ACTIONBUTTON'):
   i=int(action[len('ACTIONBUTTON'):])-1
   cat=label(layout['main']['cat'][i]);stealth=cat
   if cat=='Cat Rear':cat,stealth='Shred','Ravage if learned; otherwise Shred'
   if cat=='Cat Q':cat,stealth='Dash','Pounce if learned; otherwise Dash'
   if cat=='Prowl':cat,stealth='Prowl ON','Prowl OFF'
   row=[cat,stealth,label(layout['main']['bear'][i]),label(layout['main']['human'][i])]
  elif action=='MACRO Form Resource':
   row=['Shifting Power','Shifting Power','Enrage','Innervate (self)']
  else:
   assert action in ('MULTIACTIONBAR1BUTTON9','MACRO Faerie Pull')
   row=['Faerie Fire']*4
  result.append([key.replace('SHIFT-','Shift+').replace('ALT-','Cmd/Alt+')]+row)
 return rows(result)
support=[['F','Rejuvenation','Friendly hover → friendly target → self only in human; Cmd/Alt always self'],['G','Regrowth','Friendly hover → friendly target → self only in human; Cmd/Alt always self'],['5','Healing Touch','Friendly hover → friendly target → self only in human; Cmd/Alt always self'],['C','Remove Curse','Friendly mouseover → friendly target → self'],['V','Cure / Abolish Poison','Friendly mouseover → friendly target → self'],['Y','Innervate','Friendly mouseover → friendly target → self'],[('Shift+W / Z' if numbered else 'Shift+W / Z / 4'),'Faerie Fire','Hostile mouseover → hostile target. Shift+Z = focus; Shift+W never selects focus'],['T','Roots','Hostile mouseover → hostile target; Shift = focus'],['X','Hibernate','Hostile mouseover → hostile target; Shift = focus'],['U','Rebirth','Dead friendly mouseover → dead friendly target'],['7','Moonfire','Hostile mouseover → hostile target'],['K','Tranquility','Normal cast; no forced form cancellation']]
utility=[['Shift+D','Toggle native damage meter','', ''],['Cmd/Alt+D','Barkskin (damage protection)','8','Mark of the Wild'],['Cmd/Alt+E',"Nature’s Grasp (escape)",'9','Thorns'],['Cmd/Alt+3','Shadowmeld','0','Gift of the Wild'],['Cmd/Alt+4',"Elune’s Light",'−','Revive'],['Cmd/Alt+X','PvP trinket','=','Teleport: Moonglade'],['Cmd/Alt+Z','Healing potion','O','Track Humanoids'],['Cmd/Alt+B','Healthstone','P','Bandage'],['[ / ]','Food / drink','Backslash','Mount'],['Cmd/Alt+S','Frenzied Regeneration (Bear sustain)','Cmd/Alt+R','Shifting Power / Enrage / self-Innervate'],['L','Mana potion','','']]
forms=[['Wheel up / down','Enter Cat / Bear; do nothing if already in that form'],['Cmd/Alt+wheel up / down','Deliberately re-shift Cat / Bear, including from the same form'],['Middle-click','Aquatic while swimming; Travel outdoors on land'],['H','Leave form, stop casting and attacking'],['Shift+Space','Set focus: living mouseover, otherwise living target'],['Cmd/Alt+Shift+Space','Clear focus'],['W/S · A/D','Forward/back · strafe left/right'],['Space · Tab','Jump · target nearest enemy'],['Page Up / Page Down','Zoom in / out']]
commands=[['/fs setup',"Install this package's fixed bindings, macros, human page and fixed bars. Start human on page 1, then apply Cat/Bear with /fs form."],['/fs form','Place the current form page; reuse existing macro bodies. Required in Cat and Bear after installing/replacing a package.'],['/fs targeting','Refresh explicit mouseover macros/settings and the fixed bindings. Keeps bars; does not migrate old slot ordering.'],['/fs bindings','Reapply this package’s one key map, preserving bars and existing macro bodies.'],['/fs update','Replace/create guide macros; detect learned form numbers, poison upgrade and stealth openers. Run after learning Ravage/Pounce. No bar/binding changes.'],['/fs install','Same macro-only operation as update.'],['/fs save','Record a recovery snapshot and reload to persist it.'],['/fs restore','Restore saved bindings, actions and referenced macros. Follow with /reload.'],['/fs undo','Restore original pre-setup snapshot. Follow with /reload.'],['/fs status','Package edition, form pages, targeting settings and currently learned stealth openers.'],['/fs guide','Current area, next area, quests and training notes.'],['/fs guide off','Disable automatic level-up reminders for this character.'],['/fs guide on','Enable automatic level-up reminders again.']]
# Read route checkpoints directly from the addon; keep recommendations in one place.
level=(ADDON/'Leveling.lua').read_text()
route=re.findall(r"\{level=(\d+),area=([^\n]+),",level)
route_rows=[]
for i,(start,quoted) in enumerate(route):
 area=lua.eval(quoted)
 end=int(route[i+1][0])-1 if i+1<len(route) else 29
 route_rows.append([str(start)+'–'+str(end),area])
route_rows.append(['30','Finish the agreed route; train milestone abilities.'])
macro_rows=''.join('<details id="macro-'+str(i)+'"><summary>'+html.escape(m['name'])+'</summary><pre>'+html.escape(re.sub(r'\{\{(\w+)\}\}',lambda m:defaults.get(m[1],''),unlearned.get(m['name'],m['body'])))+'</pre><button onclick="copyMacro('+str(i)+',this)">Copy macro</button></details>' for i,m in enumerate(macros))
files={'FeralSetup/'+p.name:p.read_text() for p in sorted(ADDON.iterdir()) if p.suffix in ('.lua','.toc','.txt','.xml')}
files['FeralSetup/Leveling.html']=(ROOT/'docs/Leveling.html').read_text()
def jsjson(obj):return json.dumps(obj,ensure_ascii=True).replace('<','\\u003c')
values={'VERSION':version,'EDITION':edition,'COMBAT_ROWS':combat_rows(),'CONTROL_KEY':control,'CHARGE_KEY':charge,'ATTACK_SUMMARY':('Cat: 1 → 2 = Claw → Bite; 3 → 4 = Rake → Rip. Bear: 1 Maul, 2 Primal Bite, 3 Swipe, 4 Lacerate. Human: 1 Roots, 2 Wrath, 3 Moonfire, 4 Starfire.' if numbered else 'Cat: Q → E = Claw → Bite; Shift+Q → Shift+E = Rake → Rip. Bear: Q Maul, E Primal Bite, Shift+Q Swipe, Shift+E Lacerate. Human: Q Roots, E Wrath, Shift+Q Moonfire, Shift+E Starfire.'),'SECONDARY_NOTE':('Shift+Q/E focus the controls; Shift+1/2/3 are unassigned.' if numbered else 'Shift+Q/E are bleed/secondary damage. Shift+1/2 focus the controls. Plain 3 and Shift+3 are unassigned; 4 is an extra Faerie Fire key.'),'SUPPORT_ROWS':rows(support),'UTILITY_ROWS':rows(utility),'FORM_ROWS':rows(forms),'COMMAND_ROWS':rows(commands),'ROUTE_ROWS':rows(route_rows),'MACRO_ROWS':macro_rows,'DATA_JSON':jsjson({'defaults':defaults,'macros':macros,'unlearned':unlearned}),'FILES_JSON':jsjson(files),'ZIP_JS':(ROOT/'scripts/zip_store.js').read_text(),'CAT':defaults['cat'],'BEAR':defaults['bear'],'AQUATIC':defaults['aquatic'],'TRAVEL':defaults['travel']}
template=(ROOT/'scripts/guide_template.html').read_text()
guide=re.sub(r'\{\{([A-Z_]+)\}\}',lambda m:values[m[1]],template)
args.guide_output.parent.mkdir(parents=True,exist_ok=True)
args.guide_output.write_text(guide)
files['FeralSetup/Guide.html']=guide
args.zip_output.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(args.zip_output,'w',zipfile.ZIP_DEFLATED) as z:
 for path,content in sorted(files.items()):
  info=zipfile.ZipInfo(path,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
  z.writestr(info,content.encode())
with zipfile.ZipFile(args.zip_output) as z:
 assert z.testzip() is None
 assert {p.split('/')[0] for p in z.namelist()}=={'FeralSetup'}
 assert 'FeralSetup/FeralSetup.toc' in z.namelist()
 for path,content in files.items():assert z.read(path).decode()==content
print(f'Built {edition} v{version}: {args.guide_output} and {args.zip_output}; {len(files)} files in one FeralSetup folder.')
