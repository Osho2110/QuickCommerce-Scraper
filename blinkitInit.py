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
        BlinkFirstResult()
        BlinkSecondResult()

def blinkResultCross(): 
    try:
        blinkCross = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ProductVariantModal__AddCrossIcon-sc-7k6v9m-14')))
        blinkCross.click()
    except TimeoutException:
        print("Element not clickable within timeout.")

# XPATH combinations - 
re1 = "/a[1]"
re2 = "/a[2]"
r3 = "/a[3]" # No. of result
re4 = "/a[4]"
re5 = "/a[5]"
basestruct = "/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]" # Page 1 initial structure
p1structv1 = "/div/div[2]/div[2]" # Type 1 product structure.
p1structv2 = "/div/div[3]/div[2]" # Type 2 product structure.
ttl = "/div[1]/div[1]" # TITLE (usage order : base + re[] + structv1/v2 + ttl)
stockcheck = "/div[2]/div[2]/span"
quant = "/div[1]/div[2]" # quantity 
singleq = "/span" # no dropdown and single quantity
ddq = "/div"      # dropdown and multiple quantities
prc = "/div[2]/div[1]" # price
actprc = "/div" # non-discounted price
discprc = "/div[1]" # discounted price
ddbase = ".ProductVariantModal__BottomSection-sc-7k6v9m-2 > "
dd1 = "div:nth-child(1) > "
dd2 = "div:nth-child(2) > "
dd3 = "div:nth-child(3) > "
ddquant = "div:nth-child(1) > div:nth-child(1) > div:nth-child(2)"
ddprc = "div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)"


def BlinkFirstResult():
        
        #checks if the product is in stock
        blinkR1nostock = False
        blinkR1stockV1 = basestruct+re1+p1structv1+stockcheck
        blinkR1stockV2 = basestruct+re1+p1structv2+stockcheck
        try:
               blinkR1stock = driver.find_element(By.XPATH,blinkR1stockV1)
               blinkR1nostock = True
        except NoSuchElementException:
                pass
        try: 
               blinkR1stock = driver.find_element(By.XPATH,blinkR1stockV2)
               blinkR1nostock = True
        except NoSuchElementException:
               pass
        
        # checks product title's length, and chooses accordingly
        try :
                blinkR1TitleV1= basestruct+re1+p1structv1+ttl
                blinkR1Title = driver.find_element(By.XPATH,blinkR1TitleV1).text
        except NoSuchElementException:
                blinkR1TitleXP2 = basestruct+re1+p1structv2+ttl
                blinkR1Title = driver.find_element(By.XPATH,blinkR1TitleXP2).text
        
        noDDactprcV1 = basestruct+re1+p1structv1+prc+actprc
        noDDactprcV2 = basestruct+re1+p1structv2+prc+actprc
        noDDdiscprcV1 = basestruct+re1+p1structv1+prc+discprc
        noDDdiscprcV2 = basestruct+re1+p1structv2+prc+discprc
        quantChecksingleV1 = basestruct+re1+p1structv1+quant+singleq
        quantChecksingleV2 = basestruct+re1+p1structv2+quant+singleq
        quantCheckddwnV1 = basestruct+re1+p1structv1+quant+ddq
        quantCheckddwnV2 = basestruct+re1+p1structv1+quant+ddq
        ddwnQ1 = ddbase+dd1+ddquant
        ddwnQ2 = ddbase+dd2+ddquant
        ddwnQ3 = ddbase+dd3+ddquant
        ddwnP1 = ddbase+dd1+ddprc
        ddwnP2 = ddbase+dd2+ddprc
        ddwnP3 = ddbase+dd3+ddprc

        
        #checks if quantity is single or in dropdown
        if len(driver.find_elements(By.XPATH,quantChecksingleV1))>0:
                blinkR1Q1 = driver.find_element(By.XPATH,quantChecksingleV1).text
                
                # checks if price is discounted or actual
                try:
                        blinkR1Q1prc = driver.find_element(By.XPATH,noDDdiscprcV1).text
                except NoSuchElementException : 
                        blinkR1Q1prc = driver.find_element(By.XPATH,noDDactprcV1).text
        
        
        elif len(driver.find_elements(By.XPATH,quantChecksingleV2))>0:
                blinkR1Q1 = driver.find_elements(By.XPATH,quantChecksingleV2)[0].text
                
                try:
                        blinkR1Q1prc = driver.find_element(By.XPATH,noDDdiscprcV2).text
                except NoSuchElementException : 
                        blinkR1Q1prc=driver.find_element(By.XPATH,noDDactprcV2).text


        elif len(driver.find_elements(By.XPATH,quantCheckddwnV1))>0:
                blinkR1QuantityDropdown = driver.find_element(By.XPATH,quantCheckddwnV1).click()
                blinkR1Q1 = driver.find_element(By.CSS_SELECTOR,ddwnQ1).text
                blinkR1Q1prc = driver.find_element(By.CSS_SELECTOR,ddwnP1).text
                try : 
                       blinkR1Q2 = driver.find_element(By.CSS_SELECTOR, ddwnQ2).text
                       blinkR1Q2prc = driver.find_element(By.CSS_SELECTOR, ddwnP2).text
                except NoSuchElementException:
                       pass
                blinkResultCross()
        
        elif len(driver.find_elements(By.XPATH, quantCheckddwnV2))>0:
                blinkR1QuantityDropdown = driver.find_element(By.XPATH,quantCheckddwnV2).click()
                blinkR1Q1 = driver.find_element(By.CSS_SELECTOR,ddwnQ1).text
                blinkR1Q1prc = driver.find_element(By.CSS_SELECTOR,ddwnP1).text
                try : 
                       blinkR1Q2 = driver.find_element(By.CSS_SELECTOR, ddwnQ2).text
                       blinkR1Q2prc = driver.find_element(By.CSS_SELECTOR, ddwnP2).text
                except NoSuchElementException:
                       pass
                blinkResultCross()

        blinkR1OP = f"1) {blinkR1Q1} {blinkR1Title} @ {blinkR1Q1prc}"
        if 'blinkR1Q2' in locals():
                blinkR1OP = f"1) {blinkR1Title} is available in following packs : {blinkR1Q1} @ {blinkR1Q1prc} ; {blinkR1Q2} @ {blinkR1Q2prc} "
        
        print(blinkR1OP)


