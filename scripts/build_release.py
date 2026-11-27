"""Generate the HTML guide and one-folder install ZIP. Requires lupa."""
from pathlib import Path
import html
import json
import re
import zipfile
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
lua=LuaRuntime()
for f in ['Data.lua','Layout.lua']:lua.execute((ROOT/'FeralSetup'/f).read_text())
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
version=re.search(r'^## Version: (.+)$',(ROOT/'FeralSetup/FeralSetup.toc').read_text(),re.M)[1]
def rows(data):return ''.join('<tr>'+''.join('<td>'+html.escape(str(c))+'</td>' for c in row)+'</tr>' for row in data)
def label(entry):return entry.get('name','—')
def combat_rows(profile):
 keys={'A':['1','2','3','4','Q','E','R','SHIFT-3','Z','6','B','J','ALT-J'],
       'B':['Q','E','SHIFT-Q','SHIFT-E','1','2','R','3','Z','6','B','J','ALT-J']}[profile]
 result=[]
 for key in keys:
  action=layout['bindingProfiles'][profile][key]
  if action.startswith('ACTIONBUTTON'):
   i=int(action[len('ACTIONBUTTON'):])-1
   cat=label(layout['main']['cat'][i]);stealth=cat
   if cat=='Cat Rear':cat,stealth='Shred','Ravage if learned; otherwise Shred'
   if cat=='Cat Q':cat,stealth='Dash','Pounce if learned; otherwise Dash'
   if cat=='Prowl':cat,stealth='Prowl ON','Prowl OFF'
   row=[cat,stealth,label(layout['main']['bear'][i]),label(layout['main']['human'][i])]
  else:
   assert action=='MULTIACTIONBAR1BUTTON9'
   row=['Faerie Fire']*4
  result.append([key.replace('SHIFT-','Shift+').replace('ALT-','Cmd/Alt+')]+row)
 return rows(result)
support=[['F','Rejuvenation','Friendly mouseover → friendly target → self'],['G','Regrowth','Friendly mouseover → friendly target → self'],['5','Healing Touch','Friendly mouseover → friendly target → self'],['C','Remove Curse','Friendly mouseover → friendly target → self'],['V','Cure / Abolish Poison','Friendly mouseover → friendly target → self'],['Y','Innervate','Friendly mouseover → friendly target → self'],['Z (also 4 in B)','Faerie Fire','Hostile mouseover → hostile target; Shift = focus'],['T','Roots','Hostile mouseover → hostile target; Shift = focus'],['X','Hibernate','Hostile mouseover → hostile target; Shift = focus'],['U','Rebirth','Dead friendly mouseover → dead friendly target'],['7','Moonfire','Hostile mouseover → hostile target'],['K','Tranquility','Normal cast; no forced form cancellation']]
utility=[['Shift+D','Toggle native damage meter','', ''],['Cmd/Alt+1','Barkskin','8','Mark of the Wild'],['Cmd/Alt+2',"Nature’s Grasp",'9','Thorns'],['Cmd/Alt+3','Shadowmeld','0','Gift of the Wild'],['Cmd/Alt+4',"Elune’s Light",'−','Revive'],['Cmd/Alt+X','PvP trinket','=','Teleport: Moonglade'],['Cmd/Alt+Z','Healing potion','O','Track Humanoids'],['Cmd/Alt+B','Healthstone','P','Bandage'],['[ / ]','Food / drink','Backslash','Mount'],['L','Mana potion','Cmd/Alt+J','Frenzied Regeneration (Bear)']]
forms=[['Wheel up / down','Enter Cat / Bear; do nothing if already in that form'],['Cmd/Alt+wheel up / down','Deliberately re-shift Cat / Bear, including from the same form'],['Middle-click','Aquatic while swimming; Travel outdoors on land'],['H','Leave form, stop casting and attacking'],['Shift+Space','Set focus: living mouseover, otherwise living target'],['Cmd/Alt+Shift+Space','Clear focus'],['W/S · A/D','Forward/back · strafe left/right'],['Space · Tab','Jump · target nearest enemy'],['Page Up / Page Down','Zoom in / out']]
commands=[['/fs a','Numbers layout in every form. Bindings only; no form-page rebuild.'],['/fs b','Q/E layout in every form. Bindings only; no form-page rebuild.'],['/fs targeting','Upgrade macros/settings/bindings: explicit mouseover, native mouseover off, autoUnshift on. Keeps action-bar slots.'],['/fs setup [a|b]','Full install: macros, fixed bars, bindings and humanoid page. Start humanoid, main page 1. Omitting layout keeps the selection (B initially). setupa/setupb are aliases.'],['/fs form','Place the current form page; reuse existing macro bodies. Needed once per animal on initial setup, not to switch A/B.'],['/fs update','Replace/create guide macros; detect learned form numbers, poison upgrade and stealth openers. Run after learning Ravage/Pounce. No bar/binding changes.'],['/fs install','Same macro-only operation as update.'],['/fs bindings [a|b]','Apply selected bindings only; same as a/b when specified.'],['/fs save','Record a recovery snapshot and reload to persist it.'],['/fs restore','Restore saved layout selection, bindings, actions and referenced macros. Follow with /reload.'],['/fs undo','Restore original pre-setup snapshot. Follow with /reload.'],['/fs status','Version, A/B selection, form pages, targeting settings and currently learned stealth openers.'],['/fs guide','Current area, next area, quests and training notes.'],['/fs guide off','Disable automatic level-up reminders for this character.'],['/fs guide on','Enable automatic level-up reminders again.']]
# Read route checkpoints directly from the addon; keep recommendations in one place.
level=(ROOT/'FeralSetup/Leveling.lua').read_text()
route=re.findall(r"\{level=(\d+),area=([^\n]+),",level)
route_rows=[]
for i,(start,quoted) in enumerate(route):
 area=lua.eval(quoted)
 end=int(route[i+1][0])-1 if i+1<len(route) else 29
 route_rows.append([str(start)+'–'+str(end),area])
