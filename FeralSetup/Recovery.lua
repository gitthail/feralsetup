-- FeralSetup v3.5.6: setup, snapshots, restore. All changes require a slash command.
-- No automatic restoration on login, no combat handlers and no spell casting.
local A=FeralSetup
local unpack=unpack or table.unpack
local function copy(t)
 if type(t)~='table' then return t end
 local r={};for k,v in pairs(t) do r[k]=copy(v) end;return r
end
local function groupKey()
 local f=GetActiveTalentGroup or GetSpecialization
 local ok,g=pcall(f or function() return 1 end)
 return tostring(ok and g or 1)
end
local function db()
 FeralSetupCharDB=FeralSetupCharDB or {profiles={}}
 FeralSetupCharDB.profiles=FeralSetupCharDB.profiles or {}
 local k=groupKey()
 FeralSetupCharDB.profiles[k]=FeralSetupCharDB.profiles[k] or {pages={}}
 return FeralSetupCharDB.profiles[k]
end
local function actionInfo(slot)
 local f=GetActionInfo or (C_ActionBar and C_ActionBar.GetActionInfo)
 return f(slot)
end
local function spellName(id)
 if C_Spell and C_Spell.GetSpellName then return C_Spell.GetSpellName(id) end
 if GetSpellInfo then return GetSpellInfo(id) end
end
local function actionSnapshot(slot)
 local k,id,sub=actionInfo(slot)
 if not k then return {kind='empty'} end
 local d={kind=k,id=id,sub=sub}
 if k=='macro' then
  d.name,d.icon,d.body=GetMacroInfo(id)
  d.scope=id>(MAX_ACCOUNT_MACROS or 120) and 'character' or 'general'
  if not d.name and GetActionText then
   d.name=GetActionText(slot)
   if d.name then
    local i=A.findMacro(d.name)
    if i then d.name,d.icon,d.body=GetMacroInfo(i);d.scope=i>(MAX_ACCOUNT_MACROS or 120) and 'character' or 'general' end
   end
  end
 elseif k=='spell' then d.name=spellName(id) end
 return d
end
local function bindingsSnapshot()
 local t={}
 for i=1,GetNumBindings() do
  local cmd=GetBinding(i)
  if cmd and cmd~='' then
   for _,key in ipairs({GetBindingKey(cmd)}) do if key then t[key]=cmd end end
  end
 end
 return t
end
local cvarNames={'enableMouseoverCast','autoSelfCast','lockActionBars','alwaysShowActionBars'}
local function settingsSnapshot()
 local s={cvars={},modified={}}
 if GetActionBarToggles then
  local a,b,c,d=GetActionBarToggles()
  local function on(v) return v==true or v==1 or v=='1' end
  s.toggles={on(a),on(b),on(c),on(d)}
 end
 for _,k in ipairs(cvarNames) do if GetCVar then local ok,v=pcall(GetCVar,k);if ok and v~=nil then s.cvars[k]=v end end end
 if GetModifiedClick then
  for _,k in ipairs({'SELFCAST','FOCUSCAST'}) do s.modified[k]=GetModifiedClick(k) end
 end
 return s
end
local function snapshot()
 local s={version=3,actions={},bindings=bindingsSnapshot(),settings=settingsSnapshot(),time=(time and time()) or 0,pages=copy(db().pages)}
 local slots={};for i=1,120 do slots[i]=true end
 for _,page in pairs(db().pages) do for _,slot in ipairs(page) do slots[slot]=true end end
 for slot in pairs(slots) do s.actions[slot]=actionSnapshot(slot) end
 return s
end
local function baseline()
 local d=db();if not d.before then d.before=snapshot() end
end
local function savedSnapshot()
 local d=db();d.saved=snapshot()
end
local function callBool(f,...)
 if not f then return false end
 local ok,result=pcall(f,...);return ok and result~=false
end
local function setCvar(k,v)
 if not GetCVar or not SetCVar then return end
 local ok,old=pcall(GetCVar,k)
 if ok and old~=nil then pcall(SetCVar,k,v) end
