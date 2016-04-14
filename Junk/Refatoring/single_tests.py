# -*- encoding: UTF-8 -*-

import requests
import time
import base64
import json
import getpass
import pickle
import cookielib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
USER_ID64 = '76561197983139814'
uname = raw_input("Username: ")
passwd = getpass.getpass("Password: ")

URL_DO_LOGIN = 'https://steamcommunity.com/login/dologin/'
URL_RSA = 'https://steamcommunity.com/login/getrsakey/'
URL_USER_PROFILE = 'http://steamcommunity.com/profiles/'
URL_USER_ALL_LIBRARY = URL_USER_PROFILE + USER_ID64 +'/games/?tab=all'
URL_USER_WISHLIST = URL_USER_PROFILE + USER_ID64 +'/wishlist/'

values_for_rsa = {'username' : 'jose691', 'donotcache' : str(int(time.time()*1000))}
headers_for_rsa = { 'User-Agent' : user_agent }

with requests.Session() as c:
	#let's get some POST from rsa and crypt our key
	response = c.post(URL_RSA, values_for_rsa)
	data_rsa = response.json()
	
	mod = long(str(data_rsa['publickey_mod']), 16)
	exp = long(str(data_rsa['publickey_exp']), 16)
	rsa = RSA.construct((mod,exp))
	cipher = PKCS1_v1_5.new(rsa)
    #For debugging purposes
	print base64.b64encode(cipher.encrypt(passwd))

    #Okay, let's finally login!
	values_for_login = {
		'username' : uname,
		"password": base64.b64encode(cipher.encrypt(passwd)),
		"loginfriendlyname": "",
		"captchagid": "",
		"captcha_text": "",
		"emailsteamid": "",
		"rsatimestamp": data_rsa["timestamp"],
		"remember_login": True,
		"donotcache": str(int(time.time()*1000)),
	}

	response_for_login = c.post(URL_DO_LOGIN, values_for_login)
	print response_for_login.status_code
	data_login = response_for_login.json()
	USER_ID64 = data_login['emailsteamid']
	print USER_ID64

	#Condicao que ira verificar a necessidade do codigo de verificacao via mail
	if data_login['emailauth_needed'] == True:
		email_code_auth = raw_input("Verifique seu e-mail, eh necessario incluir o codigo de verificacao: ")
		mail_update_dict = {"emailauth": email_code_auth}
		values_for_login.update(mail_update_dict)
		data_login = response_for_login.json()

		response_for_login = c.post(URL_DO_LOGIN, values_for_login)
		print response_for_login.status_code
		data_login = response_for_login.json()
		if data_login['success'] == True:
			print ("Usuario logado com sucesso")
	
	with open ('cookies.tmp', 'w') as f:
		pickle.dump(requests.utils.dict_from_cookiejar(response_for_login.cookies), f)
		print ("Cookies importados.")