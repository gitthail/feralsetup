-- Agreed 15-30 Alliance route from Feral_Leveling_and_Professions.html.
-- Private chat reminders only; never changes macros, bindings or action bars.
local A=FeralSetup
local route={
 {level=15,area='Darkshore - Auberdine',
  quests='Buzzbox; Washed Ashore / Beached Sea Creature; The Red Crystal; How Big a Threat?; The Cliffspring River.',
  note='Stack nearby objectives. If quests run dry, use suitable Westfall / Loch Modan / Redridge leftovers.'},
 {level=20,area="Ashenvale - Maestra's Post / Astranaar",
  quests="Bathran's Hair -> Orendil's Cure; Elune's Tear; early Raene's Cleansing; The Zoram Strand; The Ancient Statuette.",
  note="First complete The Great Cat Spirit for Cat Form. Get Astranaar's flight path; leave harder chain steps for later."},
 {level=23,area='Wetlands - Menethil Harbor',
  quests="Claws from the Deep; Young Crocolisk Skins; The Greenwarden -> Tramping Paws; early Ormer's Revenge; Digging Through the Ooze.",
  note="Return to Auberdine, boat to Menethil, and get its flight path. Combine excavation and swamp objectives."},
 {level=25,area='Duskwood - Darkshire',
  quests='The Night Watch; Raven Hill; Wolves at Our Heels; Eight-Legged Menaces; The Totem of Infliction.',
  note='Establish connecting flight paths. Batch cemetery objectives; Redridge leftovers are an alternative. Skip elite finales without a ready group.'},
 {level=27,area='Wetlands return / Ashenvale if needed',
  quests="The Third Fleet / The Cursed Crew; War Banners; later Ormer's Revenge; Uncovering the Past. Ashenvale: later Raene's Cleansing; An Aggressive Defense; Culling the Threat.",
  note='Finish productive Duskwood clusters first. Avoid another boat trip while easy local quests remain.'},
}
local training={
 [16]='Swipe; Rejuvenation upgrade; Aquatic quest available (combine travel with your route).',
 [18]='Maul upgrade; Faerie Fire; Hibernate; Roots / Regrowth upgrades.',
 [20]='The Great Cat Spirit; Omen of Clarity; Healing Touch / Mark upgrades; Rebirth. After learning Cat, update macros and place the Cat page out of combat.',
 [22]='Rejuvenation upgrade on a convenient trainer visit.',
 [24]='Rake; Ferocious Bite; Remove Curse; Swipe / Regrowth / Thorns upgrades.',
 [26]='Dash; Abolish Poison; Maul / Healing Touch upgrades.',
 [28]='Claw and Rip upgrades; useful healing / control upgrades.',
 [30]='Travel Form; Bash upgrade; frequently used support upgrades.',
}
local function eligible()
 local _,class=UnitClass('player')
 return class=='DRUID' and UnitFactionGroup('player')=='Alliance'
end
local function enabled()
 return not FeralSetupCharDB or FeralSetupCharDB.levelingReminders~=false
end
local function show(level,details)
 if not eligible() then
  if details then A.say('This guide is for your Alliance Druid (levels 15-30).') end
  return
 end
 level=tonumber(level)
 if not level or level<1 then return end
 if level<15 then
  if details then A.say('The agreed guide starts at level 15: Darkshore - Auberdine.') end
  return
 end
 if level>=30 then
  if details or level==30 then
   A.say('Level '..level..': the agreed route ends at 30. No next area is planned yet.')
   if level==30 then A.say('Train: '..training[30]) end
  end
  return
 end
 local index=1
 for i,step in ipairs(route) do if level>=step.level then index=i end end
 local step,nextStep=route[index],route[index+1]
 local nextText=nextStep and (nextStep.area..' at '..nextStep.level) or 'finish to 30; no later area planned'
 A.say('Level '..level..' | Recommended now: '..step.area..' | Next: '..nextText..'.')
 if training[level] then A.say('Train: '..training[level]) end
 if details then
  A.say('Quests: '..step.quests)
  A.say(step.note)
  for n=level+1,30 do
   if training[n] then A.say('Next trainer stop ('..n..'): '..training[n]);break end
  end
  A.say('Flexible checkpoints, not quest tracking. Reminders: '..(enabled() and 'on' or 'off')..'. /feralsetup guide on|off')
 end
end
function A.guide(option)
 option=(option or ''):lower()
 if option=='on' or option=='off' then
  FeralSetupCharDB=FeralSetupCharDB or {}
  FeralSetupCharDB.levelingReminders=option=='on'
  A.say('Level-up reminders '..option..' for this character.')
 elseif option=='' then show(UnitLevel('player'),true)
 else A.say('Usage: /feralsetup guide [on|off]') end
end
local frame=CreateFrame('Frame')
frame:RegisterEvent('PLAYER_LEVEL_UP')
frame:SetScript('OnEvent',function(_,_,newLevel)
 -- UnitLevel can still report the old level during PLAYER_LEVEL_UP.
 if enabled() then show(newLevel,false) end
end)
