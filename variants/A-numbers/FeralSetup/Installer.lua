-- Macro engine. User-requested, out-of-combat setup only; no spell execution.
FeralSetup={}
local A=FeralSetup
function A.say(s) print('|cff6bd6c9FeralSetup:|r '..s) end
function A.guard()
 if InCombatLockdown and InCombatLockdown() then A.say('Leave combat first. Nothing changed.');return false end
 local _,class=UnitClass('player')
 if class~='DRUID' then A.say('Use this on your Druid. Nothing changed.');return false end
 if GetCursorInfo and GetCursorInfo() then A.say('Put down the item/spell on your cursor first.');return false end
 return true
end
function A.text(s,c) return (s:gsub('{{(%w+)}}',function(k) return tostring(c[k] or '') end)) end
function A.spellBook()
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
     local name=id and ((C_Spell and C_Spell.GetSpellName and C_Spell.GetSpellName(id)) or (GetSpellInfo and GetSpellInfo(id)))
     local isSpell=info and (info.itemType==nil or info.itemType=='SPELL' or (Enum and Enum.SpellBookItemType and info.itemType==Enum.SpellBookItemType.Spell))
     if name and isSpell then book[name]={index=i,id=id,bank=bank};count=count+1 end
    end
   end
  end
 end
 return book,count
end

function A.config()
 local c={};for k,v in pairs(FeralSetupDefaults) do c[k]=v end
 local ids={[768]='cat',[5487]='bear',[9634]='bear',[1066]='aquatic',[783]='travel'}
 local names={['Cat Form']='cat',['Bear Form']='bear',['Dire Bear Form']='bear',['Aquatic Form']='aquatic',['Travel Form']='travel'}
 local found={}
 if GetNumShapeshiftForms and GetShapeshiftFormInfo then
  for i=1,GetNumShapeshiftForms() do
   local _,n,_,id=GetShapeshiftFormInfo(i);local k=ids[id] or (type(n)=='string' and names[n])
   if k then c[k]=tostring(i);found[k]=true end
   if id==9634 or n=='Dire Bear Form' then c.bearSpell='Dire Bear Form' end
  end
 end
 local known=IsPlayerSpell or IsSpellKnown or (C_SpellBook and C_SpellBook.IsSpellKnown)
 if known then
  if known(9634) then c.bearSpell='Dire Bear Form' end
  if known(2893) then c.poison='Abolish Poison' end
 end
 local book=A.spellBook()
 c.hasRavage=book.Ravage~=nil
 c.hasPounce=book.Pounce~=nil
 return c,found
end
function A.renderMacro(m,c)
 local body=m.body
 if (m.name=="Cat Rear" and not c.hasRavage) or (m.name=="Cat Q" and not c.hasPounce) then
  body=FeralSetupUnlearnedMacros[m.name]
 end
 return A.text(body,c)
