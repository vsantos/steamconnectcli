#- *- coding: utf- 8 - *-
#!/usr/bin/env python3
import os
import json
import codecs
import operator
from dialog import Dialog

def parsing_user_library_to_json():
	print ("== Offline logic test for: 'Parsing Steam's library ==")

	if os.path.isfile('mocked/user_library.json') == True:
		f_output = codecs.open('mocked/user_library.json', 'r', encoding='utf-8')
		temp_library = json.load(f_output)

		user_games_list = []
		for game in temp_library:
			user_games_list.append((str(game['gameid']), game['name'], 0))
		
		user_games_list.sort(key=operator.itemgetter(1))
		return True
	else:
		return False

def game_choice_test():
	print ("== Offline logic test for: 'Game choice from Dialog' ==")	

	if os.path.isfile('mocked/user_library_parsed.txt') == True:
		f = open()
		temp
		temp_library = [line.strip() for line in open("mocked/user_library_parsed.txt", 'r')]

		d_box = Dialog()
		code, get_gameid = d_box.radiolist("You currently have " +str(len(temp_library))+ " games. Please, choose one of them to install.", width=200, height=100, list_height=20,choices=temp_library)

		return True
	else:
		return False

if parsing_user_library_to_json() == True:
	print ("Passed.")
else:
	print ("Failed.")
if game_choice_test() == True:
	print ("Passed.")
else:
	print ("Failed.")