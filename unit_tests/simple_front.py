#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -'''- coding: utf-8 -'''-

#import __future__
from dialog import Dialog
import sys, re
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

d = Dialog()

non_utf_character='Counter-Strike without utf-8: Céaser Útopic'
formatted = subprocess.call(non_utf_character.encode(sys.getfilesystemencoding()))



code, value = d.radiolist('Please, choose one game for install', width=40, height=10, list_height=3, choices=[\
('204300', 'Awesomenauts', 0),\
('240', 'Counter-Strike: Source', 0),\
('340', formatted, 0),\
('377160', 'Fallout 4', 0)])

if value == '204300':
	d.msgbox("Awesomenauts escolhido para download.", height=10, width=45)
elif value == '240':
	d.msgbox("Counter-Strike Source escolhido para download.", height=10, width=45)
elif value == '377160':
	d.msgbox("Fallout 4 escolhido para download. ;D", height=10, width=45)