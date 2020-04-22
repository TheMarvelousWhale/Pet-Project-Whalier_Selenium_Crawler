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


##############################################################################
#Global Resources
TFTMN_cover = "https://m.youtube.com/watch?v=19sVE5Zp548&feature=youtu.be" 
SENORITA_url = "https://www.youtube.com/watch?v=2cevbhEqQF4"
Kevin_url = "https://www.youtube.com/watch?v=XR7Ev14vUh8"
downpour_url ="https://www.youtube.com/watch?v=QCKOWQ-_CYc"
crush_url = "https://www.youtube.com/watch?v=Kf3IumJmLqM"
ITSP_url = "https://www.youtube.com/watch?v=FX2WeSucYHc"
WAM_url = "https://www.youtube.com/watch?v=1eq9F-t02GY"
PM_url = "https://www.youtube.com/watch?v=M3rg-rh6MPo"
VVV_url = "https://www.youtube.com/watch?v=GdxvD7r58ng"
IOI_list = [downpour_url,crush_url,ITSP_url,WAM_url,PM_url,VVV_url]


ad_class = "ytp-ad-text"
ad_skip_class = "ytp-ad-skip-button"
cancel_button_class = "ytp-upnext-cancel-button"
fullscreen_class = "ytp-fullscreen-button"
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

    if (fuck_ad(Fox) == 0): #if ad is unclickable, wait until ad finishes
        while (Fox.execute_script("return document.getElementById('movie_player').getPlayerState()") == -1):
            time.sleep(1)
            continue
    try:
        time.sleep(3) #Another latency
        #on_fullscreen(Fox)
        while Fox.execute_script( "return document.getElementById('movie_player').getPlayerState()"):
            time.sleep(1) 
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
            Fox.quit()

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


def gen_multithread(num_thread,url):
    print("Starting main thread")
    threads = []
    lock = threading.Lock()
    for i in range(num_thread):
        
        threads.append(myThread(str(i),url,lock))
    
    for thread in threads:
        thread.start()
        time.sleep(3)
    
    for i in threads:
        i.join()
    print("Exiting main thread")

    
def user_interface():
    num_thread = num_round = 1
    while True:
        try:
            
            num_thread = int(input("Enter the number of threads: "))
        except ValueError:
            print()
            print("Please input some meaningful number: ")
        else:
            if num_thread > 16:
                print()
                print("Are you sure to proceed with {} threads? {} fucking threads??".format(num_thread,num_thread))
                ans = input("Key in 1 followed by Enter to continue with {} fucking threads: ".format(num_thread))
                if ans == '1':
                    break
                else :
                    num_thread = 0
                    print("Please enter a lower number this time.")
            elif num_thread < 0:
                print()
                print("Please enter a positive number. ")
            else:
                break
    while True:
        try:
            num_round = int(input("How many rounds do you want to run (-1 for infinite loop): "))
            break
        except:
            continue
    return num_thread,num_round

    

##############################################################################
#threading
class myThread(threading.Thread):
    def __init__(self,name,url,lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.name = name
        self.url = url
    def run(self):
        self.lock.acquire()
        time.sleep(1)
        print("Starting " + self.name)
        print("Thread {} acquired Lock".format(self.name))
        Fox = webdriver.Firefox()
        stream_ready(Fox,self.url)
        self.lock.release()
        print("Thread {} released Lock".format(self.name))
        streaming(Fox)
        print("Exiting " + self.name)

        
        
###############################################################################
"""""""""""""""""""""""""""""MAIN EXECUTION"""""""""""""""""""""""""""""
num_thread ,num_rounds = user_interface()


if num_rounds == -1:
    print("Ctrl C when done")
    while True :    
        gen_multithread(num_thread,random.choice(IOI_list))
else:
    for i in range(num_rounds):
        print("Round {}".format(i+1))
        gen_multithread(num_thread,random.choice(IOI_list))
    
    


    