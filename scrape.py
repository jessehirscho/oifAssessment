import time
import pandas 
from selenium import webdriver



## GET BOOKING.COM REQUEST
search_url = "https://www.booking.com"
driver.get(search_url)
time.sleep(3)  # Allow the page to load


# SCRAPE LISTINGS
hotelsLs = []

# Loop through hotels
print("Checkpoint #1")

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



# CSV functionality
data = pandas.DataFrame(hotelsLs, columns=["Title" , "Address", "Headline Room Type", "Cost (AUD)", "Review Score", "# of Reviews"])
filename = 'test.csv'
print("Checkpoint #3")
data.convertToCSV(filename, index=False)
print("Data officialy scraped!")