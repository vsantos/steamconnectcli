# -*- encoding: UTF-8 -*-

#Steam Chimera's Library (SCL)

import requests
import time
import base64
import json
import demjson
import codecs
import getpass
import pickle
import http.cookiejar
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
			self.steam_user = input("Username: ")
			steam_temp_password = getpass.getpass("Password: ")
			self.steam_password = str.encode(steam_temp_password)
			return True
		elif os.path.isfile('/tmp/chimera_os/cookies.tmp'):
			print ("[INFO]: You are already logged.")
			return True
		else:
			return False

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

			if data_rsa['success']:
				print ("[INFO]: Got RSA keys successfully.")

			mod = int(str(data_rsa['publickey_mod']), 16)
			exp = int(str(data_rsa['publickey_exp']), 16)
			rsa = RSA.construct((mod,exp))
			cipher = PKCS1_v1_5.new(rsa)
			try:
				self.values_for_login.update({'password': base64.b64encode(cipher.encrypt(steam_password))})
				print ("[INFO]: Password encrypted.")
				return True
			except:
				return False

	def do_steam_login(self, values_for_login):
		URL_DO_LOGIN = 'https://steamcommunity.com/login/dologin/'

		with requests.Session() as c:
			try:
				response_for_login = c.post(URL_DO_LOGIN, self.values_for_login)
				data_login = response_for_login.json()
			except:
				print ("[ERROR]: Could not login, did you checked your password?")
				return False

			if data_login['success'] == False:
				try:
					if data_login['message'] == "Please verify your humanity by re-entering the characters below.":
						print ("[ERROR]: Are you human? Please enter captcha or try again later.")
				except:
					return False

				try:
					if data_login['message'] == "There have been too many login failures from your network in a short time period.  Please wait and try again later.":
						print ("[ERROR]: Too many login failures from your network, try again later.")
				except:
					pass

				try:
					if data_login['emailauth_needed']:
						email_code_auth = input("[INFO]: Please check your e-mail and input Steam Mail code, you need to allow this operation: ")
						self.values_for_login.update({'emailauth':email_code_auth})
						self.do_steam_login(self.values_for_login)
				except:
					pass

				try:
					if data_login['requires_twofactor']:
						print ("[INFO]: Not able to trigger e-mail auth, trying Steam Guard.")
						mobile_code_auth = input("[INFO]: Please check your mobile and input Steam Guard Code, you need to allow this operation: ")
						self.values_for_login.update({'twofactorcode':mobile_code_auth})
						self.do_steam_login(self.values_for_login)
				except:
					pass

			if data_login['success']:
				print ("[INFO]: User logged in.")
				#print data_login

				with open('/tmp/chimera_os/user_info.txt', 'w') as ui:
					ui.write(data_login['transfer_parameters']['steamid'])
					print ("[INFO]: User's info updated. ")

				with open("/tmp/chimera_os/steam_username.txt","w") as h:
					h.write(values_for_login['username'])
					print ("[INFO]: Username updated. ")

				with open('/tmp/chimera_os/steam_cookies.tmp', 'w') as f:

					jar = http.cookiejar.LWPCookieJar(filename="/tmp/chimera_os/steam.cookies")
					#print (response_for_login.cookies)
					for c in response_for_login.cookies:
					    jar.set_cookie(c)
					jar.save(ignore_discard=True)
					#print (jar)
					print ("[INFO]: Cookies imported.")
				return True
			else:
				return False

	def getting_user_library(self):
		if os.path.isfile('/tmp/chimera_os/user_info.txt') == False:
			print ("[ERROR]: Please, log in before continue.")
			time.sleep(3)
			sys.exit(1)

		try:
			file = open('/tmp/chimera_os/user_info.txt','r')
			USER_ID64 = file.read()
			file.close()
		except:
			print ("[ERROR]: Seens that we do not have a credential needed file, please check it then try again.")

		URL_USER_PROFILE = 'http://steamcommunity.com/profiles/'
		URL_USER_ALL_LIBRARY = URL_USER_PROFILE + USER_ID64 +'/games/?tab=all'
		print ("[INFO]: Connecting to your library")

		try:
			jar2 = http.cookiejar.LWPCookieJar()
			jar2.load(filename="/tmp/chimera_os/steam.cookies")
		except:
			print("[ERROR]: I could not open the 'cookies' file properly. Please check if everything is ok.")

		with requests.Session() as c:
			try:
				response_for_games = c.get(URL_USER_ALL_LIBRARY, cookies=jar2)
				#print (response_for_games.status_code)
				data = str(response_for_games.content)
			except:
				print ('[ERROR]: Unable to access your library, for your safety we are removing the cookie file under your installation directory.')

			#Here we are wrapping the html page for getting only the games json:
			first_split_left, first_split_right = data.split("rgGames =")
			first_split_right = first_split_right[1:]
			second_split_left, second_split_right = first_split_right.split(" rgChangingGames =")
			second_split_left = second_split_left[:-12]
			final_all_games = json.dumps(second_split_left)
			final_json_all_games = json.loads(final_all_games)

			#Now we have to treat the json to our purposes
			games_count = 0
			with codecs.open('/tmp/chimera_os/user_library.json', 'w', encoding='utf-8') as ul:
				print ("[INFO]: Inserting user's library...")

				user_games = []

				# The html 'json' have some escaped characters which is not readble as a real json, so we need to decode
				decoded = demjson.decode(final_json_all_games)

				for key in decoded:
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
				print ("[INFO]: Your user currently have an amount of "+str(games_count)+" games.\n")

	def list_friends(self):
		self.STEAM_API_KEY = '219AE164017EB5546AE1C6059ECDBF8A'
		try:
			file = open('/tmp/chimera_os/user_info.txt','r')
			USER_ID64 = file.read()
			file.close()
		except:
			print ("[ERROR]: Seens that we do not have a credential needed file, please check it then try again.")

		MY_FRIENDS_URL = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s&relationship=friend" %(self.STEAM_API_KEY, USER_ID64)
		response = requests.get(MY_FRIENDS_URL)
		jsondata = response.json()
		if response.status_code == 401:
			print ("[ERROR]: Your profile is private, we can't continue.")
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
		if os.path.isfile('/tmp/chimera_os/steam.cookies') == False and os.path.isfile('/tmp/chimera_os/user_info.txt') == False and os.path.isfile('steam_username.txt') == False:
			print ("[INFO]: You do not have any stored files to delete.\n")
		else:
			try:
				os.remove('/tmp/chimera_os/steam_username.txt')
				os.remove('/tmp/chimera_os/steam.cookies')
				os.remove('/tmp/chimera_os/user_info.txt')
				os.remove('/tmp/chimera_os/user_library.json')

			except:
				print ("File not found.")
			print ("[INFO]: Files deleted, please create a new session. \n")
