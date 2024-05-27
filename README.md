<p align="center">
  <picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/MercuryLight.png">
  <source media="(prefers-color-scheme: dark)" srcset="/assets/MercuryDark.png">
  <img alt="Logo">
</picture>
</p>


# Mercury: A Quick Commerce Scraper

### Currently Supported Sites: 
* Blinkit

### Prerequisites/dependencies:
1. Python:
   - Flask
   - Selenium
   - Requests
   - BeautifulSoup (bs4)
2. Firefox web browser (or any other Gecko based browser)
3. Node.js

### Instructions for running locally:
1. Clone this repository
2. Install all python pre-requisites by running:
```bash
pip install -r requirements.txt
```
3. Run `app.py` ONLY.
4. Open `localhost:5000` on your browser or follow the link in the output terminal window
5. Enter pincode and click on submit.
6. Wait untill availablity of services is verified.
7. Enter your search term in the searchbar and click on the magnifying glass icon.
8. Final output is currently available in the terminal.
