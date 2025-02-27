import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


# Before you continue to Google -> We use cookies and data to...
def handle_cookie_window(browser):
    first_form = browser.find_element(By.TAG_NAME, "form")
    action = first_form.get_attribute("action")
    if action != "https://consent.google.com/save":
        return
    button = first_form.find_element(By.CSS_SELECTOR, "button")
    button.click() # click reject all


def parse_links(links):
    data = []    
    for a in links:
        href = a.get_attribute("href")
        if href != None and href.startswith("https://www.google.com/finance/quote/"):
            d = parse_link(a)            
            data.append(d)
    return data

def parse_link(a): 
    #a.screenshot("link.png")    
    divs = a.find_elements(By.TAG_NAME, "div")        
    data = divs[0].text.split("\n")
    instrument = data[0]
    value = data[1]
    movement = data[2]
    movement2 = data[3]
    return (instrument, value, movement, movement2)


# hide broswer
os.environ['MOZ_HEADLESS'] = '1'
browser = webdriver.Firefox()

#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")
#driver = webdriver.Chrome(options=chrome_options)
#browser = webdriver.Chrome()

browser.get("https://www.google.com/finance/")

handle_cookie_window(browser)

c_wiz = browser.find_elements(By.TAG_NAME, "c-wiz")[2]
#c_wiz.screenshot("test.png")
c_wiz_divs = browser.find_elements(By.TAG_NAME, "div")

currency_div = None
crypto_div = None
for div in c_wiz_divs:
    if div.text == "Currencies":        
        currency_div = div        
    if div.text == "Crypto":        
        crypto_div = div        
    if currency_div != None and crypto_div != None:
        break


tab = False
try:
    import tabulate
    tab = True
except ModuleNotFoundError:
    pass

currency_div.click()
links = c_wiz.find_elements(By.TAG_NAME, "a")
currencies = parse_links(links)
df = pd.DataFrame(currencies)
df.columns = ["Currency", "price", "movement in %", "movement"]
df.set_index("Currency", inplace=True)
print(df.to_markdown()) if tab else print(df.to_string())

print("")

crypto_div.click()
links = c_wiz.find_elements(By.TAG_NAME, "a")
crypto = parse_links(links)
df = pd.DataFrame(crypto)
df.columns = [ "CryptoCurrency", "price", "movement in %", "movement"]
df.set_index("CryptoCurrency", inplace=True)
print(df.to_markdown()) if tab else print(df.to_string())

browser.quit()