from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_binance_announcements():
    # Initialize Chrome options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    print("Getting Chrome driver")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print("Got Chrome driver")
    
    try:
        print("Starting")
        driver.get('https://www.binance.com/en')
        
        # Wait until the announcements tab is loaded
        tab_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bn-tab'))
        )
        print("Found announcements tab")
        
        # Find and click the "New Listing" tab (second child)
        new_listing_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.bn-tab-list > div:nth-child(2)'))
        )
        new_listing_tab.click()
        print("Clicked on New Listing")
        
        # Wait for announcements to load and get them
        announcements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, 
                'div.flex.flex-col.items-start.mobile\\:items-center.mobile\\:gap-\\[24px\\].noH5\\:gap-\\[20px\\].w-full.flex-initial.tablet\\:w-auto.tablet\\:flex-1 a div >:nth-child(2)'
            ))
        )
        
        # Extract text from announcements and clean the coin names
        coin_listings = []
        for announcement in announcements:
            text = announcement.text
            # Extract just the coin name from announcements
            if "(" in text and ")" in text:
                coin = text[text.find("(")+1:text.find(")")]
                coin_listings.append(coin)
        
        print(f"Found {len(coin_listings)} new coin listings:")
        for coin in coin_listings:
            print(f"- {coin}")
            
        return coin_listings
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
        
    finally:
        driver.quit()
        print("Browser closed")