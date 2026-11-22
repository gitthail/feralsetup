-- Macro templates; all rendered bodies must fit 255 characters.
FeralSetupDefaults={
  ["bandage"]="Your current bandage",
  ["bear"]="1",
  ["poison"]="Cure Poison",
  ["travel"]="4",
  ["bearCharge"]="Feral Charge",
  ["cat"]="3",
  ["aquatic"]="2",
  ["interface"]="16001",
  ["trinket"]="13",
  ["bearSpell"]="Bear Form"
}
FeralSetupMacros={
  {
    ["name"]="Rejuvenation",
    ["body"]="#showtooltip\n/stopmacro [mod:shift,nomod:cmd/alt][mod:ctrl,nomod:cmd/alt,@mouseover,nohelp][mod:ctrl,nomod:cmd/alt,@mouseover,dead]\n/stopattack\n/cancelform\n/cast [mod:cmd/alt,@player][@mouseover,help,nodead][help,nodead][@player] Rejuvenation"
  },
  {
    ["name"]="Regrowth",
    ["body"]="#showtooltip\n/stopmacro [mod:shift,nomod:cmd/alt][mod:ctrl,nomod:cmd/alt,@mouseover,nohelp][mod:ctrl,nomod:cmd/alt,@mouseover,dead]\n/stopattack\n/cancelform\n/cast [mod:cmd/alt,@player][@mouseover,help,nodead][help,nodead][@player] Regrowth"
  },
  {
    ["name"]="Healing Touch",
    ["body"]="#showtooltip\n/stopmacro [mod:shift,nomod:cmd/alt][mod:ctrl,nomod:cmd/alt,@mouseover,nohelp][mod:ctrl,nomod:cmd/alt,@mouseover,dead]\n/stopattack\n/cancelform\n/cast [mod:cmd/alt,@player][@mouseover,help,nodead][help,nodead][@player] Healing Touch"
  },
  {
    ["name"]="Remove Curse",
    ["body"]="#showtooltip\n/stopmacro [mod:shift,nomod:cmd/alt][mod:ctrl,nomod:cmd/alt,@mouseover,nohelp][mod:ctrl,nomod:cmd/alt,@mouseover,dead]\n/stopattack\n/cancelform\n/cast [mod:cmd/alt,@player][@mouseover,help,nodead][help,nodead][@player] Remove Curse"
  },
  {
    ["name"]="Poison Cleanse",
    ["body"]="#showtooltip\n/stopmacro [mod:shift,nomod:cmd/alt][mod:ctrl,nomod:cmd/alt,@mouseover,nohelp][mod:ctrl,nomod:cmd/alt,@mouseover,dead]\n/stopattack\n/cancelform\n/cast [mod:cmd/alt,@player][@mouseover,help,nodead][help,nodead][@player] {{poison}}"
  },
  {
    ["name"]="Innervate",
    ["body"]="#showtooltip\n/stopmacro [mod:shift,nomod:cmd/alt][mod:ctrl,nomod:cmd/alt,@mouseover,nohelp][mod:ctrl,nomod:cmd/alt,@mouseover,dead]\n/stopattack\n/cancelform\n/cast [mod:cmd/alt,@player][@mouseover,help,nodead][help,nodead][@player] Innervate"
  },
  {
    ["name"]="Thorns",
    ["body"]="#showtooltip\n/stopmacro [mod:shift,nomod:cmd/alt][mod:ctrl,nomod:cmd/alt,@mouseover,nohelp][mod:ctrl,nomod:cmd/alt,@mouseover,dead]\n/stopattack\n/cancelform\n/cast [mod:cmd/alt,@player][@mouseover,help,nodead][help,nodead][@player] Thorns"
  },
  {
    ["name"]="Pounce",
    ["body"]="#showtooltip Pounce\n/cast [mod:shift,@focus,harm,nodead][mod:ctrl,@mouseover,harm,nodead][nomod,harm,nodead] Pounce"
  },
  {
    ["name"]="Bash",
    ["body"]="#showtooltip Bash\n/cast [mod:shift,@focus,harm,nodead][mod:ctrl,@mouseover,harm,nodead][nomod,harm,nodead] Bash"
  },
  {
    ["name"]="Cat Charge",
    ["body"]="#showtooltip Feral Charge (Cat)\n/cast [mod:shift,@focus,harm,nodead][mod:ctrl,@mouseover,harm,nodead][nomod,harm,nodead] Feral Charge (Cat)"
  },
  {
    ["name"]="Bear Charge",
    ["body"]="#showtooltip {{bearCharge}}\n/cast [mod:shift,@focus,harm,nodead][mod:ctrl,@mouseover,harm,nodead][nomod,harm,nodead] {{bearCharge}}"
  },
  {
    ["name"]="Faerie Fire",
    ["body"]="#showtooltip Faerie Fire\n/cast [mod:ctrl,@mouseover,harm,nodead][nomod:ctrl,harm,nodead] Faerie Fire"
  },
  {
    ["name"]="Growl",
    ["body"]="#showtooltip Growl\n/cast [mod:shift,@focus,harm,nodead][mod:ctrl,@mouseover,harm,nodead][nomod,harm,nodead] Growl"
  },
  {
    ["name"]="Roots",
    ["body"]="#showtooltip Entangling Roots\n/stopattack\n/cancelform [mod:shift,@focus,harm,nodead][mod:ctrl,@mouseover,harm,nodead][nomod,harm,nodead]\n/cast [mod:shift,@focus,harm,nodead][mod:ctrl,@mouseover,harm,nodead][nomod,harm,nodead] Entangling Roots"
  },
  {
    ["name"]="Hibernate",
    ["body"]="#showtooltip Hibernate\n/stopattack\n/cancelform [mod:shift,@focus,harm,nodead][mod:ctrl,@mouseover,harm,nodead][nomod,harm,nodead]\n/cast [mod:shift,@focus,harm,nodead][mod:ctrl,@mouseover,harm,nodead][nomod,harm,nodead] Hibernate"
  },
  {
    ["name"]="Moonfire",
    ["body"]="#showtooltip Moonfire\n/cancelform [harm,nodead]\n/cast [harm,nodead] Moonfire"
  },
  {
    ["name"]="Rebirth",
    ["body"]="#showtooltip Rebirth\n/stopattack\n/cancelform [@mouseover,help,dead][help,dead]\n/cast [@mouseover,help,dead][help,dead] Rebirth"
  },
  {
    ["name"]="Tranquility",
    ["body"]="#showtooltip Tranquility\n/stopattack\n/cancelform\n/cast Tranquility"
  },
  {
    ["name"]="Prowl",
    ["body"]="#showtooltip Prowl\n/cast [form:{{cat}}] Prowl"
  },
  {
    ["name"]="Maul",
    ["body"]="#showtooltip Maul\n/cast !Maul\n/startattack [harm,nodead]"
  },
  {
    ["name"]="Barkskin",
    ["body"]="#showtooltip Barkskin\n/stopcasting\n/cast Barkskin"
  },
  {
    ["name"]="Nature's Grasp",
    ["body"]="#showtooltip Nature's Grasp\n/stopcasting\n/stopattack\n/cast Nature's Grasp"
  },
  {
    ["name"]="Shadowmeld",
    ["body"]="#showtooltip Shadowmeld\n/stopcasting\n/stopattack\n/cast Shadowmeld"
  },
  {
    ["name"]="PvP Trinket",
    ["body"]="#showtooltip {{trinket}}\n/stopcasting\n/use {{trinket}}"
  },
  {
    ["name"]="Cat Form",
    ["body"]="#showtooltip Cat Form\n/stopcasting\n/cast [mod:cmd/alt][noform:{{cat}}] Cat Form"
  },
  {
    ["name"]="Bear Form",
    ["body"]="#showtooltip {{bearSpell}}\n/stopcasting\n/cast [mod:cmd/alt][noform:{{bear}}] {{bearSpell}}"
  },
  {
    ["name"]="Travel Forms",
    ["body"]="#showtooltip\n/stopcasting\n/cast [swimming,noform:{{aquatic}}] Aquatic Form; [noswimming,outdoors,noform:{{travel}}] Travel Form"
  },
  {
    ["name"]="Leave Form",
    ["body"]="/stopcasting\n/stopattack\n/cancelform"
  },
  {
    ["name"]="Set Focus",
    ["body"]="/clearfocus [mod:cmd/alt]\n/stopmacro [mod:cmd/alt]\n/focus [@mouseover,exists,nodead][exists,nodead]"
  },
  {
    ["name"]="Mark of the Wild",
    ["body"]="#showtooltip\n/stopmacro [mod:shift,nomod:cmd/alt][mod:ctrl,nomod:cmd/alt,@mouseover,nohelp][mod:ctrl,nomod:cmd/alt,@mouseover,dead]\n/stopattack\n/cancelform\n/cast [mod:cmd/alt,@player][@mouseover,help,nodead][help,nodead][@player] Mark of the Wild"
  },
  {
    ["name"]="Cat Rear",
    ["body"]="#showtooltip\n/cast [form:{{cat}},stealth] Ravage; [form:{{cat}}] Shred"
  },
  {
    ["name"]="Cat Q",
    ["body"]="#showtooltip\n/cast [form:{{cat}},mod:alt,nomod:cmd/ctrl/shift] Dash; [form:{{cat}},stealth,mod:shift,@focus,harm,nodead][form:{{cat}},stealth,mod:ctrl,@mouseover,harm,nodead][form:{{cat}},stealth,nomod,harm,nodead] Pounce; [form:{{cat}},nostealth,nomod] Dash"
  }
}
