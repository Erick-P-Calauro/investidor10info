from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from conversion import convert

def get_ticker_info(ticker):
    
    DELAY = 10 # Seconds

    # Chrome Settings
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--headless=true")

    time.sleep(DELAY)

    # Getting investidor10 page
    driver = webdriver.Chrome(options=options)
    driver.get("https://investidor10.com.br/acoes/"+ticker)

    time.sleep(DELAY)

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

    # Getting and parsing html price element
    html_price = soup.find(attrs={"class":"_card cotacao"})
    name = "cotação"
    value = str(html_price.find(attrs={"class", "value"}))
    value = value[value.find("$")+2:value[1:].find("<")+1]
    indicators_values.update({name: convert(value)})

    # Getting and parsing html dy element
    html_dy = soup.find(attrs={"class": "_card dy"})
    name = "dy"
    value = str(html_dy.find_all(name="span")[1].contents[0])
    indicators_values.update({name: convert(value)})

    # Filling dictionary with indicators
    for indicator in html_indicators_cells:
        name = indicator.find(name="span").contents[0]
        value = indicator.find(name="div").find("span").contents[0]

        name = str(name).lower().strip()
        value = str(value).strip()

        indicators_values.update({name: convert(value)})

    # Filling dictionary with info about ticker
    for info in html_info_about_cells:
        name = str(info.find(attrs={"class":"title"}).contents[0]) # It is a string value
        value = info.find(attrs={"class":"value"}) # Can be a <span> with divs or a span with a text value

        if(value.find(attrs={"class":"detail-value"}) == None): # value == <span class="value">""</span>
            value =  str(value.contents[0]).strip()
        else: # value == <span class="value"><div>""</div></span>
            value = str(value.find(attrs={"class":"detail-value"}).contents[0])
            
            startIndex = value.find(">") + 1
            endIndex = value[1:].find("<")
            moneyIndex= value.find("$")

            if(moneyIndex != -1):
                startIndex = moneyIndex + 2

            value = value[startIndex:endIndex].strip()
        # END IF

        # value = convert(value)
        indicators_values.update({name.lower().strip(): convert(value)})
    
    driver.quit()

    return indicators_values
# END