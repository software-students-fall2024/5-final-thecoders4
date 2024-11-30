import os
import csv
from flask import Flask, render_template, url_for
from pymongo import MongoClient

def create_app():
    """
    Create and configure the Flask application
    Returns: app: the Flask application object
    """
    app = Flask(__name__)
    # mongo setup
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client.database
    collections = db.collections
    
    #handle the csv files
    csv_file_path = "archive/breed_traits.csv"
    with open(csv_file_path, mode="r") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        for entry in data:
            for key in entry:
                try: 
                    entry[key] = int(entry[key])
                except ValueError:
                    pass
    collections.insert_many(data)
    
    @app.route('/home')
    def home():
        """
        Route for the home page
        Returns: rendered template (str): the rendered HTML template
        """
        return render_template("index.html")