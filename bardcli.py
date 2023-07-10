import sys
import time
from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getElement(driver,byWhat,strng,waitTime):
    wait = WebDriverWait(driver, waitTime)
    return wait.until(EC.presence_of_element_located((byWhat,strng)))
    
    
def operateElement(value,element,keysValue,waitTime):
    start_time = time.time()
    if(value == "click"):
        while time.time() - start_time < waitTime:
            try:
                element.click()
                break  
            except:
                time.sleep(0.5)
    elif(value == "send_keys"):
        while time.time() - start_time < waitTime:
            try:
                element.send_keys(keysValue)
                break
            except:
            	time.sleep(0.5)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://bard.google.com/")

argument = sys.argv[1]
element = getElement(driver,By.ID,"mat-input-0",2)
operateElement("send_keys",element,str(argument),2)
operateElement("send_keys",element,"" + Keys.TAB*2 + Keys.ENTER,2)

element = getElement(driver,By.CLASS_NAME,"response-container-content",2)
html_value = element.get_attribute("innerHTML")
while len(html_value) < 20  and ("I'm Bard" not in html_value):
	element = getElement(driver,By.CLASS_NAME,"response-container-content",2)
	try:
		html_value = element.get_attribute("innerHTML")
	except:
		1==1

soup = BeautifulSoup(html_value, 'html.parser')

# Extract all strings and format them
formatted_strings = [string.strip() for string in soup.strings if string.strip()]

# Output the formatted strings
for string in formatted_strings:
    print(string)
    













