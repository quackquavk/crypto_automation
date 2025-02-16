from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_binance_announcements():
    # Initialize Chrome options
    options = Options()
    # Add any additional options if needed
    # options.add_argument('--headless')
    new_coins = []
    print("Getting Chrome driver")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("Got Chrome driver")
    
    try:
        print("Starting")
        driver.get('https://www.binance.com/en')
        
        tab_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bn-tab'))
        )
        print("Found announcements tab")
        
        new_listing_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.bn-tab-list > div:nth-child(2)'))
        )
        new_listing_tab.click()
        print("Clicked on New Listing")
        
        announcements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, 
                'div.flex.flex-col.items-start.mobile\\:items-center.mobile\\:gap-\\[24px\\].noH5\\:gap-\\[20px\\].w-full.flex-initial.tablet\\:w-auto.tablet\\:flex-1 a div >:nth-child(2)'
            ))
        )
        
        announcement_texts = [announcement.text for announcement in announcements]
        print(f"Found {len(announcement_texts)} announcements:")
        for text in announcement_texts:
            print(f"- {text}")
            new_coins.append(text)
        print(new_coins[5:])        
        return announcement_texts
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
        
    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    get_binance_announcements()