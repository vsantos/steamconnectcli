#!/bin/bash

#First things first, we need to install Steam CMD as core of our software and your dependences as well

sudo rm /var/lib/apt/lists/lock 
#For x64 systems otherwise it will just be ignored
echo Y | sudo apt-get install lib32gcc1

#installing dialog for future purpose
echo Y | sudo apt-get install python-pip python-dev build-essential
echo Y | sudo apt-get install python-dialog
#echo Y | sudo apt-get install libffi-dev libssl-dev
sudo pip install requests
sudo pip install pycrypto
sudo pip install termcolor
sudo pip install --upgrade pip
sudo pip install --upgrade requests

#We prepare the directory that holds Steam CMD
mkdir ~/steamcmd
cd ~/steamcmd
wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
tar -xvzf steamcmd_linux.tar.gz
rm steamcmd_linux.tar.gz

#Preparing the game cenario
#sudo apt-get install wine1.4
echo Y | sudo apt-get install wine
echo Y | sudo apt-get install winetricks
mkdir ~/steamcmd/games/exec_script

cd ~/Downloads
wget https://steamcdn-a.akamaihd.net/client/installer/SteamSetup.exe
wine SteamSetup.exe /S
#We have to disable 'dwrite' library for text renderer purposes
wine reg add 'HKCU\Software\Valve\Steam' /v DWriteEnable /t REG_DWORD /d 00000000
#creating an alias to just "steam-wine" on terminal :3
alias steam-wine='WINEDEBUG=-all wine ~/.wine/drive_c/Program\ Files\ \(x86\)/Steam/Steam.exe >/dev/null 2>&1 &'
wine ~/.wine/drive_c/"Program Files (x86)"/Steam/Steam.exe -no-dwrite 2>&1 &

#We have to remove the desktop symbolic link and create a new one due Steam issues
rm ~/Desktop/Steam.desktop

#Now we just have to execute steam CMD for the first time, make sure that the installation will run lastly
cd ~/steamcmd
echo exit | ./steamcmd.sh