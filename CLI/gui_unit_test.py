# -*- encoding: UTF-8 -*-
#!/usr/bin/env python

import os
import sys
import json
import operator
import codecs
import easygui
import time
#from scl import SteamConnect
#from game_install import *

f_output = codecs.open('/tmp/chimera_os/user_library.json', 'r', encoding='utf-8')
temp_library = json.load(f_output)

user_games_list = []
user_game_list_without_id = []
for g in temp_library:

	gameid_temp = str(g['gameid'])
	gamename_temp =  str(g['name'].encode('utf-8'))

	user_games_list.append((gameid_temp, gamename_temp))#, 0))
	user_game_list_without_id.append(gamename_temp)

user_games_list.sort(key=operator.itemgetter(1))

game_choice = easygui.choicebox(msg='Pick an item', title='', choices=user_game_list_without_id)

for p in temp_library:
	if str(p['name'].encode('utf-8')) == game_choice:

		gameid_temp_2 = str(p['gameid'])
