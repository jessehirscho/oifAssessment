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
    listings = []

    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'listings.csv')
        with open(file_path, "r") as csv_file:
            lines = csv.DictReader(csv_file)
            for line in lines:
                if 'price' in line and line['price']:  
                    try:
                        price_str = str(line['price'])  
                        line['price'] = float(price_str.replace('AUD ', '').strip())
                        listings.append(line)
                    except ValueError:
                        continue
    except FileNotFoundError:
        return jsonify({"Err: File not exists"}), 404
   
    cheapest_listings = sorted(listings, key=lambda x: x['price'])[:50]
    
    return jsonify(cheapest_listings)


if __name__ == "__main__":
    app.run(debug=True)