def BlinkSecondResult():
        
        #checks if the product is in stock
        blinkR2nostock = False
        blinkR2stockV1 = basestruct+re2+p1structv1+stockcheck
        blinkR2stockV2 = basestruct+re2+p1structv2+stockcheck
        try:
               blinkR2stock = driver.find_element(By.XPATH,blinkR2stockV1)
               blinkR2nostock = True
        except NoSuchElementException:
                pass
        try: 
               blinkR2stock = driver.find_element(By.XPATH,blinkR2stockV2)
               blinkR2nostock = True
        except NoSuchElementException:
               pass
        
        # checks product title's length, and chooses accordingly
        try :
                blinkR2TitleV1= basestruct+re2+p1structv1+ttl
                blinkR2Title = driver.find_element(By.XPATH,blinkR2TitleV1).text
        except NoSuchElementException:
                blinkR2TitleXP2 = basestruct+re2+p1structv2+ttl
                blinkR2Title = driver.find_element(By.XPATH,blinkR2TitleXP2).text
        
        noDDactprcV1 = basestruct+re2+p1structv1+prc+actprc
        noDDactprcV2 = basestruct+re2+p1structv2+prc+actprc
        noDDdiscprcV1 = basestruct+re2+p1structv1+prc+discprc
        noDDdiscprcV2 = basestruct+re2+p1structv2+prc+discprc
        quantChecksingleV1 = basestruct+re2+p1structv1+quant+singleq
        quantChecksingleV2 = basestruct+re2+p1structv2+quant+singleq
        quantCheckddwnV1 = basestruct+re2+p1structv1+quant+ddq
        quantCheckddwnV2 = basestruct+re2+p1structv1+quant+ddq
        ddwnQ1 = ddbase+dd1+ddquant
        ddwnQ2 = ddbase+dd2+ddquant
        ddwnQ3 = ddbase+dd3+ddquant
        ddwnP1 = ddbase+dd1+ddprc
        ddwnP2 = ddbase+dd2+ddprc
        ddwnP3 = ddbase+dd3+ddprc

        
        #checks if quantity is single or in dropdown
        if len(driver.find_elements(By.XPATH,quantChecksingleV1))>0:
                blinkR2Q1 = driver.find_element(By.XPATH,quantChecksingleV1).text
                
                # checks if price is discounted or actual
                try:
                        blinkR2Q1prc = driver.find_element(By.XPATH,noDDdiscprcV1).text
                except NoSuchElementException : 
                        blinkR2Q1prc = driver.find_element(By.XPATH,noDDactprcV1).text
        
        
        elif len(driver.find_elements(By.XPATH,quantChecksingleV2))>0:
                blinkR2Q1 = driver.find_elements(By.XPATH,quantChecksingleV2)[0].text
                
                try:
                        blinkR2Q1prc = driver.find_element(By.XPATH,noDDdiscprcV2).text
                except NoSuchElementException : 
                        blinkR2Q1prc=driver.find_element(By.XPATH,noDDactprcV2).text


        elif len(driver.find_elements(By.XPATH,quantCheckddwnV1))>0:
                blinkR2QuantityDropdown = driver.find_element(By.XPATH,quantCheckddwnV1).click()
                blinkR2Q1 = driver.find_element(By.CSS_SELECTOR,ddwnQ1).text
                blinkR2Q1prc = driver.find_element(By.CSS_SELECTOR,ddwnP1).text
                try : 
                       blinkR2Q2 = driver.find_element(By.CSS_SELECTOR, ddwnQ2).text
                       blinkR2Q2prc = driver.find_element(By.CSS_SELECTOR, ddwnP2).text
                except NoSuchElementException:
                       pass
                blinkResultCross()
        
        elif len(driver.find_elements(By.XPATH, quantCheckddwnV2))>0:
                blinkR2QuantityDropdown = driver.find_element(By.XPATH,quantCheckddwnV2).click()
                blinkR2Q1 = driver.find_element(By.CSS_SELECTOR,ddwnQ1).text
                blinkR2Q1prc = driver.find_element(By.CSS_SELECTOR,ddwnP1).text
                try : 
                       blinkR2Q2 = driver.find_element(By.CSS_SELECTOR, ddwnQ2).text
                       blinkR2Q2prc = driver.find_element(By.CSS_SELECTOR, ddwnP2).text
                except NoSuchElementException:
                       pass
                blinkResultCross()

        blinkR2OP = f"1) {blinkR2Q1} {blinkR2Title} @ {blinkR2Q1prc}"
        if 'blinkR2Q2' in locals():
                blinkR2OP = f"1) {blinkR2Title} is available in following packs : {blinkR2Q1} @ {blinkR2Q1prc} ; {blinkR2Q2} @ {blinkR2Q2prc} "
        
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