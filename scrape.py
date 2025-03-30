import time
import pandas 
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


## GET BOOKING.COM REQUEST
search_url = "https://www.booking.com"
page = requests.get(search_url)
print(page.text)

# driver.get(search_url)
time.sleep(3)  # Allow the page to load


# SCRAPE LISTINGS
def scrape_listings(driver):
    hotelsLs = []
    
    ## GET BOOKING.COM REQUEST
    search_url = "https://www.booking.com/searchresults.en-gb.html?ss=Australia&checkin_year=2026&checkin_month=02&checkin_monthday=01&checkout_year=2026&checkout_month=02&checkout_monthday=02&group_adults=1&no_rooms=1&group_children=0&sb_lp=1"
    
    full_page = requests.get(search_url)
    print(full_page.text)

    # Scrape page HTML 
    print("Checkpoint #1: Scrape page HTML")

    # Create tmp instance of chrome for selenium
    selenium_instance  = webdriver.ChromeOptions()
    selenium_instance.add_argument("--headless")
    selenium_instance.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    web_driver = webdriver.Chrome(options=selenium_instance)
    web_driver.get(search_url)
    
    try: 
        while len(hotelsLs) < 100:
            listings = driver.find_elements(By.CLASS_NAME, "sr_property_block")
            print("Checkpoint #2")

            for listing in listings:
                try:
                    title = listing.find_element(By.CLASS_NAME, "sr-hotel__name").text
                    address = listing.find_element(By.CLASS_NAME, "sr_card_address_line").text
                    room_type = listing.find_element(By.CLASS_NAME, "room_link").text
                    price = listing.find_element(By.CLASS_NAME, "bui-price-display__value").text
                    review_score = listing.find_element(By.CLASS_NAME, "bui-review-score__badge").text
                    num_reviews = listing.find_element(By.CLASS_NAME, "bui-review-score__text").text

                    hotelsLs.append([title, address, room_type, price, review_score, num_reviews])
                except:
                    continue
    except Exception as e:
        print(f"Err: {e}")
    finally:
        driver.quit()

    return pandas.DataFrame(hotelsLs, columns=["Title" , "Address", "Headline Room Type", "Cost (AUD)", "Review Score", "# of Reviews"])



# CSV functionality
# data = pandas.DataFrame(hotelsLs, columns=["Title" , "Address", "Headline Room Type", "Cost (AUD)", "Review Score", "# of Reviews"])
filename = 'test.csv'
print("Checkpoint #3: " + filename)
# data.convertToCSV(filename, index=False)
print("Data officialy scraped!")