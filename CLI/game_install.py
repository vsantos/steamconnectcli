# -*- encoding: UTF-8 -*-
#!/usr/bin/env python

import os
import sys
import json
import requests
import operator
import codecs
import time
import subprocess
from termcolor import colored
from scl import SteamConnect

requests.packages.urllib3.disable_warnings()
#subprocess.call(command.encode(sys.getfilesystemencoding()))

pick_me = SteamConnect()

#First we will import user_library.json from /tmp, prepare the tuples, sort them and then display as UI
try:
	import dialog
	d = dialog.Dialog()
except:
	print ("Seens that you do not have python-dialog installed, we won't take care of it for you.")
	print ("before continue install Dialog: sudo apt-get install python-dialog")
	sys.exit(0)

def dialog_game_choice():
	#We have to check if the user is logged in, otherwise we will just restart the Menu
	if os.path.isfile('/tmp/chimera_os/user_info.txt') == False:
		print ("You are not logged, please get yourself online first.")
		print ("Returning to menu again.")
		time.sleep(3)
		menu()

	#If somehow the user doesn't have a updated library the system will take care of it
	if os.path.isfile('/tmp/chimera_os/user_library.json') == False:
		pick_me.getting_user_library()
		dialog_game_choice()

	f_output = codecs.open('/tmp/chimera_os/user_library.json', 'r')
	temp_library = json.load(f_output)

	user_games_list = []
	for g in temp_library:
		user_games_list.append((str(g['gameid']), g['name'], 0))
	user_games_list.sort(key=operator.itemgetter(1))

	code, get_gameid = d.radiolist("You currently have " +str(len(user_games_list))+ " games. Please, choose one of them to install.", width=80, height=80, list_height=20,choices=user_games_list)

	#Loop for getting the game's name from selected ID
	if get_gameid != "":
		for g in temp_library:
			if g['gameid'] == int(get_gameid):
				name_game_choice = g['name']
	else:
		if code == 0:
			d.msgbox("Not a valid option, don't forget to use the 'spacebar' for selecting the game")
			dialog_game_choice()
		elif code == 1:
			os.system("clear")
			print ("Thank you for using Chimera OS SIS. Cya! \n===\n")
			sys.exit(0)
	dialog_game_installer(name_game_choice, get_gameid)

def dialog_game_installer(name_game_choice, get_gameid):

	os.system("clear")
	#with the game selected, let's get some details from it such as platform and price :3
	SINGLE_GAME_URL = 'http://store.steampowered.com/api/appdetails?appids='+get_gameid
	supported_platforms = []
	game_categories = []

	with requests.Session() as c:
		response = c.get(SINGLE_GAME_URL)
		data = response.json()

		if data[get_gameid]['success'] == False:
			d.msgbox("Couldn't contact the game info page.")
			os.system("clear")
			dialog_game_choice()
		elif data[get_gameid]['success'] == True:
			for g in data[get_gameid]['data']['categories']:
				game_categories.append("-> "+g['description']+"\n ")
			print ("")

			if data[get_gameid]['data']['platforms']['linux'] == True:
				supported_platforms.append("Linux")
			if data[get_gameid]['data']['platforms']['windows'] == True:
				supported_platforms.append("Windows")
			if data[get_gameid]['data']['platforms']['mac'] == True:
				supported_platforms.append("mac")

	confirm_install = d.yesno("Your choice is:\n -> %s.\n\n\Do you want to continue?"\
	%(name_game_choice), height=15, width=35)

	if confirm_install == 1:
		#os.system("clear")
		dialog_game_choice()
	else:
		os.system("clear")
		print ("Installing")
		#os.system("steam_password=$( dialog --stdout --title 'Confirmação' --inputbox 'Por gentileza confirme sua senha da Steam' 10 50)")
		#os.system("steam_username=$( cat /tmp/chimera_os/steam_username.txt )")

		file1 = open('/tmp/chimera_os/temp_gameid.txt', 'w')
		file1.write(get_gameid)
		file1.close()
		file2 = open('/tmp/chimera_os/temp_gamename.txt', 'w')
		file2.write(name_game_choice)
		file2.close()
		file3 = open('/tmp/chimera_os/temp_platforms.txt','w')
		file3.write(supported_platforms[0])
		file2.close()

		os.system("chmod +x ./CLI/SteamGameInstaller/install_call.sh")
		os.system("./CLI/SteamGameInstaller/install_call.sh")