end
-- General macros are the default pool. Existing character macros are recognised.
-- Resolve names deterministically: General first, then this character; lowest index.
function A.macroList()
 local t={};local ac,ch=GetNumMacros();local base=MAX_ACCOUNT_MACROS or 120
 for _,range in ipairs({{1,ac},{base+1,base+ch}}) do
  for i=range[1],range[2] do
   local n,icon,body=GetMacroInfo(i)
   if n then t[#t+1]={index=i,name=n,icon=icon,scope=i>base and 'character' or 'general',body=body or (GetMacroBody and GetMacroBody(i)) or ''} end
  end
 end
 return t,ac,ch
end
function A.findMacro(name,body,scope)
 local collision=false
 for _,m in ipairs(A.macroList()) do
  if m.name==name and (not scope or m.scope==scope) then
   if body==nil or body==m.body then return m.index end
   collision=true
  end
 end
 return nil,collision and ('different existing macro: '..name) or ('missing macro: '..name)
end
local function backupDefinition(m)
 FeralSetupCharDB=FeralSetupCharDB or {}
 FeralSetupCharDB.macroReplacements=FeralSetupCharDB.macroReplacements or {}
 local history=FeralSetupCharDB.macroReplacements
 -- Keep unique replaced definitions, including macros not currently on a bar.
 for _,old in ipairs(history) do
  if old.name==m.name and old.body==m.body and old.scope==m.scope then return end
 end
 history[#history+1]={name=m.name,body=m.body,icon=m.icon,scope=m.scope,time=time and time() or 0}
end
-- overwrite=true deliberately replaces all visible same-name definitions in scope.
-- This is called only from explicit installation/update/recovery commands.
function A.ensureOne(name,body,icon,overwrite,scope)
 if #name>16 or #body>255 then return nil,'macro too long: '..name end
 local existing={};local list,ac,ch=A.macroList()
 for _,m in ipairs(list) do
  if m.name==name and (not scope or m.scope==scope) then existing[#existing+1]=m end
 end
 FeralSetupDB=FeralSetupDB or {};FeralSetupDB.owned=FeralSetupDB.owned or {}
 if #existing>0 then
  if not overwrite then return A.findMacro(name,body,scope) end
  if not EditMacro then return nil,'EditMacro API unavailable: '..name end
  -- Editing the body without changing the name does not reorder the macro list.
  for _,m in ipairs(existing) do
   if m.body~=body then
    backupDefinition(m)
    local ok,res=pcall(EditMacro,m.index,name,icon or 134400,body)
    if not ok then return nil,'could not replace '..name..': '..tostring(res) end
   end
  end
  -- Do not mistake an existing matching duplicate for successful replacement.
  for _,m in ipairs(A.macroList()) do
   if m.name==name and (not scope or m.scope==scope) and m.body~=body then
    return nil,'client did not replace '..name..' ('..m.scope..')'
   end
  end
  local i,err=A.findMacro(name,body,scope)
  if i then FeralSetupDB.owned[name]=body end
  return i,err
 end
 local perCharacter=scope=='character'
 if perCharacter then
  if ch>=(MAX_CHARACTER_MACROS or 18) then return nil,'Character Macros are full: '..name end
 elseif ac>=(MAX_ACCOUNT_MACROS or 120) then return nil,'General Macros are full: '..name end
 if not CreateMacro then return nil,'CreateMacro API unavailable: '..name end
 local ok,res=pcall(CreateMacro,name,icon or 134400,body,perCharacter)
 if not ok then return nil,'could not create '..name..': '..tostring(res) end
 local i=A.findMacro(name,body,perCharacter and 'character' or 'general')
 if not i then return nil,'could not create macro: '..name end
 FeralSetupDB.owned[name]=body
 return i
end
function A.macros(overwrite)
 local c=A.config();local errors={};local bodies={}
 for _,m in ipairs(FeralSetupMacros) do
  local body=A.renderMacro(m,c);bodies[m.name]=body
  local _,err=A.ensureOne(m.name,body,134400,overwrite)
  if err then errors[#errors+1]=err end
 end
 if #errors>0 then for _,e in ipairs(errors) do A.say(e) end;return nil end
 return bodies
end
-- Form placement is NOT a reinstall. Reuse existing bodies, even if edited;
-- create only missing macros that the current page actually requires.
function A.pageMacros(rows)
 local templates={};for _,m in ipairs(FeralSetupMacros) do templates[m.name]=m end
 local c=A.config();local bodies={};local errors={}
 for _,row in ipairs(rows) do
  if row.kind=='macro' and bodies[row.name]==nil then
   local i,err=A.findMacro(row.name)
   if not i then
    local m=templates[row.name]
    if m then i,err=A.ensureOne(m.name,A.renderMacro(m,c),134400,false)
    else err='No template for missing macro: '..row.name end
   end
   if i then
    local _,_,body=GetMacroInfo(i)
    bodies[row.name]=body or (GetMacroBody and GetMacroBody(i)) or ''
   else errors[#errors+1]=err end
  end
 end
 if #errors>0 then for _,e in ipairs(errors) do A.say(e) end;return nil end
 return bodies
end

-- Native Forever meter enable/disable, using the same CVar as Advanced Options.
BINDING_NAME_FERALSETUP_DAMAGE_METER='Toggle damage meter'
function A.toggleDamageMeter()
 local get=(C_CVar and C_CVar.GetCVar) or GetCVar
 local set=(C_CVar and C_CVar.SetCVar) or SetCVar
 if not get or not set then A.say('Damage meter settings unavailable in this client.');return end
 local value=get('damageMeterEnabled')
 if value==nil then A.say('Native damage meter unavailable in this client.');return end
 local enabled=tostring(value)=='1'
 set('damageMeterEnabled',enabled and '0' or '1')
 A.say(enabled and 'Damage meter disabled.' or 'Damage meter enabled. Its visibility follows your meter settings (use Always to see it outside combat).')
end
