import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def typeSim(element, text, delay=0.05):
    for character in text:
        ActionChains(driver).move_to_element(element).click().send_keys(character).perform()
        time.sleep(delay)

def blinkSearch(driver):
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/header/div[2]/a/div[2]/div').click()
    searchbar = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/header/div[2]/div/input')
    searchbar.clear()
    searchbar.send_keys(productName)
    BlinkFirstResult()
    BlinkSecondResult()
    BlinkThirdResult()
    BlinkFourthResult()

def blinkResultCross():
    try:
        blinkCross = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ProductVariantModal__AddCrossIcon-sc-7k6v9m-14')))
        blinkCross.click()
    except TimeoutException:
        print("Element not clickable within timeout.")

def getProductInfo(resultNo, baseStruct, reNo, structV1, structV2):
    no_stock = False
    stockV1 = f"{baseStruct}{reNo}{structV1}{stockcheck}"
    stockV2 = f"{baseStruct}{reNo}{structV2}{stockcheck}"
    
    # checks if product is in stock
    try:
        driver.find_element(By.XPATH, stockV1)
        no_stock = True
    except NoSuchElementException:
        pass
    try:
        driver.find_element(By.XPATH, stockV2)
        no_stock = True
    except NoSuchElementException:
        pass

    if no_stock:
        return

    # finds product title
    try:
        title_v1 = f"{baseStruct}{reNo}{structV1}{ttl}"
        title = driver.find_element(By.XPATH, title_v1).text
    except NoSuchElementException:
        title_v2 = f"{baseStruct}{reNo}{structV2}{ttl}"
        title = driver.find_element(By.XPATH, title_v2).text

    no_dd_act_prc_v1 = f"{baseStruct}{reNo}{structV1}{prc}{actprc}"
    no_dd_act_prc_v2 = f"{baseStruct}{reNo}{structV2}{prc}{actprc}"
    no_dd_disc_prc_v1 = f"{baseStruct}{reNo}{structV1}{prc}{discprc}"
    no_dd_disc_prc_v2 = f"{baseStruct}{reNo}{structV2}{prc}{discprc}"
    quant_check_single_v1 = f"{baseStruct}{reNo}{structV1}{quant}{singleq}"
    quant_check_single_v2 = f"{baseStruct}{reNo}{structV2}{quant}{singleq}"
    quant_check_ddwn_v1 = f"{baseStruct}{reNo}{structV1}{quant}{ddqV1}"
    quant_check_ddwn_v2 = f"{baseStruct}{reNo}{structV2}{quant}{ddqV2}"

    # checks quantity type - dropdown / single
    try:
        q1 = driver.find_element(By.XPATH, quant_check_single_v1).text
       #checks price type - actual/discount
        try:
            q1_prc = driver.find_element(By.XPATH, no_dd_disc_prc_v1).text
        except NoSuchElementException:
            q1_prc = driver.find_element(By.XPATH, no_dd_act_prc_v1).text

    except NoSuchElementException:
        pass

    try:
        q1 = driver.find_element(By.XPATH, quant_check_single_v2).text
        try:
            q1_prc = driver.find_element(By.XPATH, no_dd_disc_prc_v2).text
        except NoSuchElementException:
            q1_prc = driver.find_element(By.XPATH, no_dd_act_prc_v2).text
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.XPATH, quant_check_ddwn_v1).click()
        q1 = driver.find_element(By.CSS_SELECTOR, ddwnQ1).text
        q1_prc = driver.find_element(By.CSS_SELECTOR, ddwnP1).text
        try:
            q2 = driver.find_element(By.CSS_SELECTOR, ddwnQ2).text
            q2_prc = driver.find_element(By.CSS_SELECTOR, ddwnP2).text
        except NoSuchElementException:
            pass
        blinkResultCross()
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.XPATH, quant_check_ddwn_v2).click()
        q1 = driver.find_element(By.CSS_SELECTOR, ddwnQ1).text
        q1_prc = driver.find_element(By.CSS_SELECTOR, ddwnP1).text
        try:
            q2 = driver.find_element(By.CSS_SELECTOR, ddwnQ2).text
            q2_prc = driver.find_element(By.CSS_SELECTOR, ddwnP2).text
        except NoSuchElementException:
            pass
        blinkResultCross()
    except NoSuchElementException:
        pass

    op = f"{resultNo}) {q1} {title} @ {q1_prc}"
    #alters o/p if there's more than 1 qty
    if 'q2' in locals():
        op = f"{resultNo}) {title} is available in following packs : {q1} @ {q1_prc} ; {q2} @ {q2_prc}"

    print(op)

def BlinkFirstResult():
    getProductInfo(1, basestruct, re1, p1structv1, p1structv2)

def BlinkSecondResult():
    getProductInfo(2, basestruct, re2, p1structv1, p1structv2)

def BlinkThirdResult():
    getProductInfo(3, basestruct, re3, p1structv1, p1structv2)

def BlinkFourthResult():
    getProductInfo(4, basestruct, re4, p1structv1, p1structv2)

re1 = "/a[1]"
re2 = "/a[2]"
re3 = "/a[3]"  # No. of result
re4 = "/a[4]"
re5 = "/a[5]"
basestruct = "/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]"  # Page 1 initial structure
p1structv1 = "/div/div[2]/div[2]"  # Type 1 product structure.
p1structv2 = "/div/div[3]/div[2]"  # Type 2 product structure.
ttl = "/div[1]/div[1]"  # TITLE (usage order : base + re[] + structv1/v2 + ttl)
stockcheck = "/div[2]/div[2]/span"
quant = "/div[1]/div[2]"
singleq = "/span"  # no dropdown and single quantity
ddqV1 = "/div"  # dropdown and multiple quantities type 1
ddqV2 = "/div/div[1]"  # dropdown and multiple quantities type 2
prc = "/div[2]/div[1]"  # price
actprc = "/div"  # non-discounted price
discprc = "/div[1]"  # discounted price
ddbase = ".ProductVariantModal__BottomSection-sc-7k6v9m-2 > "
dd1 = "div:nth-child(1) > "
dd2 = "div:nth-child(2) > "
dd3 = "div:nth-child(3) > "
ddquant = "div:nth-child(1) > div:nth-child(1) > div:nth-child(2)"
ddprc = "div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)"
ddwnQ1 = ddbase + dd1 + ddquant
ddwnQ2 = ddbase + dd2 + ddquant
ddwnQ3 = ddbase + dd3 + ddquant
ddwnP1 = ddbase + dd1 + ddprc
ddwnP2 = ddbase + dd2 + ddprc
ddwnP3 = ddbase + dd3 + ddprc

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
    unserviceableAddress = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[2]/div/div/div/div')))

    print("Sorry for the inconvenience, Blinkit doesn't deliver at your location.")
    driver.quit()
except (TimeoutException, NoSuchElementException):
    print("Delivery available at your location, fetching relevant results.")
    blinkSearch(driver)