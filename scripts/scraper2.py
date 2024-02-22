from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readHistory, updateHistory, readUrl, updateDB
import time


def main():
    key = 2
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    time.sleep(4)
    
    try:
        driver.find_element(By.CSS_SELECTOR, "a#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection").click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
        
    time.sleep(4)
    
    items = driver.find_elements(By.CSS_SELECTOR, "li.whr-item")
    
    newHist = []
    
    data = []
    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        
        if not link in readHistory(key) and item.find_element(By.CSS_SELECTOR, "li.whr-location").text.strip() in ['London', 'New York']:
            data.append([
                item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                com,
                item.find_element(By.CSS_SELECTOR, "li.whr-location").text.strip(),
                link
            ])
        
        newHist.append(link)
        
    updateDB(data)
    
    updateHistory(f'{key}', newHist)


if __name__ == "__main__":
    main()