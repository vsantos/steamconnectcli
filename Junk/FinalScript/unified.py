# -*- encoding: UTF-8 -*-

import requests
import time
import base64
import json
import codecs
import getpass
import pickle
import cookielib
import os, sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

#We have to disable the SSL warnings from Steam manually, lifes fucks
requests.packages.urllib3.disable_warnings()

#Global variables
user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
USER_ID64 = ''
encrypted_steam_password = ""
email_code_auth = ""
rsa_time_stamp = ""
steam_user = ""
games_count = 0

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
	#twofactorcode used for mobile auth
	"twofactorcode": "",
	"donotcache": str(int(time.time()*1000)),
}

URL_RSA = 'https://steamcommunity.com/login/getrsakey/'
URL_DO_LOGIN = 'https://steamcommunity.com/login/dologin/'
URL_USER_PROFILE = 'http://steamcommunity.com/profiles/'
URL_USER_ALL_LIBRARY = URL_USER_PROFILE + USER_ID64 +'/games/?tab=all'
#URL_USER_WISHLIST = URL_USER_PROFILE + USER_ID64 +'/wishlist/'
#URL_OWNED_GAMES = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=219AE164017EB5546AE1C6059ECDBF8A&steamid=76561197983139814&format=json'
STEAM_API_KEY = '219AE164017EB5546AE1C6059ECDBF8A'

def get_rsa_from_steam():
	global URL_RSA
	global values_for_rsa
	global steam_password
	global encrypted_steam_password
	global values_for_login
	global rsa_time_stamp

	with requests.Session() as c:
		response = c.post(URL_RSA, values_for_rsa)
		data_rsa = response.json()
		values_for_login.update({'rsatimestamp':data_rsa['timestamp']})

		if data_rsa['success'] == True:
			print ("Got RSA keys successfully.\n")

		mod = long(str(data_rsa['publickey_mod']), 16)
		exp = long(str(data_rsa['publickey_exp']), 16)
		rsa = RSA.construct((mod,exp))
		cipher = PKCS1_v1_5.new(rsa)
		#For debugging purposes
		values_for_login.update({'password': base64.b64encode(cipher.encrypt(steam_password))})
		#print values_for_login

def do_steam_login():
	global USER_ID64
	global values_for_login
	global email_code_auth
	global values_for_login

	with requests.Session() as c:
		try:
			response_for_login = c.post(URL_DO_LOGIN, values_for_login)
			data_login = response_for_login.json()
		except:
			print ("Could not login, did you checked your password? \n")

		if data_login['success'] == False:
			try:
				if data_login['message'] == "Please verify your humanity by re-entering the characters below.":
					print ("Are you human? Please enter captcha or try again later.\n")
			except:
				print ("")

			try:
				if data_login['emailauth_needed'] == True:
					email_code_auth = raw_input("Please check your e-mail and input Steam Mail code, you need to allow this operation: ")
					values_for_login.update({'emailauth':email_code_auth})
					do_steam_login()	
			except:
				if data_login['requires_twofactor'] == True:
					print ("Not able to trigger e-mail auth, trying Steam Guard.")
					mobile_code_auth = raw_input("Please check your mobile and input Steam Guard Code, you need to allow this operation: ")
					values_for_login.update({'twofactorcode':mobile_code_auth})
					do_steam_login()
		
		if data_login['success'] == True:
			print ("User logged in.")

			with open('user_info.txt', 'w') as ui:
				ui.write(data_login['transfer_parameters']['steamid'])
				print ("User's info updated.")

			with open('cookies.tmp', 'w') as f:
				pickle.dump(requests.utils.dict_from_cookiejar(response_for_login.cookies), f)
				print ("Cookies importados.\n")

			with open("steam_username.txt","w") as h:
				h.write(values_for_login['username'])	

def getting_user_library():
	global URL_USER_ALL_LIBRARY
	global USER_ID64
	global games_count

	try:
		file = open('user_info.txt','r')
		USER_ID64 = file.read()
		file.close()
	except:
		print ("Seens that we do not have a needed file, please check your credentials then try again.")

	URL_USER_ALL_LIBRARY = URL_USER_PROFILE + USER_ID64 +'/games/?tab=all'
	print ("Connecting to your library...\n")

	try:
		with open('cookies.tmp') as f:
			cookie = requests.utils.cookiejar_from_dict(pickle.load(f))
	except:
		print("I could not open the 'cookies' file properly. Please check if everything is ok.")	

	with requests.Session() as c:
		try:
			response_for_games = c.get(URL_USER_ALL_LIBRARY, cookies=cookie)
			data = str(response_for_games.content)
		except:
			print ('Unable to access your library, for your safety we are removing the cookie file under your installation directory.')
		
		#try:
		first_split_left, first_split_right = data.split("rgGames =")
		first_split_right = first_split_right[1:]
		second_split_left, second_split_right = first_split_right.split("var rgChangingGames =")
		second_split_left = second_split_left[:-5]
		final_all_games = json.dumps(second_split_left)
		final_json_all_games = json.loads(final_all_games)

		#Now lets split out on shell the user's library
		with codecs.open('user_library.json', 'w', encoding='utf-8') as ul:
			print ("Inserting user's library")
			try:
				for key in json.loads(final_json_all_games):
					games_count += 1

					ul.write("ID: " + str(key['appid'])+"\n")
					ul.write("Name: "+ key['name']+"\n")
					try:
						ul.write("Hours played: " + str(key['hours_forever'])+"\n")
					except:
						ul.write("Hours played: Never played\n")
					ul.write("")
			except:
				print ("Something went wrong when splitting user's library.")

			print ("Your user currently have an amount of "+str(games_count)+" games.\n")

def remove_local_cookie_files():
	if os.path.isfile('cookies.tmp') == False and os.path.isfile('user_info.txt') == False:
		print ("You do not have any stored files to delete.\n")
	if os.path.isfile('cookies.tmp') == True or os.path.isfile('user_info.txt') == True:
		os.remove('cookies.tmp')
		os.remove('user_info.txt')
		os.remove('steam_username.txt')
		print ("Files deleted, please create a new session. \n")

## Executing the script it self##
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
print ("Currently logged in as: "+currently_user+"\n")
print ("================\n")

print("Please select an option: \n\
	\n\
	1 - List your game library;\n\
	2 - Remove 'remember me' session files;\n\
	3 - List my friends (deprecated);\n\
	9 - Exit\n")
option = raw_input("SIS >")

if option == "1":
	if os.path.isfile('cookies.tmp') == False or os.path.isfile('user_info.txt') == False:
		get_rsa_from_steam()
		do_steam_login()

	getting_user_library()
elif option == "2":
	remove_local_cookie_files()
elif option == "9":
	sys.exit()

## End of execution ##
