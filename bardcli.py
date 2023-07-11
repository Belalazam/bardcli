import sys
import time
import pickle
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
    
def getElements(driver,byWhat,strng,waitTime):
    wait = WebDriverWait(driver, waitTime)
    return wait.until(EC.presence_of_all_elements_located((byWhat,strng)))
	
    
    
    
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
            	
def save_driver(driver):
    with open('storage.pkl', 'wb') as file:
        pickle.dump(driver, file)

def load_driver():
    with open('storage.pkl', 'rb') as file:
        return pickle.load(file)
       
def optmizeCondition(temp):
	z = 0
	try:
		z=len(str(temp.get_attribute("innerHTML")))
	except:  
		return True
	if(z>20):
		return False
	return True
        
def helper():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
	driver = webdriver.Chrome(options=chrome_options)

	argument = None
	if(len(sys.argv) > 2):
		argument = sys.argv[2]
	else :
		argument = sys.argv[1]
	for i in range(1,len(sys.argv)):
		if str(sys.argv[i]) == "new" or str(sys.argv[i]) == "-n":
			driver = webdriver.Chrome(options=chrome_options)
			driver.get("https://bard.google.com/")
			save_driver(driver.get_cookies())
			print("new instance has been created \n")
			if(len(sys.argv) == 2):
				return
			print("working on your new query ... \n\n")

		
	if driver == None : 
		driver = webdriver.Chrome(options=chrome_options)
		driver.get("https://bard.google.com/")
	else : 
		try:
	    		cookies = load_driver()
	    		for cookie in cookies:
	    			driver.add_cookie(cookie)
	    		
		except:
			print("oops not found , creating new instance , your old query trainning is been lossed")
			driver = webdriver.Chrome(options=chrome_options)
			driver.get("https://bard.google.com/")
			save_driver(driver.get_cookies())
			return
			
	element = getElement(driver,By.ID,"mat-input-0",2)
	operateElement("send_keys",element,str(argument),2)
	operateElement("send_keys",element,"" + Keys.TAB*2 + Keys.ENTER,2)

	element = getElements(driver,By.CLASS_NAME,"response-container-content",20)
	temp = element[len(element) - 1]
	while optmizeCondition(temp): 
		element = getElements(driver,By.CLASS_NAME,"response-container-content",20)
		temp = element[len(element)-1]
	element = temp
	html_value = element.get_attribute("innerHTML")
	while len(html_value) < 10  and ("I'm Bard" not in html_value):
		element = getElement(driver,By.CLASS_NAME,"response-container-content",2)
		try:
			html_value = element.get_attribute("innerHTML")
		except:
			1==1

	soup = BeautifulSoup(html_value, 'html.parser')


	formatted_strings = [string.strip() for string in soup.strings if string.strip()]

	list = []
	for string in formatted_strings:
		list.append(string)
	for i in range(0,len(list)-5):
		print(list[i])
	cookies = driver.get_cookies()
	save_driver(cookies)
helper()
	    













