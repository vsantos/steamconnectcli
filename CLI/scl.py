# -*- encoding: UTF-8 -*-

#Steam Chimera's Library (SCL)

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

class SteamConnect:

	def __init__(self):
		#We have to disable the SSL warnings from Steam manually, life sucks
		requests.packages.urllib3.disable_warnings()

		if os.path.isdir("/tmp/chimera_os/") == False:
			os.system("mkdir /tmp/chimera_os/")

	def getting_credentials(self):
		if os.path.isfile('/tmp/chimera_os/cookies.tmp') == False or os.path.isfile('/tmp/chimera_os/user_info.txt') == False:	
			self.steam_user = raw_input("Username: ")
			self.steam_password = getpass.getpass("Password: ")
		else:
			print ("You already have the files")

	def get_rsa_from_steam(self, steam_user, steam_password):
		URL_RSA = 'https://steamcommunity.com/login/getrsakey/'

		self.values_for_login = {
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
		values_for_rsa = {
			'username' : steam_user, 
			'donotcache' : str(int(time.time()*1000)),
		}

		with requests.Session() as c:
			response = c.post(URL_RSA, values_for_rsa)
			data_rsa = response.json()
			self.values_for_login.update({'rsatimestamp':data_rsa['timestamp']})

			if data_rsa['success'] == True:
				print ("Got RSA keys successfully.\n")

			mod = long(str(data_rsa['publickey_mod']), 16)
			exp = long(str(data_rsa['publickey_exp']), 16)
			rsa = RSA.construct((mod,exp))
			cipher = PKCS1_v1_5.new(rsa)
			self.values_for_login.update({'password': base64.b64encode(cipher.encrypt(steam_password))})
			print ("Password encrypted. \n")
			#For debugging purposes
			#print self.values_for_login

	def do_steam_login(self, values_for_login):
		URL_DO_LOGIN = 'https://steamcommunity.com/login/dologin/'

		with requests.Session() as c:
			try:
				response_for_login = c.post(URL_DO_LOGIN, self.values_for_login)
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
					if data_login['message'] == "There have been too many login failures from your network in a short time period.  Please wait and try again later.":
						print ("Too many login failures from your network, try again later. \n")
				except:
					print ("")

				try:
					if data_login['emailauth_needed'] == True:
						email_code_auth = raw_input("Please check your e-mail and input Steam Mail code, you need to allow this operation: ")
						self.values_for_login.update({'emailauth':email_code_auth})
						self.do_steam_login(self.values_for_login)
				except:
					if data_login['requires_twofactor'] == True:
						print ("Not able to trigger e-mail auth, trying Steam Guard.")
						mobile_code_auth = raw_input("Please check your mobile and input Steam Guard Code, you need to allow this operation: ")
						self.values_for_login.update({'twofactorcode':mobile_code_auth})
						self.do_steam_login(self.values_for_login)

			if data_login['success'] == True:
				print ("User logged in.")
				#print data_login
				
				with open('/tmp/chimera_os/user_info.txt', 'w') as ui:
					ui.write(data_login['transfer_parameters']['steamid'])
					print ("== User's info updated. ==")

				with open("/tmp/chimera_os/steam_username.txt","w") as h:
					h.write(values_for_login['username'])
					print ("== Username updated. ==")

				with open('/tmp/chimera_os/cookies.tmp', 'w') as f:
					pickle.dump(requests.utils.dict_from_cookiejar(response_for_login.cookies), f)
					print ("== Cookies importados. ==")

	def getting_user_library(self):
	
		try:
			file = open('/tmp/chimera_os/user_info.txt','r')
			USER_ID64 = file.read()
			file.close()
		except:
			print ("Seens that we do not have a needed file, please check your credentials then try again.")

		URL_USER_PROFILE = 'http://steamcommunity.com/profiles/'
		URL_USER_ALL_LIBRARY = URL_USER_PROFILE + USER_ID64 +'/games/?tab=all'
		print ("Connecting to your library...\n")

		try:
			with open('/tmp/chimera_os/cookies.tmp') as f:
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
			games_count = 0
			games = []
			with codecs.open('/tmp/chimera_os/user_library.json', 'w', encoding='utf-8') as ul:
				print ("Inserting user's library")

				#try:
				user_games = []
				for key in json.loads(final_json_all_games):
					games_count += 1

					gameid = key['appid']
					gamename = key['name']
					try:
						gamehours = key['hours_forever']
					except:
						gamehours = "Never played"
					game_list = {'gameid':gameid,'name':gamename,'hoursplayed':gamehours}
					user_games.append(game_list)
				#except:
					#print ("Something went wrong when splitting user's library.")
				#print user_games	
				json.dump(user_games, ul)
				print ("Your user currently have an amount of "+str(games_count)+" games.\n")

	def list_friends(self):
		self.STEAM_API_KEY = '219AE164017EB5546AE1C6059ECDBF8A'
		try:
			file = open('/tmp/chimera_os/user_info.txt','r')
			USER_ID64 = file.read()
			file.close()
		except:
			print ("Seens that we do not have a needed file, please check your credentials then try again.")

		MY_FRIENDS_URL = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s&relationship=friend" %(self.STEAM_API_KEY, USER_ID64)
		response = requests.get(MY_FRIENDS_URL)
		jsondata = response.json()
		if response.status_code == 401:
			print ("Your profile is private, honey.")
		else:
			#Loop for getting friend's info
			for f in jsondata['friendslist']['friends']:
				friend_id = f['steamid']
				friend_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json" %(self.STEAM_API_KEY, friend_id)
				friend_req = requests.get(friend_url).json()

				try:
					for f in friend_req['response']['players']:
						friend_nick = f['personaname']
						#friend_avatar = f['avatar']
						print ("Nick: %s") %(friend_nick.encode('utf-8'))
						if f['personastate'] == 0:
							print ("Status: Offline")
						elif f['personastate'] == 1:
							print ("Status: Online")
						elif f['personastate'] == 2:
							print ("Status: Busy")
						elif f['personastate'] == 3:
							print ("Status: Away")	
						elif f['personastate'] == 4:
							print ("Status: Snooze Zzzzzz....")
						elif f['personastate'] == 5:
							print ("Status: Currently in trade or looking for one")
						elif f['personastate'] == 6:
							print ("Status: Playing")						
						else:
							print ("Status: Unknown status! Get help.")	
						print ("")
											
				except:
					friend_name = f['realname']
					print ("Nick: %s") %(friend_name.encode('utf-8'))
					if f['personastate'] == 0:
						print ("Status: Offline")
					elif f['personastate'] == 1:
						print ("Status: Online")
					elif f['personastate'] == 2:
						print ("Status: Busy")
					elif f['personastate'] == 3:
						print ("Status: Away")	
					elif f['personastate'] == 4:
						print ("Status: Snooze Zzzzzz....")
					elif f['personastate'] == 5:
						print ("Status: Currently in trade")
					elif f['personastate'] == 6:
						print ("Status: Playing something")						
					else:
						print ("Status: Unknown status! Get help.")	
					print ("")

	def remove_local_cookie_files(self):
		if os.path.isfile('/tmp/chimera_os/cookies.tmp') == False and os.path.isfile('/tmp/chimera_os/user_info.txt') == False and os.path.isfile('steam_username.txt') == False:
			print ("You do not have any stored files to delete.\n")
		#if os.path.isfile('cookies.tmp') == True and os.path.isfile('user_info.txt') == True and os.path.isfile('steam_username.txt') == False:
		else:
			try:
				os.remove('/tmp/chimera_os/cookies.tmp')
				os.remove('/tmp/chimera_os/user_info.txt')
				os.remove('/tmp/chimera_os/steam_username.txt')
				os.remove('/tmp/chimera_os/user_library.json')
			except:
				print ("File not found.")
			print ("Files deleted, please create a new session. \n")