#The containts of the data collected are owned by Valve Corporation.
#Ticker number: 3869-QYLC-9515

import requests
import time
import base64
import getpass
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

#How can I login ? :D
user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
USER_ID64 = '76561197983139814'
uname = raw_input("Username: ")
passwd = getpass.getpass("Password: ")

URL_RSA = 'https://steamcommunity.com/login/getrsakey/'
URL_USER_PROFILE = 'http://steamcommunity.com/profiles/'
URL_USER_ALL_LIBRARY = URL_USER_PROFILE + USER_ID64 +'/games/?tab=all'
URL_USER_WISHLIST = URL_USER_PROFILE + USER_ID64 +'/wishlist/'

values = {'username' : uname, 'donotcache' : str(int(time.time()*1000))}
headers = { 'User-Agent' : user_agent }

with requests.Session() as c:
        response = c.post('https://steamcommunity.com/login/getrsakey/', values, headers, timeout=20)
        data = response.json()

        #Processing key
        mod = long(str(data['publickey_mod']), 16)
        exp = long(str(data['publickey_exp']), 16)
        rsa = RSA.construct((mod,exp))
        cipher = PKCS1_v1_5.new(rsa)
        print base64.b64encode(cipher.encrypt(passwd))

        #Let's finally login!
        values2 = {
                'username' : uname,
                "password": base64.b64encode(cipher.encrypt(passwd)),
                "emailauth": "",
                "loginfriendlyname": "",
                "captchagid": "-1",
                "captcha_text": "",
                "emailsteamid": "",
                "rsatimestamp": data["timestamp"],
                "remember_login": False,
                "donotcache": str(int(time.time()*1000)),
        }
        response2 = c.post(URL_USER_ALL_LIBRARY, values2, headers, timeout=20)
        print response2.content
        print response2.status_code
