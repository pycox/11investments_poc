from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readHistory, updateHistory, readUrl, updateDB
import time


def main():
    key = 6
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
            
            items = driver.find_elements(By.CSS_SELECTOR, "div.job-summary")
            
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                location = item.find_element(By.CSS_SELECTOR, 'p').text.strip()
                                
                if not link in readHistory(key) and location.split(',')[-1].strip() in ['United States', 'United Kingdom']:
                    data.append([
                        item.find_element(By.CSS_SELECTOR, 'h2').text.strip(),
                        com,
                        location,
                        link
                    ])
                    
                newHist.append(link)
                
            if len(driver.find_elements(By.CSS_SELECTOR, "li.page-next")) > 0: 
                driver.find_element(By.CSS_SELECTOR, "li.page-next").click()
                i = i + 1
            else: 
                flag = False
                break
        except:
            flag = False
            
    updateDB(data)
    
    updateHistory(f'{key}', newHist)
    
    
if __name__ == "__main__":
    main()
    
    
    