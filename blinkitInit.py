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


def blinkSearch(driver):
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/header/div[2]/a/div[2]/div').click()
        searchbar=driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/header/div[2]/div/input')
        searchbar.clear()
        searchbar.send_keys(productName)
        BlinkfirstResult()
        BlinkSecondResult()
           
def BlinkfirstResult():
        blinkR1Title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[1]/div/div[2]/div[2]/div[1]/div[1]').text
        #checks if qty is not a drop down, if true, fetch price and qty directly
        if len(driver.find_elements(By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[1]/div/div[2]/div[2]/div[1]/div[2]/span'))>0:
               blinkR1Q1=driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[1]/div/div[2]/div[2]/div[1]/div[2]/span').text
               blinkR1Q1prc=driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[1]/div/div[2]/div[2]/div[2]/div[1]/div').text
        #if above conditonal is false, proceeds to click on dropdown menu and fetches price and qty from the popup menu      
        else:
               blinkR1QuantityDropdown = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[1]/div/div[2]/div[2]/div[1]/div[2]/div').click()
               blinkR1Q1 = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[1]/div/div[1]/div[2]').text
               blinkR1Q1prc = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div').text
        if len(driver.find_elements(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]'))>0:
                blinkR1Q2 = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]')
                blinkR1Q2prc = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div')
        blinkR1OP = f"1) {blinkR1Q1} {blinkR1Title} @ {blinkR1Q1prc}"
        if 'BlinkR1Q2' in locals():
                blinkR1OP = f"1) {blinkR1Title} is available in following packs : {blinkR1Q1} @ {blinkR1Q1prc} ; {blinkR1Q2} @ {blinkR1Q2prc} "
        print(blinkR1OP)


def BlinkSecondResult():
        blinkR2Title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[2]/div/div[2]/div[2]/div[1]/div[1]').text
        if len(driver.find_elements(By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[2]/div/div[2]/div[2]/div[2]/div[2]/span'))>0:
               blinkR2Q1=driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[2]/div/div[2]/div[2]/div[1]/div[2]/span').text
               blinkR2Q1prc=driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[2]/div/div[2]/div[2]/div[2]/div[1]/div').text      
        else:
               blinkR2QuantityDropdown = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[2]/div/div[2]/div[2]/div[1]/div[2]/div').click()
               blinkR2Q1 = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[1]/div/div[1]/div[2]').text
               blinkR2Q1prc = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div').text
                
        if len(driver.find_elements(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]'))>0:
                        blinkR2Q2 = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]').text
                        blinkR2Q2prc = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div').text
                
        blinkR2OP = f"2) {blinkR2Q1} {blinkR2Title} @ {blinkR2Q1prc}"
        if 'blinkR2Q2' in locals():
                blinkR2OP = f"2) {blinkR2Title} is available in following packs : {blinkR2Q1} @ {blinkR2Q1prc} ; {blinkR2Q2} @ {blinkR2Q2prc} "
        print(blinkR2OP)


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

addressBar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input')
addressBar.clear()
typeSim(addressBar, pincode[:3])

reAddressBar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input')
typeSim(reAddressBar, pincode[-3:])
time.sleep(1)
addressSuggestion = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div[1]')
addressSuggestion.click()

try:
    unserviceableAddress = WebDriverWait(driver, 3).until(  
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[2]/div/div/div/div')))

    print("Sorry for the inconvenience, Blinkit doesn't deliver at your location.")
    driver.quit()
except (TimeoutException, NoSuchElementException):
                print("Delivery available at your location, fetching relevant results.")
                blinkSearch(driver)