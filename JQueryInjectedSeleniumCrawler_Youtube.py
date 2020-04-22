# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 01:12:55 2019

@author: Viet_NJPS
"""


from selenium import webdriver

Fox = webdriver.Firefox()
url = "https://www.youtube.com/watch?v=pSudEWBAYRE"
Fox.get(url)
script = None
while (script != '#'):
       script = input("Enter new script: \n")
       try:
           Fox.execute_script(script)
       except:
           print("error")
           
           
pause_script = "document.getElementsByTagName('video')[0].pause()"
play_script = "document.getElementsByTagName('video')[0].play()"
mute_script = "document.getElementById('movie_player').mute()"
unmute_script = "document.getElementById('movie_player').unMute()"
adjust_volume = 'document.querySelector("video").volume = 0.5'
