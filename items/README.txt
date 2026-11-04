# Ids for --give, one list per kind of thing.
#
#   weapon-parts.txt           weapon parts and Mako Gems
#   tickets-medals-events.txt  draw tickets, medals, vouchers, event exchange items
#   materials.txt              character, summon and role pieces, materia and weapon materials, brands
#   chocobo.txt                chocobo expedition finds and medals
#   misc.txt                   everything else: gil, keys, stamina, item boxes, passes, Highwind
#   weapons.txt                weapons
#   costumes.txt               costumes
#   wallpapers.txt             home wallpapers
#   memoria.txt                memoria
#
# To give yourself some, start the server from a command prompt in the game
# folder with --give, once per thing, as many as you like:
#
#   FF7ECServer.exe --give item=9003=100 --give item=10012=30
#
# The number after "item=" is the id in the first column of any of the first
# five lists; the last number is how many. Short names exist for the common
# currencies, no id needed:
#
#   FF7ECServer.exe --give crystals=3000 --give red_crystals=300 --give gil=20000
#   --give stamina=200 --give chocobo_medals=50 --give weapon_medals=500
#   --give crisis_medals=50 --give dungeon_keys=5 --give gear_vouchers=3
#   --give memory_vouchers=3 --give parts=100
#
# Names the game gives to several items - a Victory Draw Ticket for every
# banner, the same medal in every run of an event - carry the event and the
# month it opened, so you can tell which is which.
#
# --give weapon=ID hands a weapon over at its highest rarity; --give
# weapon=ID=11 gives eleven copies, the ten spares paid as the weapon's parts
# the way a drawn duplicate is - what the 1.5 anniversary's Umbral Blade gift
# was:
#
#   FF7ECServer.exe --give weapon=1046=11
#
# --give costume=ID adds a costume to the character's wardrobe - the
# crossover outfits too, which no voucher or banner offers any more:
#
#   FF7ECServer.exe --give costume=1018
#
# --give wallpaper=ID and --give memoria=ID add one of those; "all" in place
# of the id adds every one the game has, and costumes take all:NAME for one
# character's. One already owned is left alone:
#
#   FF7ECServer.exe --give wallpaper=20003 --give memoria=all
#   FF7ECServer.exe --give costume=all:Cloud --give "costume=all:Red XIII"
