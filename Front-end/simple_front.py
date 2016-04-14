#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dialog import Dialog

d = Dialog()


code, value = d.radiolist('Please, choose one game for install', width=40, height=10, list_height=3, choices=[\
('204300', 'Awesomenauts', 0),\
('240', 'Counter-Strike: Source', 0),\
('377160', 'Fallout 4', 0)])

if value == '204300':
	d.msgbox("Awesomenauts escolhido para download.", height=10, width=45)
elif value == '240':
	d.msgbox("Counter-Strike Source escolhido para download.", height=10, width=45)
elif value == '377160':
	d.msgbox("Fallout 4 escolhido para download. ;D", height=10, width=45)