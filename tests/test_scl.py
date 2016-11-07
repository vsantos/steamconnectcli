import unittest
import codecs
import json
import time
import sys
sys.path.append('../src')
from scl import SteamConnect

class SteamConnectUnitTest(unittest.TestCase):

	def setUp(self):
		self.scl_object = SteamConnect()

	def setting_credentials_from_mocked_file(self):
		with codecs.open('mocked/mocked_steam_credentials.json','r') as f:
			mocked_steam_credentials = json.loads(f.read())
			steam_password = str.encode(mocked_steam_credentials['mocked_steam_password'])
			return mocked_steam_credentials['mocked_steam_username'], steam_password

	def test_steam_get_credentials(self):
		self.assertTrue(self.scl_object.getting_credentials())
		print ("Finished: test_steam_login\n")

	def test_steam_rsa_cryptography(self):
		with codecs.open('mocked/mocked_steam_credentials.json','r') as f:
			mocked_steam_credentials = f.read()
			steam_password = str.encode(mocked_steam_credentials['mocked_steam_password'])

		self.assertTrue(self.scl_object.get_rsa_from_steam(mocked_steam_credentials['mocked_steam_username'],steam_password))
		print ("Finished: test_steam_rsa_cryptography_with_credentials\n")

	def test_steam_login(self):
		steam_user, steam_password = self.setting_credentials_from_mocked_file()
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

		#self.assertTrue(self.scl_object.do_steam_login(self.scl_object.values_for_login))
		print ("Finished: test_steam_login\n")

if __name__ == '__main__':
	unittest.main()
