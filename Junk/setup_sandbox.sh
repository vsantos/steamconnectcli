#!/bin/bash

#installing your sandbox virtual environment 
pip install virtualenv
pip install virtualenvwrapper

export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh

deactivate
mkvirtualenv SteamConnect
workon SteamConnect

#from 'requeriments' source we install all dependences
 pip install -r requirements.txt