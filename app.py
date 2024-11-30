from flask import Flask, render_template, url_for
from pymongo import MongoClient
import os

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
    