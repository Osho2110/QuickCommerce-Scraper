import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchElementException

def typeSim(element, text, delay=0.05):
        for character in text:
                ActionChains(driver).move_to_element(element).click().send_keys(character).perform()
                time.sleep(delay)


while True:
    pincode = input("Enter Pincode : ")
    if pincode.isdigit():
        break  
    else:
        print("Invalid Pincode. Please enter only digits.")
productName = input("Enter Product Name : ")
driver = webdriver.Firefox()
driver.get("https://blinkit.com")
driver.implicitly_wait(2)

def unserviceableAdressLocated():
      try:
        unserviceableAddress = WebDriverWait(driver, 3).until(  
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[2]/div/div/div/div')))
        return False
      except (TimeoutException,NoSuchElementException):
        return True

def addressIn():
        addressBar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input')
        addressBar.clear()
        typeSim(addressBar, pincode[:3])

        reAddressBar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input')
        typeSim(reAddressBar, pincode[-3:])

        addressSuggestion = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div[1]')
        addressSuggestion.click()
        isServiceable = unserviceableAdressLocated()
        blinkSearch()
        if not isServiceable:
                addressRe()

def addressRe():
       pincodeRe = int(pincode)
       pincodeRe = pincodeRe+1
       pincodeRe = str(pincodeRe)
       addressBar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input')
       typeSim(addressBar, Keys.BACK_SPACE * 6)
       time.sleep(2)
       typeSim(addressBar, pincodeRe[:3])

       reAddressBar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input')
       typeSim(reAddressBar, pincodeRe[-3:])
       addressSuggestion = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div[1]')
       addressSuggestion.click()
       isNewServiceable = unserviceableAdressLocated()
       if not isNewServiceable:
             print("Sorry for the inconvenience, Blinkit doesn't deliver at your location.")
       else: 
             print("Delivery available at your location, fetching relevant results.")
             waitForSearchBar = WebDriverWait(driver, timeout=None).until(  
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/header/div[2]/a/div[2]/div')))
             blinkSearch()
             


def blinkSearch():
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/header/div[2]/a/div[2]/div').click()
        searchbar=driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/header/div[2]/div/input')
        searchbar.clear()
        searchbar.send_keys(productName)
        BlinkfirstResult()
        
                
def BlinkfirstResult():
        blinkR1Title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[1]/div/div[2]/div[2]/div[1]/div[1]').text
        blinkR1Quantity = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[1]/div/div[2]/div[2]/div[1]/div[2]/div').click()
        BlinkR1Q1 = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[1]/div/div[1]/div[2]').text
        BlinkR1Q1prc = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div').text
        BlinkR1OP = f"Product Info : {BlinkR1Q1} {blinkR1Title} @ {BlinkR1Q1prc}"
        try : 
                BlinkR1Q2 = WebDriverWait(driver,0).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]'))).text
                BlinkR1Q2prc = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div').text
        except (NoSuchElementException) :
                pass
        print(BlinkR1OP)

addressIn()



         