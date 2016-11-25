#!/bin/bash

TEMP_STEAM_PASSWORD=$( dialog --stdout --title 'Confirmation' --passwordbox "Please confirm your steam's password" 10 50)
TEMP_STEAM_USERNAME=$( cat /tmp/chimera_os/steam_username.txt )
TEMP_STEAM_GAME_ID=$( cat /tmp/chimera_os/temp_gameid.txt )
TEMP_STEAM_GAME_NAME=$( cat /tmp/chimera_os/temp_gamename.txt )
TEMP_STEAM_GAME_PLAT=$( cat /tmp/chimera_os/temp_platforms.txt )

if [[ $TEMP_STEAM_PASSWORD == '' ]]; then
    echo "[ERROR]: You just canceled the operation or didn't type anything"
    exit 1
fi
clear

#removing temp files
sudo rm /tmp/chimera_os/temp_gameid.txt
sudo rm /tmp/chimera_os/temp_gamename.txt
sudo rm /tmp/chimera_os/temp_platforms.txt

#Checking game's platform
if [ "$TEMP_STEAM_GAME_PLAT" = "Linux" ]; then
	echo "We are not working with linux yet"
else
	echo "Connecting to Steam's Database..."
	~/steamcmd/steamcmd.sh +@sSteamCmdForcePlatformType windows \
	+login $TEMP_STEAM_USERNAME $TEMP_STEAM_PASSWORD  \
	+force_install_dir ~/.wine/drive_c/"Program Files (x86)"/Steam/steamapps/common/"$TEMP_STEAM_GAME_NAME"/ \
	+app_update $TEMP_STEAM_GAME_ID validate +quit #> dialog --title "Downloading your game" --tailbox out 0 0

    ln -s ~/.wine/drive_c/"Program Files (x86)"/Steam/steamapps/common/"$TEMP_STEAM_GAME_NAME" ~/Desktop/"$TEMP_STEAM_GAME_NAME"
fi
