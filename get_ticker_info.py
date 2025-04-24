from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_ticker_info(ticker):
    
    # Chrome Settings
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--headless=true")

    time.sleep(5)

    # Getting investidor10 page
    driver = webdriver.Chrome(options=options)
    driver.get("https://investidor10.com.br/acoes/"+ticker)

    time.sleep(5)

    # HTMLdoc
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Getting html elements : "indicator" div and "cell" divs.
    html_indicators_section = soup.find(attrs={"id":"table-indicators"})
    html_indicators_cells = html_indicators_section.find_all(attrs={"class":"cell"})

    # Getting html elements : "info_about" and "cells" divs.
    html_info_about_section = soup.find(attrs={"id":"info_about"})
    html_info_about_cells = html_info_about_section.find_all(attrs={"class":"cell"})

    # Dictionary to store values
    indicators_values = {}

    # Filling dictionary with indicators
    for indicator in html_indicators_cells:
        name = indicator.find(name="span").contents[0]
        value = indicator.find(name="div").find("span").contents[0]

        name = str(name).lower()
        value = str(value).strip()

        indicators_values.update({name: value})

    # Filling dictionary with info about ticker
    for info in html_info_about_cells:
        name = info.find(attrs={"class":"title"}).contents[0]
        value = info.find(attrs={"class":"detail-value"})

        name = str(name).lower()
        value = str(value).strip()
        value = value[value.find(">"):]
        value = value[:value.find("<")+1]

        if(value != ""):
            indicators_values.update({name: value})
    
    driver.quit()

    return indicators_values
# END