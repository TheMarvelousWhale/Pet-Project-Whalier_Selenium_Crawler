# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 23:24:45 2019

@author: Viet_NJPS
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import time
import threading
import random
import pandas as pd 

##############################################################################
#Global Resources

filename = "SeulgiFancam.csv"
songMainDF = pd.read_csv(filename)
songList = songMainDF.iloc[:,1]
ad_class = "ytp-ad-text"
ad_skip_class = "ytp-ad-skip-button"
cancel_button_class = "ytp-upnext-cancel-button"
fullscreen_class = "ytp-fullscreen-button"
play_btn_class = "ytp-play-button"


get_state_script =" return document.getElementById('movie_player').getPlayerState()"
pause_script = "document.getElementsByTagName('video')[0].pause()"
play_script = "document.getElementsByTagName('video')[0].play()"
mute_script = "document.getElementById('movie_player').mute()"
unmute_script = "document.getElementById('movie_player').unMute()"
adjust_volume = 'document.querySelector("video").volume = 0.5'
#play-btn-xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[3]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[24]/div[2]/div[1]/button"
##############################################################################
#helper functions
def stream_ready(Fox,url):
    Fox.get(url)
    while not ("return document.getElementById('movie_player').getPlayerState()"):
        pass

def streaming(Fox): 
    """
    Open an instance of Firefox. Click "Skip ad" whenever it appears. Close the instance when vidoe ends
    """
    if (Fox.execute_script(get_state_script) == 0):
        #Video not playing
        Fox.execute_script(play_script)
    if (Fox.execute_script(get_state_script) == -1):
        #Ad is playing
        if (fuck_ad(Fox) == 0): 
            #if ad is unclickable, wait until ad finishes
            while (Fox.execute_script("return document.getElementById('movie_player').getPlayerState()") == -1):
                pass
    try:
        while Fox.execute_script( "return document.getElementById('movie_player').getPlayerState()"):
            #time.sleep(1) 
            try:
                ad_button = WebDriverWait(Fox,3).until(EC.element_to_be_clickable((By.CLASS_NAME, ad_skip_class) )) #Continually check for ad popping halfway
                ad_button.click()
            except:
                continue
    finally:
        try:
            #click on cancel button at the end of video to prevent autoplay
            cancel_btn = WebDriverWait(Fox,7).until(EC.element_to_be_clickable((By.CLASS_NAME, cancel_button_class) ))
            cancel_btn.click()
            print("Successfully click cancel button")
            
        except:
            print("No cancel button")
            pass
        finally:
            if (Fox.execute_script(get_state_script)==0):
                play_button = WebDriverWait(Fox,3).until(EC.element_to_be_clickable((By.CLASS_NAME, play_btn_class) ))
                play_button.click()

def fuck_ad(Fox):
    """
    If ad is playing, fuck it
    """
    is_ad_on = Fox.execute_script("return document.getElementById('movie_player').getPlayerState()") == -1
    if (is_ad_on):
        try:
            ad_button = WebDriverWait(Fox,12).until(EC.element_to_be_clickable((By.CLASS_NAME, ad_skip_class) ))
            ad_button.click()
        except:
            print("Cannot click on ad")
            return 0
        else: 
            return 1
    else:
        return 1


        
###############################################################################
"""""""""""""""""""""""""""""MAIN EXECUTION"""""""""""""""""""""""""""""


def main():
    Fox = webdriver.Firefox()
    
    for song in songList:
        Fox.get("https://www.youtube.com"+song)
        
        script = input("Enter new script: \n")
        while (script != '#'):
            script = input("Enter new script: \n")
            try:
               Fox.execute_script(script)
            except:
               print("error")
        
        
if __name__ == "__main__":
    main()
    
    


    