import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.options import Options 
from bs4 import BeautifulSoup
# options = Options() 
# options.add_argument("-headless")
# options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0")
# options.add_argument("--disable-blink-features=AutomationControlled")

def typeSim(element, text, delay=0.05):
    for character in text:
        ActionChains(driver).move_to_element(element).click().send_keys(character).perform()
        time.sleep(delay)

def blinkSearch(driver):
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/header/div[2]/a/div[2]/div').click()
    searchbar = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/header/div[2]/div/input')
    searchbar.clear()
    searchbar.send_keys(productName)
    productInfo(driver)

    
def productInfo(driver):
    wait = WebDriverWait(driver, 1)
    wait.until(EC.any_of(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[4]/div/div[3]/div[2]/div[1]/div[1]")),
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[4]/div/div[2]/div[2]/div[1]/div[1]"))))
    
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    all_products = soup.find_all('a', {'data-test-id': 'plp-product'})
    products = all_products[:4]  

    for i, product in enumerate(products, start=1):
        
        # Extract Title
        title_elem = product.find('div', class_='Product__UpdatedTitle-sc-11dk8zk-9')
        title = title_elem.text.strip() if title_elem else "Title Not Found"
        
        # Extract Quantity (both single and dropdown)
        quantity_elements = product.find_all(
            class_=['plp-product__quantity--box', 'bff_variant_text_only plp-product__quantity--box'])
        quantity = quantity_elements[0].text.strip() if quantity_elements else "Quantity Not Found"

        # Extract Price (handling missing price element and potential offer price)
        price_elem = product.find('div', style='color: rgb(31, 31, 31); font-weight: 600; font-size: 12px;')
        if price_elem:
            price = price_elem.text.strip()
        else:
            offer_price_elem = product.find('div', style='color: rgb(130, 130, 130); font-weight: 400; font-size: 12px; text-decoration-line: line-through;')
            price = offer_price_elem.find_previous_sibling('div').text.strip() if offer_price_elem else "Price Not Found"

        print(f"{i}) {title} {quantity} @ {price}")  

    
while True:
    pincode = input("Enter Pincode : ")
    if pincode.isdigit():
        break
    else:
        print("Invalid Pincode. Please enter only digits.")

driver = webdriver.Firefox()
# driver = webdriver.Firefox(options=options) 
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
    print("Delivery available at your location, please enter the name of your desired product.")
    productName = input("Enter Product Name : ")
    blinkSearch(driver)