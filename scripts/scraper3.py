from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readHistory, updateHistory, readUrl, updateDB
import time


def main():
    key = 3
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(f"{url}")
    
    time.sleep(4)
    
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'I give consent to use cookies')]").click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
    
    flag = True
    data = []
    newHist = []
    
    time.sleep(4)
    
    while flag:
        try:
            time.sleep(4)
            
            items = driver.find_elements(By.CSS_SELECTOR, "li.flx-card")
            
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                                
                if not link in readHistory(key):
                    data.append([
                        item.find_element(By.CSS_SELECTOR, "div").text.strip(),
                        com,
                        driver.find_element(By.CSS_SELECTOR, '.fa-map-marker + span').find_element(By.XPATH, '..').text.strip(),
                        link
                    ])
                
                newHist.append(link)
            
            nextBtn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next page"]')

            if nextBtn.is_enabled():
                nextBtn.click()
            else:
                flag = False
        except:
            flag = False
            
    updateDB(data)
    
    updateHistory(f'{key}', newHist)
    
    
if __name__ == "__main__":
    main()
    
    
    