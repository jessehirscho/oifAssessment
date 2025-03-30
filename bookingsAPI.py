import csv
import os
from flask import Flask, jsonify


app = Flask(__name__)

# Route for the root URL
@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Booking API!"


# MAKE API GET CALL + Load data from csv 
@app.route('/cheapest', methods=['GET'])
def load_data():
    # return "TRUE"
    listings = []

    try:
        print("TEST1")
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'listings.csv')
        with open(file_path, "r") as csv_file:
            print("TEST2")
            lines = csv.DictReader(csv_file)
            for line in lines:
                listings.append(line)
            return listings

    except FileNotFoundError:
        return jsonify({"Err: File not exists"}), 404

    
    for listing in listings:
        print(listing)
        try:
            listing["Cost (AUD)"] = float(listing["Cost (AUD)"].replace(',', ''))
        except ValueError:
            listing["Cost (AUD)"] = float('inf')
    
    cheapest_listings = sorted(listings, key=lambda x: x["Cost (AUD)"])[:50]

    for listing in cheapest_listings:
        if listing["Cost (AUD)"] != float('inf'):
            listing["Cost (AUD)"] = str(listing["Cost (AUD)"])
        else:
            listing["Cost (AUD)"] = "NA"

    return jsonify(cheapest_listings)


if __name__ == "__main__":
    app.run(debug=True)
