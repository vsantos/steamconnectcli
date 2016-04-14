import json
import random
import webbrowser
import urllib, urllib2

from Tkinter import *

apikey = ''
steamid = '76561197983139814'

http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
           '?key=219AE164017EB5546AE1C6059ECDBF8A&steamid={}&include_appinfo=1
def getownedgames(apikey, steamid):
    url = ('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
           '?key={}&steamid={}&include_appinfo=1'.format(apikey, steamid))

    return json.loads(urlopen(url).read().decode())['response']['games']


def getimage(game):
    imageurl = 'http://cdn.steampowered.com/v/gfx/apps/{}/header.jpg'
    data = urlopen(imageurl.format(game['appid'])).read()

    return ImageTk.PhotoImage(data=data)


def playgame(game):
    webbrowser.open('steam://rungameid/{}'.format(game['appid']))


def choosegame(games, tk, button):
    game = random.choice(games)

    try:
        game['image'] = getimage(game)
    except HTTPError:
        return choosegame(games, tk, button)

    button.configure(image=game['image'], command=lambda: playgame(game))

    tk.title(game['name'])

games = getownedgames(apikey, steamid)

# GUI
tk = Tk()
tk.resizable(0, 0)
tk.configure(bg='gray11')

gamebutton = Button(tk, width=460, height=215, bd=0,
                    bg='gray11', activebackground='gray11',
                    relief='flat', cursor='hand2')
gamebutton.pack()

changebutton = Button(tk, width=41, height=1, bd=0,
                      fg='white', activeforeground='white',
                      bg='gray11', activebackground='gray11',
                      relief='flat', cursor='hand2',
                      font=('Segoe UI Semilight',), text='Nope!',
                      command=lambda: choosegame(games, tk, gamebutton))
changebutton.pack()

changebutton.invoke()

tk.mainloop()