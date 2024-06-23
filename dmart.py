import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json
import re

def dmartSearch(productName):
    global driver
    time.sleep(2)
    searchBar = driver.find_element(By.XPATH, '//*[@id="scrInput"]')
    searchBar.send_keys(productName)
    searchBar.send_keys(Keys.RETURN)
    productInfo(driver)


def productInfo(driver):
        
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/main/div/div/div[1]/div/div[2]/div')))

    driver.execute_script("window.scrollBy(0, 200);")  # scrolls window to reach the clickable element
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')  # parses webpage in a condition from which title can be extracted
    all_products = soup.find_all('div', {'class': 'vertical-card_title-container__fSfVD'}) 
    product_data = []
    products = all_products[:2] 
    
    for i, product in enumerate(products, start=1):

        title_raw = product.find('div', class_='vertical-card_title__pMGg9')
        title_raw = title_raw.text.strip()
        
        title = re.sub(r' :.*', '', title_raw)
        
        clickBase = "/html/body/div[1]/div[1]/main/div/div"
        clickNo = f"/div[{i}]"
        clickEnd = "/div/div[4]/div/div/div/div"
        variants = []
        
        try:
            variant_button = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH, f"{clickBase}{clickNo}{clickEnd}")))
            time.sleep(1)
            variant_button.click()
        except ElementClickInterceptedException:
            continue
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
               
        # for handling quantities
        def QuantityHandler(quantity_raw, price_per_unit_raw):
    
            quantity_match = re.search(r'(\d+(\.\d+)?)\s*([a-zA-Z]+)', quantity_raw)
            price_match = re.search(r'(\d+(\.\d+)?)\s*/\s*1\s*([a-zA-Z]+)', price_per_unit_raw)
            
            if quantity_match and price_match:
                quantity, unit = float(quantity_match.group(1)), quantity_match.group(3).lower()
                price_unit = price_match.group(3).lower()
                
                if unit in ['kg', 'l']:
                    quantity *= 1000
               
                if price_unit in ['kg', 'l']:
                    price_per_unit_raw = re.sub(r'[^\d.]', '', price_per_unit_raw)  
                    return quantity, float(price_per_unit_raw) / 1000  
                
                return quantity, float(re.sub(r'[^\d.]', '', price_per_unit_raw))
            return 0.0, 0.0  

        
        variant_ul = soup.find('ul', class_='MuiList-root MuiList-padding MuiMenu-list mui-style-r8u8y9')
        for variant_li in variant_ul.find_all('li', role='option'):
            
            price_per_unit_raw = variant_li.find('span', class_='bootstrap-select_infoTxt-value__kT4zZ').text.strip()
            quantity_raw = variant_li.find('span', style='padding-left: 0px;').text.strip()
            
            quantity, priceInt = QuantityHandler(quantity_raw, price_per_unit_raw)

            price = round(quantity * priceInt)
            price = f"{price}"
                    
            variant_dict = {'quantity': quantity_raw, 'price': price , 'Link' : "no link"}
            variants.append(variant_dict)
        
        try:
            button_close = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]')
            button_close.click()
        except:
            print(f"Could not find close button for product {i}")
        
        # Add all variants for this product to product_data
        for variant in variants:
            product_data.append({
                "title": title,
                "quantity": variant["quantity"],
                "price": variant["price"],
                #"price per unit": variant["price per unit"]
                "link": "No link"
            })
    
    with open("dmartOP.json", "w", encoding="utf-8") as json_file:
        json.dump(product_data, json_file, ensure_ascii=False, indent=4)   


def DmartCheckAvailability(pincode):
    global driver, addressBar, unserviceableAddress
    options = Options() 
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Firefox()
    driver.get("https://dmart.in")
    driver.implicitly_wait(2)

    addressBar = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pincodeInput"]')))
    addressBar.send_keys(pincode)

    try : 
        unserviceableAddress = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[2]/div[2]/div/div[2]/p[1]')))
        print ("Dmart, doesn't deliver at your location.")
        driver.quit()

    except (TimeoutException,NoSuchElementException) : 
        addressSuggestion = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li[1]/button')))
        addressSuggestion.click()
        addressConfirmation = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[2]/div[2]/div[2]/div/div[2]/button')))
        addressConfirmation.click()
        print("Delivery Available on Dmart")

#Manual input for testing
if __name__ == "__main__":
    print("running as main: ")
    x=str(input("Pincode: "))
    DmartCheckAvailability(x)
    y=str(input("search term: "))
    dmartSearch(y)
