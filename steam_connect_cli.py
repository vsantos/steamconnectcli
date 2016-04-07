# -*- encoding: UTF-8 -*-
#!/usr/bin/env python

import os
import sys
import time
from termcolor import colored
from cl import SteamConnect

pick_me = SteamConnect()

def menu():
	if os.path.isfile('steam_username.txt') == True:
		with open('steam_username.txt','r') as y:
			currently_user = y.read()
	else:
		currently_user = "Anonymous (need login)"

	try:
		os.system("clear")
	except:
		print("Not using Unix/Linux based, right?")

	print ("Welcome to Chimera OS SIS (Steam Integration System)\n")
	if currently_user == "Anonymous (need login)":
		print ("Currently logged in as: "+colored(currently_user,'red')+"\n")
	else:
		print ("Currently logged in as: "+colored(currently_user,'green')+"\n")
	print ("================\n")

	print("Please select an option: \n\
		\n\
		1 - Please, log me in!; \n\
		2 - Show me my amount of games and update my local library;\n\
		3 - List my friends (Only public profiles for now);\n\
		4 - Remove 'remember me' session files;\n\
		5 - I want to install a game! (Not yet) \n\
		9 - Exit\n")
	option = raw_input("SIS > ")

	if option == "1":
		if os.path.isfile('cookies.tmp') == False or os.path.isfile('user_info.txt') == False:
			pick_me.getting_credentials()
			pick_me.get_rsa_from_steam(pick_me.steam_user, pick_me.steam_password)
			pick_me.do_steam_login(pick_me.values_for_login)
			print "\nReturning to menu in 3aqas..."
			time.sleep(3)
			menu()
		else:
			print ("Already connected, sweetpie.")
			print ("\nReturning to menu in 5s...")
			time.sleep(3)
			menu()	
	elif option == "2":
		pick_me.getting_user_library()
		print ("\nReturning to menu in 5s...")
		time.sleep(5)
		menu()
	elif option == "3":
		pick_me.list_friends()
		print ("\nReturning to menu in 10s...")
		time.sleep(10)
		menu()
	elif option == "4":
		pick_me.remove_local_cookie_files()
		print ("\nReturning to menu in 3s...")		
		time.sleep(3)
		menu()
	elif option == "5":
		print ("Not working yet.")
		time.sleep(2)
		menu()
	elif option == "9":
		sys.exit()
	else:
		print ("Honey, select a valid option!")
		time.sleep(3)
		menu()

#startOfCalling
try: 
	menu()
except KeyboardInterrupt:
	print ("\nSteam Integration System interrupted with ctrl+c.")
	pass