# -*- encoding: UTF-8 -*-
#!/usr/bin/env python

from sc_classes import SteamConnect

pick_me = SteamConnect()

#These steps will basically log you in and store your cookies as well
#This invoke will just work for CLI version, Front-end will ask for the credentials it self
pick_me.getting_credentials()
#CLI or Front will pass the steam_user or steam_password
pick_me.get_rsa_from_steam(pick_me.steam_user, pick_me.steam_password)
pick_me.do_steam_login(pick_me.values_for_login)
pick_me.getting_user_library()
pick_me.list_friends()
