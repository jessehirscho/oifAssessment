import time
import csv
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Extracts listing attributes
def extract_listing_data(listing):
    listing_data = {}

    try:
        listing_data["title"] = listing.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text.strip()
    except Exception:
        listing_data["title"] = "Title not found"

    try:
        listing_data["address"] = listing.find_element(By.CSS_SELECTOR, "span[data-testid='address']").text.strip()
    except Exception:
        listing_data["address"] = "Address not found"

    try:
        room_type_element = listing.find_element(By.CSS_SELECTOR, "div[data-testid='recommended-units']")
        lines = room_type_element.text.strip().split("\n")  # Split text into lines

        if len(lines) > 1:  # Ensure at least two lines exist
            room_type = lines[1]  # Get the second line
        else:
            room_type = "Room type not found"

    except Exception:
        room_type = "Room type not found"
    listing_data["room_type"] = room_type  # Store result

    try:
        review_text = listing.find_element(By.CSS_SELECTOR, "div[data-testid='review-score']").text.strip()

        try:
            review_score_match = re.search(r'\d+\.\d+', review_text)
            if review_score_match:
                listing_data["review_score"] = review_score_match.group()
            else:
                listing_data["review_score"] = "Review score not found"
        except Exception:
            listing_data["review_xscore"] = "Review score not found"

        try:
            num_reviews_match = re.search(r'(\d+(?:,\d+)*) real reviews?', review_text)
            if num_reviews_match:
                listing_data["num_reviews"] = num_reviews_match.group(1).replace(",", "")
            else:
                listing_data["num_reviews"] = "Number of reviews not found"
        except Exception:
            listing_data["num_reviews"] = "Number of reviews not found"

    except Exception:
        listing_data["review_score"] = "Review score not found"
        listing_data["num_reviews"] = "Number of reviews not found"

    try:
        listing_data["price"] = listing.find_element(By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']").text.strip()
    except Exception:
        listing_data["price"] = "Price not found"

    return listing_data


# SCRAPE LISTINGS
def scrape_listings(csv_out="listings.csv"):
    hotels = []
    
    ## GET BOOKING.COM REQUEST
    search_url = "https://www.booking.com/searchresults.en-gb.html?ss=Australia&checkin_year=2026&checkin_month=02&checkin_monthday=01&checkout_year=2026&checkout_month=02&checkout_monthday=02&group_adults=1&no_rooms=1&group_children=0&sb_lp=1"
    
    print("Checkpoint #1: Scrape begins\n")

    # Create tmp instance of chrome for selenium
    selenium_instance  = webdriver.ChromeOptions()
    selenium_instance.add_argument("--headless")
    selenium_instance.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    print("instance opened\n")

    web_driver = webdriver.Chrome(options=selenium_instance)
    web_driver.get(search_url)
    print("driver created\n")

    try: 
        try:
            properties_heading = WebDriverWait(web_driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[aria-label*="properties found"]'))
            )
            properties_text = properties_heading.text
            properties_count = int(re.search(r'\d+', properties_text).group())  # num properties
            print(f"Total properties found: {properties_count}")

        except (NoSuchElementException, TimeoutException):
            print("Could not find properties count heading.")
            properties_count = 10000  

        properties_scraped = 1

        while properties_scraped < properties_count:
            try:
                # Wait for listings to load
                # NOTE TO SELF: make sure careful and mimic human activity/traffic!!!
                listings = WebDriverWait(web_driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='property-card']"))
                )
                print(f"Number of listings: {len(listings)}\n")
                
            except (TimeoutException, WebDriverException) as e:
                print(f"Error loading listings: {e}")
                time.sleep(5) 
                continue

            for listing in listings:
                try:
                    
                    listing_data = extract_listing_data(listing)
                    hotels.append(listing_data)
                    hotel_link = listing.find_element(By.CSS_SELECTOR, "a[data-testid='title-link']").get_attribute('href')

                    web_driver.execute_script(f"window.open('{hotel_link}', '_blank');") # open new tab
                    web_driver.switch_to.window(web_driver.window_handles[1]) # switch to new tab                 
                    web_driver.close()
                    web_driver.switch_to.window(web_driver.window_handles[0])
                    
                    properties_scraped += 1
                    print(properties_scraped)

                except NoSuchElementException as e:
                    print(f"Click element not found: {e}")

                    try:
                        next_button = web_driver.find_element(By.CLASS_NAME, "pagenext")
                        next_button.click()
                        time.sleep(3)
                    except NoSuchElementException as e:
                        print(f"No more pages {e}")
                        break
                    except TimeoutException as e:
                        print(f"Timeout!!!! {e}")
                        break
           
    except Exception as e:
        print(f"Err: {e}")
    finally:
        web_driver.quit()

    print(hotels, "\n")
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

