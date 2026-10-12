## Description

Fork of [NeverCrisis](https://github.com/DelistedCloud/NeverCrisis). The core files are unmodified and downloaded directly from the original [NeverCrisis Releases](https://github.com/DelistedCloud/NeverCrisis/releases). NeverCrisis there is intended for Windows installations. What is provided here is merely an additional wrapper/script to run the offline server on Linux. I am not a programming expert; these scripts were created with the help of Gemini AI.

## USAGE

Personal notes in case I have uninstalled the game and want to play it again after some time.

Based on the latest workaround discussed in several [issues](https://github.com/DelistedCloud/NeverCrisis/issues/3).
Someone shared a guide in PDF format; essentially, the files downloaded from the `NeverCrisis` release are placed in the game's installation folder, except for the `save` folder which is placed in a different location. For Linux, this location is inside the Steam prefix directory:
`../../compatdata/2484110/pfx/drive_c/users/steamuser/Documents/My Games/FF7EC/Steam`.

In that discussion, there are also instructions for downloading game data. For Linux, you can use `steamdepotdownloader` or `steamdepotdowanloadergui`. However, it seems to require a Steam login and only works for those who previously played the official online game before EOS.

Requires `libfaketime`: 
> sudo pacman -S libfaketime

Server port permissions (port 443) only needed once: 
> sudo sysctl -w net.ipv4.ip_unprivileged_port_start=443

Editing hosts:
```
sudo sh -c 'cat << "EOF" >> /etc/hosts  
   
# FF7EC Offline Server  
127.0.0.1 game-q74z3cyn.app.gl.ffviiec.com  
127.0.0.1 resources-api-c9ps53g2.app.gl.ffviiec.com  
127.0.0.1 client-masterdata-c9ps53g2.app.gl.ffviiec.com  
127.0.0.1 chat-pd381ne.app.gl.ffviiec.com  
EOF'  
``` 

There are 2 files copied into the FF7EC game directory:
- start_offline.sh
- server_args.txt

**start_offline.sh** is the script to run the offline server. The paths listed inside are based on my PC when it was created, so you should check and possibly adjust them as follows:
- Around line 11: STEAM_ROOT: path to the Steam directory. Default installation is usually at `~/.local/share/Steam`. It typically contains folders like `compatibilitytools.d`, `steam`, `steamapps`, `ubuntu12_32`, `ubuntu12_64`, `linux32`, `linux64`, etc.
- Around line 12: COMPAT_DATA: path to the game's compatdata/steam prefix directory.
- Around line 13: PROTON_BIN: path to the Proton directory. Currently using Proton Experimental.
- Around line 72: to change the date. The game reached EOS on October 7, 2026; there was a file update change on October 5, 2026, and it is currently set to October 4, 2026. This might be needed to manipulate login rewards; dates prior to October 5 are recommended.

**server_args.txt** is a file to pass additional options such as `--give item...` or `--reopen-events`. These options will automatically be included when executing `./start_offline.sh`. The item ID list can be found in the `items.txt` file included with the original `NeverCrisis` release.

To launch the game by executing `start_offline.sh`. Make sure your terminal is inside the directory where this script is located:
> ./start_offline.sh


## Gameplay Notes, Issues & Workarounds
Obviously, not everything works as it did before EOS. Some issues are already mentioned on the `NeverCrisis` page. Below are additional ones I encountered. Most workarounds rely on the `--give item` option from `NeverCrisis`.

- Even though it is offline, if connected to the internet, it gets stuck/blank on the launcher after "click to start". You can only enter if you disconnect all network connections (there is a brief blank screen).
- In the original game, duplicate weapons gave 200 weapon parts (from gacha or currency exchange). Now it only gives 1. So it is recommended to add character weapon parts via `--give item`.
- Unlocking costumes/gear seems to be consolidated in exchange > `gear 3rd anniversary gear` voucher. So get the vouchers via `--give` as well. Some costumes like Aerith Chocobo or Zack Swimsuit can be exchanged from events.
- Event weapons are also consolidated in the latest Sephiroth event. So get `sephiroth certificate` via `--give item` and exchange them on the event page.
- Memoria does not drop from completing events. But they can still be obtained from exchange > medal > co-op medal (offline does not support co-op, so get them via the `--give` option).
- Elemental and ruin materia are consolidated in exchange > enhancement > 5* materia.
- Leveling up materia can only be done using other materia.

## Unresolved Issues (No Workaround Yet)
- Cannot start summon quests/missions.
- Cannot unlock character TUNING rolestream even if all missions are fulfilled. The rolestream tree itself still works.
- Cannot open Chocobo Farm, stuck on loading stream.
- `Umbral Sword` is reportedly only from the 1.5 anniversary login event, and other than that, there is no known way to obtain it.

## What else?
As mentioned at the beginning, I am not an expert. Therefore, I will not be able to address issues. Sorry.
