from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
##

import multiprocessing


options = Options()
options.add_argument("--user-data-dir=C:\\Users\\nouma\\AppData\\Local\\Google\\Chrome\\User Data") # change to my profile path

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

    time.sleep(10)
    a=driver.find_element_by_xpath('//div[@title="Attach"]')
    a.click()
    #driver.find_element_by_class_name('_2C9f1').click()
    #click attach icon
    time.sleep(1)
    print(22)
    driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys(os.getcwd()+str(f"/{image}"))
    print(33)
    #send img dir to whatsapp                                    
    driver.find_element_by_xpath('//span[@data-icon="send"]').click()
    #send the image

    time.sleep(1.5)
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

    
    driver.find_elements_by_css_selector('._2_1wd.copyable-text.selectable-text')[-1].send_keys(msg)
    print(msg)
    #time.sleep(2)
    driver.find_elements_by_css_selector('._2_1wd.copyable-text.selectable-text')[-1].send_keys(Keys.ENTER)
    

    time.sleep(0.15)
    lock.release()

send_violation_picture(None, 'image.jpg', 'msg')

'''
while True:
    try:
        print(driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').text)
        time.sleep(1)
    except Exception as e:
        print(e)

'''



















    
