from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
##

import threading


options = Options()
options.add_argument("--user-data-dir=C:\\Users\\syedi\\AppData\\Local\\Google\\Chrome\\User Data") # change to my profile path

#chrome
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

#buffer timer
driver.implicitly_wait(10)

###########################################
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
####
driver.get("https://web.whatsapp.com/")

time.sleep(3)
driver.find_element_by_xpath('//*[@title="test"]').click()

def send_violation_picture(lock, image, msg):
    #lock.acquire()

    time.sleep(1)
    a=driver.find_element_by_xpath('//div[@title="Attach"]')
    #a.click()
    a.send_keys("\n")  ###############################################CHNAGED THIS LINE REFER TO LINE 36############################################
    #driver.find_element_by_class_name('_2C9f1').click()
    #click attach icon
    time.sleep(1)
    print("Click Attach")
    driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys(os.getcwd()+str(f"/{image}"))
   
    #send img dir to whatsapp  SncVf _3doiV                                  
    #img = driver.find_element_by_xpath('//span[@data-testid="send"]').click()
    try:
        driver.find_element_by_css_selector('._165_h._2HL9j').send_keys(Keys.ENTER)
    except:
        
        driver.find_element_by_css_selector('.SncVf._3doiV').send_keys(Keys.ENTER)
    #send the image

    time.sleep(1.5)
    try:
        
        driver.find_elements_by_css_selector('._13NKt.copyable-text.selectable-text')[-1].send_keys(msg)
        print(msg)
        #time.sleep(2)
        driver.find_elements_by_css_selector('._13NKt.copyable-text.selectable-text')[-1].send_keys(Keys.ENTER)

    except:
        driver.find_elements_by_css_selector('._2_1wd.copyable-text.selectable-text')[-1].send_keys(msg)
        print(msg)

        driver.find_elements_by_css_selector('._2_1wd.copyable-text.selectable-text')[-1].send_keys(Keys.ENTER)


    time.sleep(0.15)
    #lock.release()

def send_message(lock, msg):
    lock.acquire()

    
    #driver.find_element_by_xpath('//div[@title="Attach"]').click()
    #click attach icon

    #driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys(os.getcwd()+str(f"/{image}"))
    #send img dir to whatsapp
    #driver.find_element_by_xpath('//span[@data-icon="send"]').click()
    #send the image

    #_13NKt copyable-text selectable-text
    try:
        
        driver.find_elements_by_css_selector('._13NKt.copyable-text.selectable-text')[-1].send_keys(msg)
        print(msg)
        #time.sleep(2)
        driver.find_elements_by_css_selector('._13NKt.copyable-text.selectable-text')[-1].send_keys(Keys.ENTER)

    except:
        driver.find_elements_by_css_selector('._2_1wd.copyable-text.selectable-text')[-1].send_keys(msg)
        print(msg)

        driver.find_elements_by_css_selector('._2_1wd.copyable-text.selectable-text')[-1].send_keys(Keys.ENTER)

    time.sleep(0.15)
    lock.release()
'''
while True:
    try:
        print(driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').text)
        time.sleep(1)
    except Exception as e:
        print(e)

'''



















    