route_rows.append(['30','Finish the agreed route; train milestone abilities.'])
macro_rows=''.join('<details id="macro-'+str(i)+'"><summary>'+html.escape(m['name'])+'</summary><pre>'+html.escape(re.sub(r'\{\{(\w+)\}\}',lambda m:defaults.get(m[1],''),unlearned.get(m['name'],m['body'])))+'</pre><button onclick="copyMacro('+str(i)+',this)">Copy macro</button></details>' for i,m in enumerate(macros))
files={'FeralSetup/'+p.name:p.read_text() for p in sorted((ROOT/'FeralSetup').iterdir()) if p.suffix in ('.lua','.toc','.txt','.xml')}
files['FeralSetup/Leveling.html']=(ROOT/'docs/Leveling.html').read_text()
def jsjson(obj):return json.dumps(obj,ensure_ascii=True).replace('<','\\u003c')
values={'VERSION':version,'COMBAT_ROWS':combat_rows('B'),'COMBAT_A_ROWS':combat_rows('A'),'SUPPORT_ROWS':rows(support),'UTILITY_ROWS':rows(utility),'FORM_ROWS':rows(forms),'COMMAND_ROWS':rows(commands),'ROUTE_ROWS':rows(route_rows),'MACRO_ROWS':macro_rows,'DATA_JSON':jsjson({'defaults':defaults,'macros':macros,'unlearned':unlearned}),'FILES_JSON':jsjson(files),'ZIP_JS':(ROOT/'scripts/zip_store.js').read_text(),'CAT':defaults['cat'],'BEAR':defaults['bear'],'AQUATIC':defaults['aquatic'],'TRAVEL':defaults['travel']}
template=(ROOT/'scripts/guide_template.html').read_text()
guide=re.sub(r'\{\{([A-Z_]+)\}\}',lambda m:values[m[1]],template)
(ROOT/'docs/Guide.html').write_text(guide)
files['FeralSetup/Guide.html']=guide
out=ROOT/'dist';out.mkdir(exist_ok=True)
with zipfile.ZipFile(out/'FeralSetup.zip','w',zipfile.ZIP_DEFLATED) as z:
 for path,content in sorted(files.items()):
  info=zipfile.ZipInfo(path,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
  z.writestr(info,content.encode())
with zipfile.ZipFile(out/'FeralSetup.zip') as z:
 assert z.testzip() is None
 assert {p.split('/')[0] for p in z.namelist()}=={'FeralSetup'}
 assert 'FeralSetup/FeralSetup.toc' in z.namelist()
 for path,content in files.items():assert z.read(path).decode()==content
print(f'Built v{version}: docs/Guide.html and dist/FeralSetup.zip; {len(files)} files in one FeralSetup folder.')
