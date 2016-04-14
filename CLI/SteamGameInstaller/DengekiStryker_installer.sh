#!/bin/bash

#Getting basic_auth from user without 'echo password'
echo -n Steam user: 
read steam_user

echo -n Steam Password:
read -s steam_password

#This line will basically download the game from steam cmd's platform using user's credencials
~/steamcmd/steamcmd.sh +@sSteamCmdForcePlatformType windows +login $steam_user $steam_password +force_install_dir ~/.wine/drive_c/"Program Files (x86)"/Steam/steamapps/common/"Cho Dengeki Stryker"/ +app_update 321190 validate +quit

#We have to prepare the script for game`s calling as a symbolic link at desktop
touch ~/steamcmd/games/exec_script/Exec_Dengeki.sh
echo '#!/bin/bash' > ~/steamcmd/games/exec_script/Exec_Dengeki.sh
echo '' >> ~/steamcmd/games/exec_script/Exec_Dengeki.sh
echo 'Exec script created'
echo 'wine ~/steamcmd/games/Dengeki/"Cho Dengeki Stryker"/BGI.exe' >> ~/steamcmd/games/exec_script/Exec_Dengeki.sh
chmod 777 ~/steamcmd/games/exec_script/Exec_Dengeki.sh
ln ~/steamcmd/games/exec_script/Exec_Dengeki.sh ~/"Área de Trabalho"

#Inserting appid for wine Steam's app knows which game will run
touch ~/steamcmd/games/Dengeki/steam_appid.txt
echo 321190 > ~/steamcmd/games/Dengeki/steam_appid.txt

#wine ~/.wine/drive_c/"Program Files (x86)"/Steam/Steam.exe -no-dwrite &
