import os
import csv
from flask import Flask, render_template, request, url_for, session, redirect
from pymongo import MongoClient

def create_app():
    """
    Create and configure the Flask application
    Returns: app: the Flask application object
    """
    app = Flask(__name__)
    app.secret_key = "secret key"
    # mongo setup
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client.database
    collections = db.collections
    
    #handle the csv files
    csv_file_path = "archive/breed_traits.csv"
    
    with open(csv_file_path, mode="r") as file:
        reader = csv.DictReader(file)
        data = list(reader)
        for entry in data:
            for key in entry:
                try: 
                    entry[key] = int(entry[key])
                except ValueError:
                    pass
    collections.insert_many(data)
    @app.route('/')
    def home():
        """
        Route for the home page
        Returns: rendered template (str): the rendered HTML template
        """
        return render_template("index.html")
    @app.route('/question1', methods=['GET','POST'])
    def question1():
        if request.method=='POST':
            session["affectionate_with_family"] = request.form.get("family")
            session["good_with_young_children"] = request.form.get("children")
            session["good_with_other_dogs"] = request.form.get("dog")
            return redirect(url_for('question2'))
        print("are you here?")
        return render_template('form1.html')
    @app.route('/question2', methods=['GET','POST'])
    def question2():
        if request.method=='POST':
            session["shedding_level"] = request.form.get("shedding")
            session["coat_grooming_frequency"] = request.form.get("coat")
            session["drooling_level"] = request.form.get("drooling")
            return redirect(url_for('question3'))
        return render_template('form2.html')
    @app.route('/question3', methods=['GET','POST'])
    def question3():
        if request.method=='POST':
            session["openness_to_strangers"] = request.form.get("openness")
            session["playfulness_level"] = request.form.get("playfulness")
            session["watchgod/protective_nature"] = request.form.get("nature")
            session["adaptability_level"] = request.form.get("adaptability")
            return redirect(url_for('question4'))
        return render_template('form3.html')
    @app.route('/question4', methods=['GET','POST'])
    def question4():
        if request.method=='POST':
            session["trainability_level"] = request.form.get("trainability")
            session["energy_level"] = request.form.get("energy")
            session["barking_level"] = request.form.get("barking")
            session["mental_stimulation_needs"] = request.form.get("mental")
            return redirect(url_for('result'))
        return render_template('form4.html')
    @app.route('/result')
    def result():
        session["affectionate_with_family"]
        session["good_with_young_children"]
        session["good_with_other_dogs"]
        session["mental_stimulation_needs"]
    
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0",debug=True)