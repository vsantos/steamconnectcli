# -*- encoding: UTF-8 -*-

import requests
import time
import base64
import json
import getpass
import pickle
import cookielib
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

#Global variables
user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
USER_ID64 = ''
encrypted_steam_password = ""
email_code_auth = ""
rsa_time_stamp = ""
steam_user = ""
steam_password = ""

if os.path.isfile('cookies.tmp') == False or os.path.isfile('user_info.txt') == False:
	steam_user = raw_input("Username: ")
	steam_password = getpass.getpass("Password: ")

headers = { 'User-Agent' : user_agent }
values_for_rsa = {
	'username' : steam_user, 
	'donotcache' : str(int(time.time()*1000)),
}
values_for_login = {
	'username' : steam_user,
	"password": "",
	"loginfriendlyname": "",
	"captchagid": "",
	"captcha_text": "",
	"emailauth": "",
	"emailsteamid": "",
	"rsatimestamp": '',
	"remember_login": True,
	"donotcache": str(int(time.time()*1000)),
}

URL_RSA = 'https://steamcommunity.com/login/getrsakey/'
URL_DO_LOGIN = 'https://steamcommunity.com/login/dologin/'
URL_USER_PROFILE = 'http://steamcommunity.com/profiles/'
URL_USER_ALL_LIBRARY = URL_USER_PROFILE + USER_ID64 +'/games/?tab=all'
URL_USER_WISHLIST = URL_USER_PROFILE + USER_ID64 +'/wishlist/'

def get_rsa_from_steam():
	global URL_RSA
	global values_for_rsa
	global steam_password
	global encrypted_steam_password
	global values_for_login
	global rsa_time_stamp

	with requests.Session() as c:
		print URL_RSA
		print values_for_rsa
		response = c.post(URL_RSA, values_for_rsa)
		data_rsa = response.json()
		print data_rsa
		values_for_login.update({'rsatimestamp':data_rsa['timestamp']})

		if data_rsa['success'] == True:
			print ("Got RSA keys successfully.")

		mod = long(str(data_rsa['publickey_mod']), 16)
		exp = long(str(data_rsa['publickey_exp']), 16)
		rsa = RSA.construct((mod,exp))
		cipher = PKCS1_v1_5.new(rsa)
		#For debugging purposes
		values_for_login.update({'password': base64.b64encode(cipher.encrypt(steam_password))})

def do_steam_login():
	global USER_ID64
	global values_for_login
	global email_code_auth
	global values_for_login

	with requests.Session() as c:
		response_for_login = c.post(URL_DO_LOGIN, values_for_login)
		data_login = response_for_login.json()
		#print data_login

		if data_login['success'] == False:
			if data_login['emailauth_needed'] == True:
				email_code_auth = raw_input("Verifique seu e-mail, eh necessario incluir o codigo de verificacao: ")
				values_for_login.update({'emailauth':email_code_auth})
				do_steam_login()	
		
		if data_login['success'] == True:
			print ("User logged in.")

			with open ('user_info.txt', 'w') as ui:
				ui.write(data_login['transfer_parameters']['steamid'])
				print ("User's info updated.")

			with open ('cookies.tmp', 'w') as f:
				pickle.dump(requests.utils.dict_from_cookiejar(response_for_login.cookies), f)
				print ("Cookies importados.")

def getting_user_library():
	global URL_USER_ALL_LIBRARY
	global USER_ID64

	file = open('user_info.txt','r')
	USER_ID64 = file.read()
	file.close()

	URL_USER_ALL_LIBRARY = URL_USER_PROFILE + USER_ID64 +'/games/?tab=all'	
	print ("Connecting to url: " +URL_USER_ALL_LIBRARY)

	try:
		with open('cookies.tmp') as f:
			cookie = requests.utils.cookiejar_from_dict(pickle.load(f))
	except:
		print("I could not open the 'cookies' file properly. Please check if everything is ok.")	

	with requests.Session() as c:
		try:
			response_for_games = c.get(URL_USER_ALL_LIBRARY, cookies=cookie)
		except:
			print ('Unable to access your library, for your safety we are removing the cookie file under your installation directory.')

		data = str(response_for_games.content)
		#print data
		
		first_split_left, first_split_right = data.split("rgGames =")
		first_split_right = first_split_right[1:]
		second_split_left, second_split_right = first_split_right.split("var rgChangingGames =")
		second_split_left = second_split_left[:-5]
		final_all_games = json.dumps(second_split_left)
		final_json_all_games = json.loads(final_all_games)

		#print json.loads(final_json_all_games)
		#Now lets split out the user's library
		for key in json.loads(final_json_all_games):
			print ("ID: " + str(key['appid']))
			print ("Name: "+ key['name'])
			try:
				print ("Hours played: " + str(key['hours_forever']))
			except:
				print ("Hours played: Never played")
			print ("")

def remove_local_cookie_files():
	os.remove('cookies.tmp')
	os.remove('user_info.txt')

## Executing the script it self##

print("Please select an option: \n\
	1 - List your game library\n\
	2 - Remove 'auto login' files\n\
	3 - Which friends of mine are there?\n")
option = raw_input()

if option == "1":
	if os.path.isfile('cookies.tmp') == False or os.path.isfile('user_info.txt') == False:
		get_rsa_from_steam()
		do_steam_login()

	getting_user_library()
elif option == "2":
	remove_local_cookie_files()

##