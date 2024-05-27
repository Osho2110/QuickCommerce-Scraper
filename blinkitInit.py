import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json

def typeSim(element, text, delay=0.05):
    for character in text:
        ActionChains(driver).move_to_element(element).click().send_keys(character).perform()
        time.sleep(delay)

def blinkResultCross():
    blinkCross = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ProductVariantModal__AddCrossIcon-sc-7k6v9m-14')))
    blinkCross.click()

def blinkSearch(productName):
    global driver
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/header/div[2]/a/div[2]/div').click()
    searchbar = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/header/div[2]/div/input')
    searchbar.clear()
    searchbar.send_keys(productName)
    productInfo(driver)

def productInfo(driver):
    wait = WebDriverWait(driver, 1)
    wait.until(EC.any_of(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[2]/div/div[3]/div[2]/div[1]/div[1]")),
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[2]/div/div[2]/div[2]/div[1]/div[1]"))))

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    all_products = soup.find_all('a', {'data-test-id': 'plp-product'})
    product_data = []
    products = all_products[:2]

    # finds multiple products
    for i, product in enumerate(products, start=1):
        title_elem = product.find('div', class_='Product__UpdatedTitle-sc-11dk8zk-9')
        title = title_elem.text.strip() if title_elem else "Title Not Found"
        product_link = "blinkit.com" + product['href']

        # variables for configuring multiple quantity dropdowns XPATH:
        baseClick = "/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]"
        clickNo = f"/a[{i}]"
        clickEndA = "/div/div[2]/div[2]/div[1]/div[2]/div/div[1]"
        clickEndB = "/div/div[3]/div[2]/div[1]/div[2]/div/div[1]"
        
        #checks if there are multiple product variants
        try:
            wait = WebDriverWait(driver, 1)
            element = wait.until(EC.any_of(
                    EC.element_to_be_clickable((By.XPATH, f"{baseClick}{clickNo}{clickEndA}")),
                    EC.element_to_be_clickable((By.XPATH, f"{baseClick}{clickNo}{clickEndB}"))))
            element.click()

            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ProductVariantModal__AddCrossIcon-sc-7k6v9m-14')))

            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            variants = []
            for variant_div in soup.find_all('div', style="cursor: pointer; display: flex; flex-direction: column; gap: 12px;"):
                quantity = variant_div.find('div', class_='ProductVariantModal__ProductTitle-sc-7k6v9m-5').text.strip()
                price_div = variant_div.find('div', class_='ProductVariantModal__Price-sc-7k6v9m-7')
                price = price_div.text.strip() if price_div else "N/A"
                variant_dict = {'quantity': quantity, 'price': price}
                variants.append(variant_dict)

            for variant in variants:
                product_data.append(
                    {
                        "title": title,
                        "quantity": variant["quantity"],
                        "price": variant["price"],
                        "link": product_link,
                    }
                )
            blinkResultCross()

            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

        # when no quantity button is found : 
        except (NoSuchElementException, TimeoutException):
  
            quantity_elem = product.find('span', class_='bff_variant_text_only plp-product__quantity--box')
            quantity = quantity_elem.text.strip() if quantity_elem else "N/A"
            
            price_elem = product.find('div', style='color: rgb(31, 31, 31); font-weight: 600; font-size: 12px;')
            if price_elem:
                price = price_elem.text.strip()
           
            else:
                offer_price_elem = product.find('div', style='color: rgb(130, 130, 130); font-weight: 400; font-size: 12px; text-decoration-line: line-through;')
                price = offer_price_elem.find_previous_sibling('div').text.strip() if offer_price_elem else "Price Not Found"
            
            variant_dict["quantity"] = quantity
            variant_dict["price"] = price.encode("utf-8").decode()
            product_data.append(
                {
                    "title": title,
                    "quantity": variant_dict["quantity"],
                    "price": variant_dict["price"],
                    "link": product_link,
                }
            )

    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(product_data, json_file, ensure_ascii=False, indent=4)
        
#Receives pincode from server 
def pinin(p):
   global pincode
   pincode=p
   CheckAvailability()
   

def CheckAvailability():
    global driver, addressBar, reAddressBar, unserviceableAddress
    options = Options() 
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://blinkit.com")
    driver.implicitly_wait(4)
    addressBar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input')
    addressBar.clear()
    typeSim(addressBar, pincode[:3])
    reAddressBar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input')
    typeSim(reAddressBar, pincode[-3:])
    time.sleep(1)
    addressSuggestion = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div[1]')
    addressSuggestion.click()

    try:
        unserviceableAddress = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/div[2]/div/div/div[2]/div/div/div/div')))
        print("Sorry for the inconvenience, Blinkit doesn't deliver at your location.")
        driver.quit()
    except (TimeoutException, NoSuchElementException):
        print("Delivery available at your location, please enter the name of your desired product.")
