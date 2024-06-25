<p align="center">
  <picture>
  <source media="(prefers-color-scheme: light)" srcset="/static/assets/MercuryLight.png">
  <source media="(prefers-color-scheme: dark)" srcset="/static/assets/MercuryDark.png">
  <img alt="Logo">
</picture>
</p>


# Mercury: A Quick Commerce Scraper
Mercury is an Indian quick-commerce scraper which scrapes real-time prices of products from popular platforms like DMart, Blinkit, and BigBasket. This tool enables users to compare prices across multiple e-grocery services instantly, helping them make informed purchasing decisions.

### Currently Supported Sites: 
* Blinkit
* Bigbasket
* DMart

### Prerequisites/dependencies:
1. Python:
   - Flask
   - Selenium
   - Requests
   - BeautifulSoup (bs4)
2. Firefox web browser (or any other Gecko based browser)

### Instructions for running locally:
1. Clone this repository.
2. Open a terminal cmd window at the root of the cloned repository and install all python pre-requisites by running:
```bash
pip install -r requirements.txt
```

3. Run `Run_Mercury.bat`. The site should open in a new browser window.
4. Enter pincode on the website.
5. Wait untill availablity of services is verified.
6. Enter your search term in the searchbar.
7. Wait untill data is fetched.
8. The final output will be displayed as a datatables table, already sorted by price.

###Troubleshooting
**1. Browser window does not open automatically when ```Run_Mercury.bat``` is run.**
- This may occur because the webbrowser library may not have recognised your browser.
Manually open ```localhost:*port_num*``` where ```port_num``` is the value of ```SetPort``` variable in app.py (5000 by default)

**2. Website does not load or connection gets timed out.**
- This usually occurs because the server may not have started properly. To solve this, change the ```SetPort``` variable in app.py to change the port and re-run the code.