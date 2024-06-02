import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException 
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json
import re

def typeSim(element, text, delay=0.05):
    for character in text:
        ActionChains(driver).move_to_element(element).click().send_keys(character).perform()
        time.sleep(delay)

def bigSearch(driver):
    searchbar = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[1]/header[2]/div[1]/div[1]/div/div/div/div/input')))
    searchbar.click()
    searchbar.clear()
    searchbar.send_keys(productName)
    searchbar.send_keys(Keys.RETURN)
    productInfo(driver)

def productInfo(driver):

    WebDriverWait(driver, 1).until(EC.any_of(
                                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[5]/div[2]/section[2]/section/ul/li[3]/div/div/h3/a/div/h3')),
                                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[6]/div[2]/section[2]/section/ul/li[3]/div/div/h3/a/div/h3'))))
    driver.execute_script("window.scrollBy(0, 200);") 
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    all_products = soup.find_all('a', {'class': 'h-full'})
    product_data = []
    products = all_products[:2]

    # finds multiple products
    for i, product in enumerate(products, start=1):
        brand_name = product.find('span', class_='Label-sc-15v1nk5-0 BrandName___StyledLabel2-sc-hssfrl-1 gJxZPQ keQNWn')
        brand = brand_name.text.strip() 
        prod_name = product.find('h3', class_ ='block m-0 line-clamp-2 font-regular text-base leading-sm text-darkOnyx-800 pt-0.5 h-full')
        prod = prod_name.text.strip()
        title = f"{brand} {prod}"
        product_link = "bigbasket.com" + product['href']
        
        # button XPATH config 
        basePath = "/html/body/div[2]/div[1]/div[5]/div[2]/section[2]"
        discPath = "/div/section/ul"
        actPath = "/section/ul"
        clickNo = f"/li[{i}]"
        buttonPath = "/div/div/h3/div[2]/div/div/button"
        singlePath = "/div/div/h3/div[2]/span/span"
        variants = []

        try : 
            wait = WebDriverWait(driver, 1)
            button_element = wait.until(
            EC.any_of(
                EC.element_to_be_clickable((By.XPATH, f"{basePath}{actPath}{clickNo}{buttonPath}")),
                EC.element_to_be_clickable((By.XPATH, f"{basePath}{discPath}{clickNo}{buttonPath}"))))
            button_element.click()

            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".gTObZp > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)")))
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            pretty_html = soup.prettify()
            with open("op3.html", "w", encoding="utf-8") as f:
                f.write(pretty_html)
            

            for variant_div in soup.find_all('li', role="option"):

                quantity_div = variant_div.find('div', class_='w-3/4 mb-1.5 truncate text-md leading-xss text-darkOnyx-800')
                quantity = quantity_div.text.strip() if quantity_div else None

                price_div = variant_div.find('span', class_='Label-sc-15v1nk5-0 PackChanger___StyledLabel4-sc-newjpv-6 gJxZPQ ixfMcs')
                price = price_div.text.strip() if price_div else None
                
                if quantity and price:
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
            
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) :

            quantity_div = soup.find('div', class_='py-1.5 xl:py-1')
            label_span = quantity_div.find('span', class_='Label-sc-15v1nk5-0 PackSelector___StyledLabel-sc-1lmu4hv-0 gJxZPQ fnsuXg')
            quantity_span = label_span.find('span', class_='Label-sc-15v1nk5-0 gJxZPQ truncate')
            if quantity_span:
                quantity = quantity_span.text.strip()
            else:
                print("Could not find the quantity element on the page.")
            
            outer_div = soup.find('div', class_='flex flex-col gap-0.5')
            inner_div = outer_div.find('div', class_='Pricing___StyledDiv-sc-pldi2d-0')
            price_elem = inner_div.find('span', class_='Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi')
            if price_elem:
                price = price_elem.text.strip()
            else:
                print("Could not find the price element on the page.")
            
            variant_dict = {'quantity': quantity, 'price': price}
            
            variants.append(variant_dict)
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


        with open("outputbig.json", "w", encoding="utf-8") as json_file:
            json.dump(product_data, json_file, ensure_ascii=False, indent=4)

while True:
    pincode = input("Enter Pincode: ")
    if pincode.isdigit():
        break
    else:
        print("Invalid Pincode. Please enter only digits.")

productName = input("Enter Product Name: ")


options = Options() 
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)
# driver = webdriver.Firefox()
driver.get("https://bigbasket.com")
driver.implicitly_wait(2)

addressClick = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[1]/header[2]/div[1]/div[2]/div[1]/div/div/button/span')))
addressClick.click()

addressBar = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/header[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div[2]/input')
typeSim(addressBar, pincode[:3])

reAddressBar = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/header[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div[2]/input')
typeSim(reAddressBar, pincode[-3:])
time.sleep(1)
addressSuggestion = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/header[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div[3]/ul/li[1]')
addressSuggestion.click()

try:
    unserviceableAddress = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div[2]/span')))
    print("Sorry for the inconvenience, BigBasket doesn't deliver at your location.")
    driver.quit()
except (TimeoutException, NoSuchElementException):
    print("Delivery available at your location, please enter the name of your desired product.")
    bigSearch(driver)