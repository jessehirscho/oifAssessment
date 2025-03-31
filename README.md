# oifAssessment

Although the task is not directly relevant to our work, the skills tested will be. Feel free to use any additional packages you find online. You must take care to ensure your code is generalisable, robust, explainable, and maintainable. No formal testing is required, and the code does not have to be deployed anywhere. When completed to the best of your ability, please share a GitHub URL to your repository, and send a zip file of your scraped data if possible.


## Part 1
Booking.com contains a large quantity of listings for Australia, we want to scrape these for the 1st-2nd February 2026 (Search). Use Selenium (Python) to scrape all listings:
- Title
- Address
- Headline Room Type
- Cost (AUD)
- Review Score

## of Reviews
Scrape as many listings as you can, however your code should be designed to handle an arbitrary number of listings. Care should be taken to mimic human-like behaviour.
Structure your output in a CSV.
 

## Part 2
Create a simple Flask (Python) server in the same repository as Part 1.
Create an API endpoint that when called:
Reads your CSV file
Identifies the 50 cheapest listings
Returns it in JSON format to the end user