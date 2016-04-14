import json, requests

#user's info
#"Da Vinci's profile ID"
id_64 = "76561197983139814"
#Developer API KEY
api_key = "219AE164017EB5546AE1C6059ECDBF8A"
#Counter-Strike Global Offensive ID
game_id = 730 
#Contador
count_total = 0
count_achiev = 0

main_url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s&relationship=friend" %(api_key, id_64)
req = requests.get(main_url)
jsondata = req.json()


#Link to access achivements from a specific game and user
achievements_url = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=%d&steamid=%s&key=%s&format=json" %(game_id, id_64, api_key)
achivements_req = requests.get(achievements_url).json()
print ("Game: "+ achivements_req['playerstats']['gameName'])
for a in achivements_req['playerstats']['achievements']:
	count_total += 1
	if a['achieved'] == 1:
		count_achiev += 1

print ("Total: %d") %(count_total)
print ("Alcancado: %d") %(count_achiev)
print (format((float(count_achiev)/count_total)*100, ".2f")+"%\n")

#Player's friends information:
print ("Numero de amigos: %d\n") %len((jsondata['friendslist']['friends']))

#Loop for getting friend's info
for f in jsondata['friendslist']['friends']:
    friend_id = f['steamid']

    friend_url =  "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=219AE164017EB5546AE1C6059ECDBF8A&&steamids=%s&format=json" %(friend_id)
    friend_req = requests.get(friend_url).json()

    try:
      for f in friend_req['response']['players']:
        friend_name = f['realname']
        friend_avatar = f['avatar']
        print ("Name: %s") %(friend_name.encode('utf-8'))
    except:
      print f['personaname']
   

