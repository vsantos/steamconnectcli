#!/bin/bash

#First things first, we need to install Steam CMD as core of our software and your dependences as well

sudo rm /var/lib/apt/lists/lock 
#sudo apt-get update
#For x64 systems otherwise it will just be ignored
echo Y | sudo apt-get remove --purge lib32gcc1

#installing python and steam connect dependences

#installing dialog for future purpose
echo Y | sudo apt-get remove --purge python-pip python-dev build-essential
echo Y | sudo apt-get remove --purge python-dialog
echo Y | sudo pip uninstall requests
echo Y | sudo pip uninstall pycrypto
echo Y | sudo pip uninstall termcolor

#We prepare the directory that holds Steam CMD
rm -rf ~/steamcmd/

#Preparing the game cenario
#sudo apt-get install wine1.4
echo Y | sudo apt-get remove --purge wine1.8
echo Y | sudo apt-get remove --purge winetricks
rm -rf ~/.wine/