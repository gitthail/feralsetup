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
version=re.search(r'^## Version: (.+)$',(ROOT/'FeralSetup/FeralSetup.toc').read_text(),re.M)[1]
def rows(data):return ''.join('<tr>'+''.join('<td>'+html.escape(str(c))+'</td>' for c in row)+'</tr>' for row in data)
def label(entry):return entry.get('name','—')
keys=['1','2','3','4','R','6','Q','E','Z','B','Cmd/Alt+J','J']
combat=[]
for i,key in enumerate(keys):
 cat=label(layout['main']['cat'][i]);stealth=cat
 if cat=='Cat Rear':cat,stealth='Shred','Ravage'
 if cat=='Cat Q':cat,stealth='Dash','Pounce'
 if cat=='Prowl':cat,stealth='Prowl ON','Prowl OFF'
 combat.append([key,cat,stealth,label(layout['main']['bear'][i])])
support=[['F','Rejuvenation','Friendly routing below'],['G','Regrowth','Friendly routing below'],['5','Healing Touch','Friendly routing below'],['C','Remove Curse','Friendly routing below'],['V','Cure / Abolish Poison','Friendly routing below'],['Y','Innervate','Friendly routing below'],['Shift+R','Faerie Fire','Current target; Ctrl+Shift+R = enemy mouseover'],['T','Roots','Target; Shift = focus; Ctrl = enemy mouseover'],['X','Hibernate','Target; Shift = focus; Ctrl = enemy mouseover'],['U','Rebirth','Dead friendly mouseover → dead friendly target'],['7','Moonfire','Current enemy; leaves form'],['K','Tranquility','Leaves form to channel']]
utility=[['Cmd/Alt+1','Barkskin','8','Mark of the Wild'],['Cmd/Alt+2',"Nature’s Grasp",'9','Thorns'],['Cmd/Alt+3','Shadowmeld','0','Gift of the Wild'],['Cmd/Alt+4',"Elune’s Light",'−','Revive'],['Cmd/Alt+X','PvP trinket','=','Teleport: Moonglade'],['Cmd/Alt+Z','Healing potion','O','Track Humanoids'],['Cmd/Alt+B','Healthstone','P','Bandage'],['[ / ]','Food / drink','Backslash','Mount'],['L','Mana potion','Cmd/Alt+J','Frenzied Regeneration (Bear)']]
forms=[['Wheel up / down','Enter Cat / Bear; do nothing if already in that form'],['Cmd/Alt+wheel up / down','Deliberately re-shift Cat / Bear, including from the same form'],['Middle-click','Aquatic while swimming; Travel outdoors on land'],['H','Leave form, stop casting and attacking'],['Shift+Space','Set focus: living mouseover, otherwise living target'],['Cmd/Alt+Shift+Space','Clear focus'],['W/S · A/D','Forward/back · strafe left/right'],['Space · Tab','Jump · target nearest enemy'],['Page Up / Page Down','Zoom in / out']]
commands=[['/feralsetup setup','Replace guide macros, fixed bars, bindings and humanoid page. Start humanoid, main page 1.'],['/feralsetup form','Place the current form page; reuse existing macro bodies.'],['/feralsetup update','Replace/create guide macros; detect learned form numbers and poison upgrade. No bar/binding changes.'],['/feralsetup install','Same macro-only operation as update.'],['/feralsetup bindings','Apply keybindings without changing your action bars.'],['/feralsetup save','Record a recovery snapshot and reload to persist it.'],['/feralsetup restore','Restore saved layout, bindings and referenced macros. Follow with /reload.'],['/feralsetup undo','Restore the original pre-setup snapshot. Follow with /reload.'],['/feralsetup status','Show loaded version, form pages, macro capacity and recovery status.'],['/feralsetup guide','Current area, next area, quests and training notes.'],['/feralsetup guide off','Disable automatic level-up reminders for this character.'],['/feralsetup guide on','Enable automatic level-up reminders again.']]
# Read route checkpoints directly from the addon; keep recommendations in one place.
level=(ROOT/'FeralSetup/Leveling.lua').read_text()
route=re.findall(r"\{level=(\d+),area=([^\n]+),",level)
route_rows=[]
for i,(start,quoted) in enumerate(route):
 area=lua.eval(quoted)
 end=int(route[i+1][0])-1 if i+1<len(route) else 29
 route_rows.append([str(start)+'–'+str(end),area])
route_rows.append(['30','Finish the agreed route; train milestone abilities.'])
macro_rows=''.join('<details id="macro-'+str(i)+'"><summary>'+html.escape(m['name'])+'</summary><pre>'+html.escape(re.sub(r'\{\{(\w+)\}\}',lambda m:defaults.get(m[1],''),m['body']))+'</pre><button onclick="copyMacro('+str(i)+',this)">Copy macro</button></details>' for i,m in enumerate(macros))
files={'FeralSetup/'+p.name:p.read_text() for p in sorted((ROOT/'FeralSetup').iterdir()) if p.suffix in ('.lua','.toc','.txt')}
files['FeralSetup/Leveling.html']=(ROOT/'docs/Leveling.html').read_text()
def jsjson(obj):return json.dumps(obj,ensure_ascii=True).replace('<','\\u003c')
values={'VERSION':version,'COMBAT_ROWS':rows(combat),'SUPPORT_ROWS':rows(support),'UTILITY_ROWS':rows(utility),'FORM_ROWS':rows(forms),'COMMAND_ROWS':rows(commands),'ROUTE_ROWS':rows(route_rows),'MACRO_ROWS':macro_rows,'DATA_JSON':jsjson({'defaults':defaults,'macros':macros}),'FILES_JSON':jsjson(files),'ZIP_JS':(ROOT/'scripts/zip_store.js').read_text(),'CAT':defaults['cat'],'BEAR':defaults['bear'],'AQUATIC':defaults['aquatic'],'TRAVEL':defaults['travel']}
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
