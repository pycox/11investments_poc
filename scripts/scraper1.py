from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readHistory, updateHistory, readUrl, updateDB
import time


def main():
    key = 1
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(f"{url}")
    
    time.sleep(4)
    
    try:
        driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler").click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
    
    flag = True
    data = []
    newHist = []
    i = 1
    
    time.sleep(4)
    
    while flag:
        try:
            driver.get(f"{url}?page={i}")
            
            time.sleep(4)
            
            if len(driver.find_elements(By.CSS_SELECTOR, "td.search-listing__table__no-result")) > 0: 
                flag = False
                break
            
            items = driver.find_elements(By.CSS_SELECTOR, "tr.jobPostingsRow")
            
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                
                cells = item.find_elements(By.CSS_SELECTOR, "td")
                                
                if not link in readHistory(key) and cells[2].text.strip()[:2] in ['US', 'UK']:
                    data.append([
                        cells[0].text.strip(),
                        com,
                        cells[2].text.strip(),
                        link
                    ])
                
                newHist.append(link)
            
            i = i + 1
        except:
            flag = False
            
    updateDB(data)
    
    updateHistory(f'{key}', newHist)
    
    
if __name__ == "__main__":
    main()
    
    
    