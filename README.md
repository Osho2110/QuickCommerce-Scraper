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
3. Run `app.py` by running ```python app.py```
4. Open `localhost:5000` on your browser or follow the link in the output terminal window
5. Enter pincode on the website.
6. Wait untill availablity of services is verified.
7. Enter your search term in the searchbar.
8. Wait untill data is fetched.
9. The final output will be displayed as a datatables table, already sorted by price.

###Troubleshooting
