#!/bin/bash

#Getting basic_auth from user without 'echo password'
echo -n Steam user: 
read steam_user

echo -n Steam Password:
read -s steam_password

#This line will basically download the game from steam cmd's platform using user's credencials
~/steamcmd/steamcmd.sh +@sSteamCmdForcePlatformType windows +login $steam_user $steam_password +force_install_dir ~/.wine/drive_c/"Program Files (x86)"/Steam/steamapps/common/"GabeN: The Final Decision"/ +app_update 403740 validate +quit

#We have to prepare the script for game`s calling as a symbolic link at desktop
touch ~/steamcmd/games/exec_script/Exec_GabeN.sh
echo '#!/bin/bash' > ~/steamcmd/games/exec_script/Exec_GabeN.sh
echo '' >> ~/steamcmd/games/exec_script/Exec_GabeN.sh
echo 'Exec script created'
echo 'wine ~/steamcmd/games/Dengeki/"Gaben: The Final Decision"/Game.exe' >> ~/steamcmd/games/exec_script/Exec_GabeN.sh
chmod 777 ~/steamcmd/games/exec_script/Exec_GabeN.sh
ln ~/steamcmd/games/exec_script/Exec_GabeN.sh ~/"Área de Trabalho"

#Inserting appid for wine Steam's app knows which game will run
touch ~/.wine/drive_c/"Program Files (x86)"/Steam/steamapps/common/"GabeN: The Final Decision"/steam_appid.txt
echo 403740 > ~/.wine/drive_c/"Program Files (x86)"/Steam/steamapps/common/"GabeN: The Final Decision"/steam_appid.txt

#wine ~/.wine/drive_c/"Program Files (x86)"/Steam/Steam.exe -no-dwrite &
