[Indonesian Version](README.md)

Just personal notes in case I've uninstalled the game and happen to want to play again after some time.

## Description

Fork of [NeverCrisis](https://github.com/DelistedCloud/NeverCrisis). What is provided here is merely an additional wrapper/script to run the offline server on Linux. I am not a programming expert; this script was created with the help of Gemini AI.

For the offline server itself, you can use the following:
1. [NeverCrisis Delisted Cloud](https://github.com/DelistedCloud/NeverCrisis) - this is the main repository.
2. [NeverCrisis ShadowMPo](https://github.com/ShadowMPo/NeverCrisis) - an active fork of Delisted Cloud, featuring fixes and updates over the Delisted Cloud version.

## USAGE

Based on the latest workaround from several discussion [issues](https://github.com/DelistedCloud/NeverCrisis/issues/3).
Someone shared a guide in the form of a [PDF file](NeverCrisis-Setup-Guide-V2.1.pdf); essentially, the files downloaded from the `NeverCrisis` release are placed in the game's installation folder, except for the `save` folder which is placed in a different location. For the Linux version, this location is inside the Steam prefix directory:
`../../compatdata/2484110/pfx/drive_c/users/steamuser/Documents/My Games/FF7EC/Steam/NUMBERID`. `NUMBERID` is the ID number from the `ff7ec_account_id.txt` file.

In that discussion, there are also instructions for downloading the game data. For the Linux version, you can use `steamdepotdownloader` or `steamdepotdowanloadergui`. However, it seems to require a Steam login and only works for those who previously played the official online game before EOS.

Requires `libfaketime` if you want to manipulate the date; mandatory if using the `DelistedCloud` version, optional if using the `ShadowMPo` version: 
> sudo pacman -S libfaketime

Server permissions (port 443) are only needed once: 
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
- [start_offline.sh](start_offline.sh)
- [server_args.txt](server_args.txt)

**start_offline.sh** is the script to run the offline server. The paths listed inside are based on my PC when it was created, so you should check and possibly adjust them as follows:
- Around line 11: STEAM_ROOT: path to the Steam directory. Default installation is usually at `~/.local/share/Steam`. It typically contains folders like `compatibilitytools.d`, `steam`, `steamapps`, `ubuntu12_32`, `ubuntu12_64`, `linux32`, `linux64`, etc.
- Around line 12: COMPAT_DATA: path to the game's compatdata/steam prefix directory.
- Around line 13: PROTON_BIN: path to the Proton directory. Currently using Proton Experimental.
- If using the `ShadowMPo` version, the EOS date is already fixed, so changing the date is not required. Around line 59 to line 94 can be disabled by commenting them out (adding `#` to each line).
- If using the `Delisted Cloud` version, around line 72: to change the date. The game reached EOS on October 7, 2026, and there was a file update change on October 5, 2026; it is currently set to October 4, 2026. BTW, time manipulation is useful in both `Delisted Cloud` and `ShadowMPo` to manipulate login rewards from specific events or open the Gratitude Event gacha banner if set to July 29, 2026. There are weapons I noticed that don't exist in exchange vouchers but are available in this Gratitude gacha, such as Cloud's umbrella sword/`NobleParasol` or Tifa's `Sabin Claw`. Or you can try experimenting with even older dates.

**server_args.txt** is a file for passing additional options such as `--give item...` or `--reopen-events`. These options will automatically be included when executing `./start_offline.sh`. The item ID list can be found inside the `items.txt` file included with the original `NeverCrisis` release.

To launch the game by executing `start_offline.sh`. Make sure your terminal is inside the directory where this script is located:
> ./start_offline.sh

## What else?
As mentioned earlier, I am not an expert. Therefore, I will not be able to respond to issues. Sorry.
