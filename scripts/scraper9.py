from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readHistory, updateHistory, readUrl, updateDB
import time


def main():
    key = 9
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    
    time.sleep(4)
    
    # try:
    #     driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler").click()
    # except Exception as e:
    #     print(f'Scraper{key} cookiee button: {e}')
    
    driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='distanceLocation']").click()
    time.sleep(2)
    scrollDom = driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='filterMenu']")
    driver.execute_script('arguments[0].scrollTop = 400', scrollDom)
    time.sleep(2)
    driver.find_element(By.XPATH, "//label[contains(text(), 'United Kingdom')]").click()
    time.sleep(4)
    driver.find_element(By.XPATH, "//label[contains(text(), 'United States')]").click()
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='viewAllJobsButton']").click()
    
    flag = True
    data = []
    newHist = []
    
    time.sleep(4)
    
    while flag:
        try:
            time.sleep(4)
            
            items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
            
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                                
                if not link in readHistory(key):
                    data.append([
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        item.find_element(By.CSS_SELECTOR, "dd").text.strip(),
                        link
                    ])
                    
                newHist.append(link)
                
            if len(driver.find_elements(By.CSS_SELECTOR, "button[data-uxi-element-id='next']")) > 0: 
                driver.find_element(By.CSS_SELECTOR, "button[data-uxi-element-id='next']").click()
            else: 
                flag = False
                break
        except Exception as e:
            print(e)
            flag = False
            
    updateDB(data)
    
    updateHistory(f'{key}', newHist)
    
    
if __name__ == "__main__":
    main()
    
    
    