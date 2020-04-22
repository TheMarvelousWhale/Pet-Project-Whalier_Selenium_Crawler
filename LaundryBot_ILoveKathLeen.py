# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:26:26 2019

@author: Viet_NJPS
"""

from selenium import webdriver
import random
import time

Fox = webdriver.Firefox() #initialize driver 
url = "https://docs.google.com/forms/d/e/1FAIpQLSfddvycZub38o73tCQz_CuXadvKBhGd4FBXEjiRGp2EK5iIBA/viewform"    #url of target google form
Fox.get(url) #get an url 
random_chores = ["Vacuuming","Cleaning dog poo","Cleaning the garden","Watering plants","Feeding my cat","Feeding my dogs","Clean fish tank"]
#options for to fill in for Others: 


def iLoveKathleen():
    """
    This function runs through the google form given, choose the options randomly (with weight) and submit
    """

    num = 8 #umber of ans in the mcq
    num_Q = 2 #number of questions
    
    xps = "/html/body/div/div[2]/form/div/div[2]/div[2]/div["
    #the question number is here inbetween these 2 xpath
    xpm = "]/div/div[2]/div["
    #the option index is inbetween these 2 xpath
    xpe = "]/div/label/div/div[1]/div[2]"   
    
    #Run throught each question, randomly biased pick the answer
    for k in range(1,num_Q+1):
        num_ans = choose_top_three_v2(num,6,1) if k == 1 else choose_top_three(num,1)
        for i in num_ans:
            if i == 8:
            #When option is send in answers 
                box_xpath = xps + str(k) + "]/div/div[2]/div[8]/div/div/div/div/div/div[1]/input"
                box_elem = Fox.find_element_by_xpath(box_xpath)
                box_elem.send_keys(random.choice(random_chores))
            else: 
                xp = xps+str(k)+xpm+str(i)+ xpe   #i is the index of the question
                elem = Fox.find_element_by_xpath(xp)
                elem.click()
                
    #find submit button, send
    submit_xpath = "/html/body/div/div[2]/form/div/div[2]/div[3]/div[1]/div/div/content/span"
    elem_submit= Fox.find_element_by_xpath(submit_xpath)
    elem_submit.click()


def choose_top_three(num,bias):
    """This function returns a list of three random numbers but contain the bias 70% of the time"""
    num_ans = [] 
    prob = random.randint(1,10)
    if prob < 6 :                 #%50 of the time
        num_ans.append(bias)
    while(len(num_ans)<3):
        ran_num = random.randint(1,num);
        if ran_num not in num_ans:
            num_ans.append(ran_num)
    return num_ans


def choose_top_three_v2(num,bias1,bias2):
    """This function returns a list of three random number but bias1 appears most often followed by 2"""
    num_ans = []    #ans list
    prob = random.randint(1,10)
    if prob < 9: #80% of the time
        num_ans.append(bias1) #append 
    prob2 = random.randint(1,10)
    if prob2 <7:
        num_ans.append(bias2)
    while(len(num_ans)<3):
        ran_num = random.randint(1,num);
        if ran_num not in num_ans:
            num_ans.append(ran_num)
    return num_ans
    
### $Let it Rain$ ###
while True:
    iLoveKathleen()
    time.sleep(3)
    resub_xp = "/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/a" #resubmit xpath
    elem_re = Fox.find_element_by_xpath(resub_xp)
    elem_re.click()
    
    
    

