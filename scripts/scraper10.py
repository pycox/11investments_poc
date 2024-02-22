from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readHistory, updateHistory, readUrl, updateDB
import time


def main():
    key = 10
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(f'{url}?office=4052560002%2C4052619002')
        
    time.sleep(4)
    
    try:
        driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler").click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
        
    time.sleep(4)
    
    # driver.find_element(By.CSS_SELECTOR, "button[data-target='careers-filters']").click()
    # time.sleep(2)
        
    newHist = []
    
    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, "div.grid__item careers-listing__card")
    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        
        if not link in readHistory(key):
            data.append([
                item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                com,
                'UK',
                link
            ])
        
    driver.get(f'{url}?office=4052641002%2C4052642002%2C4052644002')
    
    time.sleep(4)
        
    items = driver.find_elements(By.CSS_SELECTOR, "div.careers-listing__card")
    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        
        if not link in readHistory(key):
            data.append([
                item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                com,
                'UK',
                link
            ])
        
        newHist.append(link)
        
    updateDB(data)
    
    updateHistory(f'{key}', newHist)


if __name__ == "__main__":
    main()