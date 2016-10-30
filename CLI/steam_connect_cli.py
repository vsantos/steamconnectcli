# -*- encoding: UTF-8 -*-
#!/usr/bin/env python

import os
import sys
import json
import requests
import operator
import codecs
import time
from termcolor import colored
from scl import SteamConnect
from game_install import *

pick_me = SteamConnect()

def menu():
	if os.path.isfile('/tmp/chimera_os/steam_username.txt'):
		with open('/tmp/chimera_os/steam_username.txt','r') as y:
			currently_user = y.read()
	else:
		currently_user = "Anonymous (need login)"

	try:
		os.system("clear")
	except:
		print("[ERROR]: Not using Unix/Linux based, right?")

	print ("Welcome to Chimera OS SIS (Steam Integration System)\n")
	if currently_user == "Anonymous (need login)":
		print ("Currently logged in as: "+colored(currently_user,'red')+"\n")
	else:
		print ("Currently logged in as: "+colored(currently_user,'green')+"\n")
	print ("================\n")

	print("""Please select an option: \n
		1 - Please, log me in!;
		2 - Update my game library;
		3 - List my friends (Only public profiles for now);
		4 - Remove 'remember me' session files;
		5 - I want to install a game!
		9 - Exit\n""")
	option = input("SIS > ")

	if option == "1":
		if os.path.isfile('/tmp/chimera_os/cookies.tmp') == False or os.path.isfile('/tmp/chimera_os/user_info.txt') == False:
			pick_me.getting_credentials()
			pick_me.get_rsa_from_steam(pick_me.steam_user, pick_me.steam_password)
			pick_me.do_steam_login(pick_me.values_for_login)
			print ("\n[INFO]: Returning to menu in 3s...")
			time.sleep(3)
			menu()
		else:
			print ("Already connected.")
			print ("\n[INFO]: Returning to menu in 5s...")
			time.sleep(3)
			menu()
	elif option == "2":
		pick_me.getting_user_library()
		print ("\n[INFO]: Returning to menu in 5s...")
		time.sleep(5)
		menu()
	elif option == "3":
		pick_me.list_friends()
		print ("\n[INFO]: Returning to menu in 10s...")
		time.sleep(10)
		menu()
	elif option == "4":
		pick_me.remove_local_cookie_files()
		print ("\n[INFO]: Returning to menu in 3s...")
		time.sleep(3)
		menu()
	elif option == "5":
		dialog_game_choice()
		time.sleep(1)
	elif option == "9" or option == "exit":
		sys.exit()
	else:
		print ("[INFO]: Please, select a valid option!")
		time.sleep(3)
		menu()

#startOfCalling
try:
	menu()
except KeyboardInterrupt:
	print ("\n[INFO]: Steam Integration System interrupted with ctrl+c.")
	pass
