#!/bin/bash

#Installing pipy
sudo easy_install pip

#Installing other script's dependences
sudo apt-get install python-dev libffi-dev libssl-dev
sudo pip install requests
sudo pip install pycrypto