import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


# SCRAPE LISTINGS
def scrape_listings(csv_out="listings.csv"):
    hotels = []
    
    ## GET BOOKING.COM REQUEST
    search_url = "https://www.booking.com/searchresults.en-gb.html?ss=Australia&checkin_year=2026&checkin_month=02&checkin_monthday=01&checkout_year=2026&checkout_month=02&checkout_monthday=02&group_adults=1&no_rooms=1&group_children=0&sb_lp=1"
    
    print("Checkpoint #1: Scrape page HTML")

    # Create tmp instance of chrome for selenium
    selenium_instance  = webdriver.ChromeOptions()
    selenium_instance.add_argument("--headless")
    selenium_instance.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    web_driver = webdriver.Chrome(options=selenium_instance)
    web_driver.get(search_url)
    
    i = 0
    try: 
        while i < 10000:
            listings = web_driver.find_elements(By.CLASS_NAME, "sr_property_block")

            for listing in listings:
                try:
                    title = listing.find_element(By.CLASS_NAME, "sr-hotel__name").text.strip()
                    address = listing.find_element(By.CLASS_NAME, "sr_card_address_line").text.strip()
                    room_type = listing.find_element(By.CLASS_NAME, "room_link").text.strip()
                    price = listing.find_element(By.CLASS_NAME, "bui-price-display__value").text.strip()
                    review_score = listing.find_element(By.CLASS_NAME, "bui-review-score__badge").text.strip()
                    num_reviews = listing.find_element(By.CLASS_NAME, "bui-review-score__text").text.split(" ")[0]

                    hotels.append({"title": title, 
                                    "address": address, 
                                    "room_type": room_type, 
                                    "price": price, 
                                    "review_score": review_score, 
                                    "num_reviews": num_reviews})
                    print(hotels)
                    
                except NoSuchElementException as e:
                    print(f"Click element not found: {e}")

                    try:
                        next_button = web_driver.find_element(By.CLASS_NAME, "pagenext")
                        next_button.click()
                        time.sleep(3)
                        i += 1
                    
                    except NoSuchElementException as e:
                        print(f"No more pages {e}")
                        break
                    except TimeoutException as e:
                        print(f"Timeout!!!! {e}")
                        break
           
    except Exception as e:
        print(f"Err: {e}")
    finally:
        print(i)
        web_driver.quit()

    write_to_csv(hotels, csv_out)


def write_to_csv(listings, csv_out):
    try:
        with open(csv_out, "w", newline="") as csv_file:
            fieldnames = ["title", "address", "room_type", "price", "review_score", "num_reviews"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listings)
    except Exception as e:
        print(f"Err out to CSV: {e}")


if __name__ == "__main__":
    scrape_listings()

