import time #used to make the program wait

from selenium import webdriver #Allows you to launch/initialise a browser
from selenium.webdriver.chrome.options import Options # used to assign options to the Chrome Driver such as No popups or incognito mode
from selenium.webdriver.common.by import By #Allows you to search for things using specific parameters
from selenium.webdriver.support.ui import WebDriverWait #Allows you to wait for a page to load
from selenium.webdriver.support import expected_conditions as EC #Specify what you are looking for on a specific page in order to determine that the webpage has loaded.
from selenium.webdriver.common.keys import Keys #Allows you to type specific key functions such as 'RETURN'


from bs4 import BeautifulSoup


import requests

import credentials


def siteLoginSearchScrape():
    
    options = Options()
    options.add_argument("start-maximized") #max window size
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'/Users/jswan/Documents/Programming/GITHUB/tomsTacos/tacosEnv/chromedriver')
    driver.get("https://www.instagram.com")
    time.sleep(.5)
    login_elem = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')
    login_elem.click()
    
    #INPUTS LOG IN INFO AND CLICKS
    driver.find_element_by_xpath("//input[@name='username']").send_keys(credentials.login['username'])
    driver.find_element_by_xpath("//input[@name='password']").send_keys(credentials.login['password'])
    driver.find_element_by_xpath("//button[contains(.,'Log in')]").click()
    
    #ACCESS THE PAGE WATING TO SCRAPE
    driver.get("https://instagram.com/" + credentials.login['searchQuery'] + "/")
    
    
    #WRITES HTML TO FILE
    htmlText = driver.page_source
    bottomOfPage = driver.execute_script("return document.body.scrollHeight")
    
    i = 0
    
    while True:
        htmlStream = open('/Users/jswan/Documents/Programming/GITHUB/tomsTacos/tomsTacos.html', 'w')
        if (i >= bottomOfPage):
            htmlText = driver.page_source
            htmlStream.write(htmlText)
            htmlStream.close()
            htmlParseAndPrint()
            break
        driver.execute_script("window.scrollBy(0,500)", "")
        bottomOfPage = driver.execute_script("return document.body.scrollHeight")
        htmlText = driver.page_source
        htmlStream.write(htmlText)
        htmlStream.close()
        htmlParseAndPrint()
        time.sleep(5)
        i += 500


def htmlParseAndPrint():
    with open('/Users/jswan/Documents/Programming/GITHUB/tomsTacos/tomsTacos.txt', 'a') as txtStream:
        htmlStream = open('/Users/jswan/Documents/Programming/GITHUB/tomsTacos/tomsTacos.html', 'r')
        soup = BeautifulSoup(htmlStream, 'lxml')
        j = 0
        for div in soup.find_all('div', class_='_4rbun'):
            for comment in div.find_all('img', alt=True):
                j += 1
                print(j)
                print(comment['alt'])
                txtStream.write(comment['alt'])
                txtStream.write('\n')
        htmlStream.close()

siteLoginSearchScrape()

print("DONE!!!")