end
local function setVisibility(toggles)
 if SetActionBarToggles then pcall(SetActionBarToggles,unpack(toggles)) end
 if Settings and Settings.SetValue and Settings.GetSetting then
  for i=1,4 do
   local k='PROXY_SHOW_ACTIONBAR_'..(i+1)
   if Settings.GetSetting(k) then pcall(Settings.SetValue,k,toggles[i]) end
  end
 end
 if MultiActionBar_Update then pcall(MultiActionBar_Update) end
end
local function setupSettings()
 setVisibility({true,true,true,false})
 if SetModifiedClick then
  pcall(SetModifiedClick,'SELFCAST','NONE');pcall(SetModifiedClick,'FOCUSCAST','NONE')
 end
 setCvar('enableMouseoverCast','0');setCvar('lockActionBars','1');setCvar('alwaysShowActionBars','1')
end
local function restoreSettings(s)
 if not s then return end
 if s.toggles then setVisibility(s.toggles) end
 for k,v in pairs(s.cvars or {}) do setCvar(k,v) end
 for k,v in pairs(s.modified or {}) do if SetModifiedClick then pcall(SetModifiedClick,k,v) end end
end
local function saveBindings()
 local ok=callBool(SaveBindings,2)
 if not ok then A.say('Client refused SaveBindings(2). Binding persistence is NOT confirmed.') end
 return ok
