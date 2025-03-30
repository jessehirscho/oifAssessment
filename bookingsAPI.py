import csv
from flask import Flask, jsonify


testStr = "String"
filename = 'test.csv'

app = Flask(__name__)

# Route for the root URL
@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Booking API!"


# MAKE API GET CALL + Load data from csv 
@app.route('/cheapest-listings', methods=['GET'])
def load_data():
    listings = []

    try:
         with open("listings.csv", "r") as csv_file:
            lines = csv.dictReader(csv_file)
            for line in lines:
                listings.append(line)
    except FileNotFoundError:
        return jsonify({"Err: File not exists"}), 404
    
    for listing in listings:
        print(listing)
        try:
            listing["Cost (AUD)"] = float(listing["Cost (AUD)"].replace(',', ''))
        except ValueError:
            listing["Cost (AUD)"] = float('inf')
        
        for listing in cheapest_listings:
            if listing["Cost (AUD)"] != float('inf'):
                listing["Cost (AUD)"] = str(listing["Cost (AUD)"])
            else:
                listing["Cost (AUD)"] = "NA"
        cheapest_listings = sorted(listings, key=lambda x: x["Cost (AUD)"])[:50]


    return jsonify(cheapest_listings)


if __name__ == "__main__":
    app.run(debug=True)
