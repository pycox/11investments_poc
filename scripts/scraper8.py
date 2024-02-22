from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readHistory, updateHistory, readUrl, updateDB
import time


def main():
    key = 8
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
        
    time.sleep(4)
    
    items = driver.find_elements(By.CSS_SELECTOR, "div.opening")
    
    newHist = []
    
    data = []
    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        
        if not link in readHistory(key):
            data.append([
                item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                com,
                'US',
                link
            ])
        
        newHist.append(link)
        
    updateDB(data)
    
    updateHistory(f'{key}', newHist)


if __name__ == "__main__":
    main()