end
local function setupBindings()
 local errors={}
 local windows=IsWindowsClient and IsWindowsClient()
 if windows==nil and IsMacClient then windows=not IsMacClient() end
 local function bind(k,c)
  -- Windows has no Command bindings. Alt aliases are installed independently.
  if windows and k:match('^CMD%-') then return end
  if not callBool(SetBinding,k,c) then errors[#errors+1]=k end
 end
 local reserved={}
 -- Let the macro receive these modifiers instead of another existing action.
 for _,k in ipairs({'F','G','5','C','V','Y','8','9'}) do
  for _,mod in ipairs({'CMD-','ALT-','CTRL-','SHIFT-'}) do reserved[mod..k]=true end
 end
 for _,k in ipairs({'Q','E','T','X','6'}) do
  reserved['CTRL-'..k]=true;reserved['SHIFT-'..k]=true
 end
 -- Retire old addon keys; leave a user's unrelated replacement bindings alone.
 local retired={['CMD-R']='MULTIACTIONBAR1BUTTON9',['ALT-R']='MULTIACTIONBAR1BUTTON9',
  ['CMD-CTRL-R']='MULTIACTIONBAR1BUTTON9',['ALT-CTRL-R']='MULTIACTIONBAR1BUTTON9',
  ['CMD-SHIFT-R']='MULTIACTIONBAR1BUTTON9',['ALT-SHIFT-R']='MULTIACTIONBAR1BUTTON9',['N']='MULTIACTIONBAR2BUTTON12',['CMD-N']='MULTIACTIONBAR2BUTTON12',
  ['`']='MULTIACTIONBAR1BUTTON9',['CTRL-`']='MULTIACTIONBAR1BUTTON9',['SHIFT-`']='MULTIACTIONBAR1BUTTON9'}
 if FeralSetupCharDB and FeralSetupCharDB.leftKey then
  local k=FeralSetupCharDB.leftKey
  retired[k]='MULTIACTIONBAR1BUTTON9';retired['CTRL-'..k]='MULTIACTIONBAR1BUTTON9';retired['SHIFT-'..k]='MULTIACTIONBAR1BUTTON9'
 end
 for k,action in pairs(retired) do
  if GetBindingAction and GetBindingAction(k)==action then reserved[k]=true end
 end
 for i=1,6 do reserved['SHIFT-'..i]=true end
 for _,wheel in ipairs({'MOUSEWHEELUP','MOUSEWHEELDOWN','BUTTON3'}) do
  for _,m in ipairs({'SHIFT-','CTRL-','ALT-','CMD-'}) do reserved[m..wheel]=true end
 end
 -- Unbind action paging and old zoom keys, including secondary bindings.
 for _,cmd in ipairs({'NEXTACTIONPAGE','PREVIOUSACTIONPAGE','CAMERAZOOMIN','CAMERAZOOMOUT'}) do
  for _,k in ipairs({GetBindingKey(cmd)}) do reserved[k]=true end
 end
 for k in pairs(reserved) do bind(k,nil) end
 for k,cmd in pairs(FeralSetupLayout.bindings) do bind(k,cmd) end
 if not saveBindings() then errors[#errors+1]='SaveBindings' end
 if #errors>0 then A.say('Bindings not accepted: '..table.concat(errors,', '));return false end
 return true
end
local function restoreBindings(saved)
 local now=bindingsSnapshot()
 for k,v in pairs(now) do
  if saved[k]~=v and not callBool(SetBinding,k,nil) then return false,'could not clear '..k end
 end
 for k,v in pairs(saved) do
  if now[k]~=v and not callBool(SetBinding,k,v) then return false,'could not bind '..k end
 end
 return saveBindings()
end
local function buttonSlot(b)
 if not b then return nil end
 if b.CalculateAction then local ok,n=pcall(b.CalculateAction,b);if ok and type(n)=='number' then return n end end
 if type(b.action)=='number' then return b.action end
 if ActionButton_CalculateAction then local ok,n=pcall(ActionButton_CalculateAction,b);if ok and type(n)=='number' then return n end end
end
local function getSlots(prefix,barName)
 local result={};local bar=barName and _G[barName]
 for i=1,12 do
  local b=_G[prefix..i] or (bar and bar.actionButtons and bar.actionButtons[i])
  result[i]=buttonSlot(b)
  if not result[i] or result[i]<1 or result[i]>180 or result[i]%1~=0 then return nil,'Cannot read native '..prefix..i..'.' end
  if i>1 and result[i]~=result[1]+i-1 then return nil,'Unexpected paging in '..prefix end
 end
 return result
end
local function currentForm()
 local idx=GetShapeshiftForm and GetShapeshiftForm() or 0
 if idx==0 then return 'human' end
 local c,found=A.config()
 for _,k in ipairs({'cat','bear','travel','aquatic'}) do if found[k] and tonumber(c[k])==idx then return k end end
 return nil
end
local function currentMain()
 local kind=currentForm()
 if kind~='cat' and kind~='bear' and kind~='human' then return nil,nil,'Use Humanoid, Cat or Bear for this command.' end
 local slots,err=getSlots('ActionButton','MainActionBar')
 if not slots then return nil,nil,err end
 -- Older Classic UI may draw animal actions on BonusActionButton rather
 -- than ActionButton. Read that live page; never assume a Cat/Bear offset.
 if kind~='human' and slots[1]<=72 then
  local bonus=getSlots('BonusActionButton','BonusActionBarFrame')
  if bonus and bonus[1]>72 then slots=bonus end
 end
 local first=slots[1]
 if kind=='human' and first~=1 then return nil,nil,'Select main action page 1 in humanoid, then retry.' end
 if kind~='human' and first<=72 then return nil,nil,'Animal form is not displaying its own native bonus page. Check paging/bar addons.' end
 for other,used in pairs(db().pages) do
  if other~=kind and used[1]==first then return nil,nil,'This page was already recorded for '..other..'; refusing to overwrite it.' end
 end
 return kind,slots
end
local function spellBook()
 local book={};local count=0
 if GetNumSpellTabs and GetSpellTabInfo and GetSpellBookItemName then
  for tab=1,GetNumSpellTabs() do
   local _,_,off,n=GetSpellTabInfo(tab)
   for i=(off or 0)+1,(off or 0)+(n or 0) do
    local name=GetSpellBookItemName(i,BOOKTYPE_SPELL or 'spell')
    local typ,id
    if GetSpellBookItemInfo then typ,id=GetSpellBookItemInfo(i,BOOKTYPE_SPELL or 'spell') end
    if name and (typ==nil or typ=='SPELL') then book[name]={index=i,id=id,legacy=true};count=count+1 end
   end
  end
 elseif C_SpellBook and C_SpellBook.GetNumSpellBookSkillLines and C_SpellBook.GetSpellBookItemInfo then
  local bank=Enum and Enum.SpellBookSpellBank and Enum.SpellBookSpellBank.Player or 0
  for line=1,C_SpellBook.GetNumSpellBookSkillLines() do
   local l=C_SpellBook.GetSpellBookSkillLineInfo(line)
   if l then
    for i=l.itemIndexOffset+1,l.itemIndexOffset+l.numSpellBookItems do
     local info=C_SpellBook.GetSpellBookItemInfo(i,bank)
     local id=info and (info.spellID or info.actionID)
     local name=id and spellName(id)
     if name then book[name]={index=i,id=id,bank=bank};count=count+1 end
    end
   end
  end
 end
 return book,count
end
local function clearSlot(slot)
 if actionInfo(slot) then
  if not callBool(PickupAction,slot) then return false end
  ClearCursor()
 end
 return actionInfo(slot)==nil
end
local function pickupSpell(d,book)
 local x=d.name and book[d.name]
 if x then
  if x.legacy and PickupSpellBookItem then pcall(PickupSpellBookItem,x.index,BOOKTYPE_SPELL or 'spell')
  elseif C_SpellBook and C_SpellBook.PickupSpellBookItem then pcall(C_SpellBook.PickupSpellBookItem,x.index,x.bank) end
 end
 if not GetCursorInfo() then
  local id=(x and x.id) or d.id
  local f=PickupSpell or (C_Spell and C_Spell.PickupSpell)
  if f and id then pcall(f,id) end
 end
 return GetCursorInfo()~=nil
end
local function put(slot,d,book,bodies)
 if d.kind=='keep' then return true end
 if d.kind=='empty' then return clearSlot(slot) end
 ClearCursor()
 if d.kind=='macro' then
  local i,err=A.findMacro(d.name,d.body or (bodies and bodies[d.name]),d.scope)
  if not i then return false,err end
  if not callBool(PickupMacro,i) then return false,'PickupMacro failed: '..d.name end
 elseif d.kind=='spell' then
  if not pickupSpell(d,book) then return false,'Spell unavailable: '..tostring(d.name or d.id) end
 elseif d.kind=='item' then
  if not callBool(PickupItem,d.id) then return false,'Item unavailable: '..tostring(d.id) end
 elseif d.kind=='companion' and PickupCompanion then
  pcall(PickupCompanion,d.sub,d.id)
 elseif d.kind=='flyout' and PickupFlyout then pcall(PickupFlyout,d.id)
 else return false,'Unsupported action type: '..tostring(d.kind) end
 if not GetCursorInfo() then return false,'Nothing picked up: '..tostring(d.name or d.id) end
 local ok=callBool(PlaceAction,slot)
 ClearCursor()
 if not ok then return false,'PlaceAction refused slot '..slot end
 local actual=actionSnapshot(slot)
 if actual.kind~=d.kind then return false,'Verification failed at slot '..slot end
 if d.kind=='macro' and actual.name~=d.name then return false,'Wrong macro at slot '..slot end
 if d.kind=='spell' and d.name and actual.name and actual.name~=d.name then return false,'Wrong spell at slot '..slot end
 if d.kind=='item' and actual.id~=d.id then return false,'Wrong item at slot '..slot end
 return true
end
local function apiReady()
 for _,name in ipairs({'GetActionInfo','GetNumBindings','GetBinding','GetBindingKey','SetBinding','SaveBindings','GetCursorInfo','ClearCursor','PickupAction','PlaceAction','PickupMacro'}) do
  if not _G[name] then A.say('Missing client API: '..name..'. No layout changes made.');return false end
 end
 return true
end
local function fill(rows,slots,book,bodies)
 local bad,missing={},{}
 for i,row in ipairs(rows) do
  local d=copy(row)
  if d.kind=='spell' and not book[d.name] then
   missing[#missing+1]=d.name;d={kind='empty'}
  end
  local ok,err=put(slots[i],d,book,bodies)
  if not ok then bad[#bad+1]=err or ('Could not clear '..slots[i]) end
 end
 if #missing>0 then A.say('Not learned / not in spellbook; slots empty: '..table.concat(missing,', ')) end
 for _,e in ipairs(bad) do A.say(e) end
 return #bad==0
end
local function preflight()
 if not A.guard() or not apiReady() then return nil end
 local b,n=spellBook()
 if n==0 then A.say('Could not read your spellbook. No layout changes made.');return nil end
 return b
end
local function applySetup()
 local book=preflight();if not book then return end
 if currentForm()~='human' then A.say('Start in HUMANOID form. Click off your form, then /feralsetup setup.');return end
 local kind,main,err=currentMain();if not main then A.say(err);return end
 local fixed={}
 for _,p in ipairs({{'support','MultiBarBottomLeftButton','MultiBarBottomLeft'}, {'selfbar','MultiBarBottomRightButton','MultiBarBottomRight'}, {'utility','MultiBarRightButton','MultiBarRight'}}) do
  local slots,e=getSlots(p[2],p[3]);if not slots then A.say(e..' Enable the native extra bars first.');return end
  fixed[p[1]]=slots
 end
 baseline()
 local bodies=A.macros(true);if not bodies then A.say('Macro preparation failed; see errors above. No bars/bindings changed.');return end
 setupSettings()
 local success=setupBindings()
 for _,k in ipairs({'support','selfbar','utility'}) do
  if not fill(FeralSetupLayout.fixed[k],fixed[k],book,bodies) then success=false end
 end
 if not fill(FeralSetupLayout.main.human,main,book,bodies) then success=false end
 db().pages.human=copy(main)
 if success then
  savedSnapshot()
  A.say('Bindings, three fixed bars and Humanoid page installed (v3.5.6; Cmd/Alt aliases; Faerie Fire on Shift+R).')
  A.say('Wheel UP into Cat, then /feralsetup form. Wheel DOWN into Bear, run it again.')
  A.say('Then /feralsetup save to save a recovery snapshot and reload.')
 else A.say('Some operations failed. Backup was preserved; see messages above. /feralsetup undo reverses layout changes.') end
end
local function applyForm()
 local book=preflight();if not book then return end
 local kind,slots,err=currentMain();if not slots then A.say(err);return end
 baseline()
 local bodies=A.pageMacros(FeralSetupLayout.main[kind]);if not bodies then return end
 if fill(FeralSetupLayout.main[kind],slots,book,bodies) then
  db().pages[kind]=copy(slots);savedSnapshot()
  A.say(kind..' page filled using LIVE slots '..slots[1]..'-'..slots[12]..'.')
  A.say('After both Cat and Bear: /feralsetup save. Cat Q/R select their stealth abilities automatically.')
 end
end
local function restore(s,label)
 local book=preflight();if not book then return end
 if not s then A.say('No '..label..' snapshot on this character/talent group yet. Use /feralsetup setup.');return end
 local need={};local problems={}
 for _,d in pairs(s.actions) do
  if d.kind=='macro' then
   if not d.name or not d.body then problems[#problems+1]='Unreadable saved macro'
   else need[(d.scope or 'any')..'\001'..d.name..'\001'..d.body]=d end
  end
 end
 for _,m in pairs(need) do
  local _,err=A.ensureOne(m.name,m.body,m.icon,true,m.scope)
  if err then problems[#problems+1]=err end
 end
 if #problems>0 then
  for _,e in ipairs(problems) do A.say(e) end
  A.say('Stopped before restoring bars/bindings; macro restoration failed. See errors above.');return
 end
 local failures={}
 for slot,d in pairs(s.actions) do
  local ok,err=put(tonumber(slot),d,book)
  if not ok then failures[#failures+1]=(err or 'Could not clear')..' [slot '..slot..']' end
 end
 local ok,err=restoreBindings(s.bindings)
 if not ok then failures[#failures+1]=err or 'Could not save bindings' end
 restoreSettings(s.settings);db().pages=copy(s.pages or {})
 for _,e in ipairs(failures) do A.say(e) end
 A.say(label..' restore finished: '..#failures..' failures. No macros were deleted.')
 A.say('Use /reload now to commit. /feralsetup save only AFTER checking the restored layout.')
end
local function saveAndReload()
 if not A.guard() or not apiReady() then return end
 if not saveBindings() then return end
 savedSnapshot()
 A.say('Snapshot recorded. Reloading to write addon data to disk.')
 if ReloadUI then ReloadUI() else A.say('Type /reload now.') end
end
local function status()
 local d=db();local form=currentForm() or 'unknown';local slots=getSlots('ActionButton','MainActionBar')
 A.say('v3.5.6. Form: '..form..'; current main slots: '..(slots and (slots[1]..'-'..slots[12]) or 'unreadable'))
 local pages={};for k,v in pairs(d.pages) do pages[#pages+1]=k..' '..v[1]..'-'..v[12] end
 A.say('Recorded pages: '..(#pages>0 and table.concat(pages,', ') or 'none'))
 A.say('Saved layout: '..(d.saved and 'yes' or 'no')..'; pre-setup backup: '..(d.before and 'yes' or 'no')..'; talent group '..groupKey())
 local ac,ch=GetNumMacros()
 A.say('Macros: General '..ac..'/'..tostring(MAX_ACCOUNT_MACROS or 120)..'; Character '..ch..'/'..tostring(MAX_CHARACTER_MACROS or 18)..'. New macros use General.')
 A.say('setup/install/update replace same-name guide macros. form only places the current page.')
 A.say('Only explicit commands change the layout. Nothing is auto-restored on login.')
end
local function leftKey(k)
 if not A.guard() then return end
 if k=='' then A.say('Usage: /feralsetup leftkey ` (or the actual key immediately left of 1).');return end
 k=k:upper()
 if k:find('%s') or k:find('CMD') or k:find('CTRL') or k:find('SHIFT') then A.say('Use a single unmodified key.');return end
 baseline()
 if callBool(SetBinding,k,'MULTIACTIONBAR1BUTTON9') then
  callBool(SetBinding,'CTRL-'..k,nil);callBool(SetBinding,'SHIFT-'..k,nil)
  FeralSetupCharDB.leftKey=k;saveBindings();A.say('Faerie Fire uses '..k..'. Run /feralsetup save after final checks.')
 else A.say('The client did not accept that key. Bind Bottom Left button 9 manually.') end
end
SLASH_FERALSETUP1='/feralsetup'
SLASH_FERALSETUP2='/fs'
SlashCmdList.FERALSETUP=function(msg)
 local cmd,rest=(msg or ''):match('^%s*(%S*)%s*(.-)%s*$');cmd=cmd:lower()
 if cmd=='setup' then applySetup()
 elseif cmd=='form' then applyForm()
 elseif cmd=='bindings' then
  if A.guard() then baseline();if setupBindings() then A.say('Bindings updated; bars unchanged. /feralsetup save after checking.') end end
 elseif cmd=='save' or cmd=='backup' then saveAndReload()
 elseif cmd=='restore' then restore(db().saved,'saved layout')
 elseif cmd=='undo' then restore(db().before,'pre-setup')
 elseif cmd=='status' then status()
 elseif cmd=='guide' then A.guide(rest)
 elseif cmd=='leftkey' then leftKey(rest)
 elseif cmd=='install' or cmd=='update' then
  if A.guard() and A.macros(true) then A.say('Guide macros installed/replaced. /feralsetup setup also places bars and bindings.') end
 else
  A.say('/feralsetup setup: replace same-name guide macros + current guide layout (start humanoid).')
  A.say('/feralsetup bindings: apply keybindings only; leave bars unchanged.')
  A.say('/feralsetup form: place current page only; keep existing macro bodies.')
  A.say('/feralsetup save: snapshot + reload. /feralsetup restore: recover saved layout.')
  A.say('/feralsetup undo: pre-setup layout. /feralsetup status: diagnostics.')
  A.say('/feralsetup guide: current route, quests and training. guide on|off: level-up reminders.')
 end
end
