# -*- encoding: UTF-8 -*-

import requests
import time
import base64
import getpass
import pickle
import re
import codecs
import json
import cookielib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

with requests.session() as c:

	USER_ID64 = '76561197983139814'
	URL_DO_LOGIN = 'https://steamcommunity.com/login/dologin/'
	URL_RSA = 'https://steamcommunity.com/login/getrsakey/'
	URL_USER_PROFILE = 'http://steamcommunity.com/profiles/'
	URL_USER_ALL_LIBRARY = URL_USER_PROFILE + USER_ID64 +'/games/?tab=all'
	URL_USER_WISHLIST = URL_USER_PROFILE + USER_ID64 +'/wishlist/'

	user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	values = {"donotcache": str(int(time.time()*1000))}

	''' 
	cookie={'steamLogin':'76561197983139814%7C%7C5B285D2AA1FB516CC82C51528C736F41B61028B5',
			'steamLoginSecure':'76561197983139814%7C%7C27A346A332868A6BD1BDF7A778488639E0D23FCD',
			'steamMachineAuth76561197983139814':'CCDD246C8697CC3A14F161747ED7ACBCD09780D5'
	}'''

	with open('cookies.tmp') as f:
		cookie = requests.utils.cookiejar_from_dict(pickle.load(f))

	response_for_games = c.get(URL_USER_ALL_LIBRARY, cookies=cookie)
	data = str(response_for_games.content)
	#print response_for_games.content
	
	#first_all_games_split = data.split('rgGames =', 1)[1]
	first_split_left, first_split_right = data.split("rgGames =")
	first_split_right = first_split_right[1:]
	second_split_left, second_split_right = first_split_right.split("var rgChangingGames =")
	second_split_left = second_split_left[:-5]
	final_all_games = json.dumps(second_split_left)
	final_json_all_games = json.loads(final_all_games)

	#print json.loads(final_json_all_games)
	
	for key in json.loads(final_json_all_games):
		print ("ID: " + str(key['appid']))
		print ("Name: "+ key['name'])
		try:
			print ("Hours played: " + str(key['hours_forever']))
		except:
			print ("Hours played: Never played")
		print ("")
