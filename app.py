
import os
import csv
from flask import Flask, render_template, request, url_for, session, redirect
from pymongo import MongoClient

def create_app(skip_initialization = False):
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
    if not skip_initialization:
        collections.drop()
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
    if not skip_initialization:
        collections.insert_many(data)
    
    csv_file_path = "archive/breed_rank.csv"
    with open(csv_file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            breed = row["Breed"]
            link = row["links"]
            image = row["Image"]
            if not skip_initialization:
                collections.update_one(
                    {"Breed": breed},           # Match condition
                    {"$set": {"links": link, "Image": image}}  # Add or update fields
                )
    
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
        query = {}
        if session["affectionate_with_family"] == "independent":
            query["Affectionate With Family"] = {"$lte": 2}
        elif session["affectionate_with_family"] == "lovey-dovey":
            query["Affectionate With Family"] = {"$gte": 4}
        if session["good_with_young_children"] == "not_recommended":
            query["Good With Young Children"] = {"$lte": 2}
        elif session["good_with_young_children"] == "good":
            query["Good With Young Children"] = {"$gte": 4}
        if session["good_with_other_dogs"] == "not_recommended":
            query["Good With Other Dogs"] = {"$lte": 2}
        elif session["good_with_other_dogs"] == "good":
            query["Good With Other Dogs"] = {"$gte": 4}
        if session["shedding_level"] == "no_shedding":
            query["Shedding Level"] = {"$lte": 2}
        elif session["shedding_level"] == "everywhere":
            query["Shedding Level"] = {"$gte": 4}
        if session["coat_grooming_frequency"] == "monthly":
            query["Coat Grooming Frequency"] = {"$lte": 2}
        elif session["coat_grooming_frequency"] == "daily":
            query["Coat Grooming Frequency"] = {"$gte": 4}
        if session["drooling_level"] == "less":
            query["Drooling Level"] = {"$lte": 2}
        elif session["drooling_level"] == "always":
            query["Drooling Level"] = {"$gte": 4}
        if session["openness_to_strangers"] == "reserved":
            query["Openness To Strangers"] = {"$lte": 2}
        elif session["openness_to_strangers"] == "everyone":
            query["Openness To Strangers"] = {"$gte": 4}
        if session["playfulness_level"] == "only":
            query["Playfulness Level"] = {"$lte": 2}
        elif session["playfulness_level"] == "non_stop":
            query["Playfulness Level"] = {"$gte": 4}
        if session["watchgod/protective_nature"] == "mine":
            query["Watchdog/Protective Nature"] = {"$lte": 2}
        elif session["watchgod/protective_nature"] == "vigilant":
            query["Watchdog/Protective Nature"] = {"$gte": 4}
        if session["adaptability_level"] == "routine":
            query["Adaptability Level"] = {"$lte": 2}
        elif session["adaptability_level"] == "adaptable":
            query["Adaptability Level"] = {"$gte": 4}
        if session["trainability_level"] == "self-willed":
            query["Trainability Level"] = {"$lte": 2}
        elif session["trainability_level"] == "eager":
            query["Trainability Level"] = {"$gte": 4}
        if session["energy_level"] == "couch_potato":
            query["Energy Level"] = {"$lte": 2}
        elif session["energy_level"] == "high":
            query["Energy Level"] = {"$gte": 4}
        if session["barking_level"] == "alert":
            query["Barking Level"] = {"$lte": 2}
        elif session["barking_level"] == "vocal":
            query["Barking Level"] = {"$gte": 4}
        if session["mental_stimulation_needs"] == "lounge":
            query["Mental Stimulation Needs"] = {"$lte": 2}
        elif session["mental_stimulation_needs"] == "job":
            query["Mental Stimulation Needs"] = {"$gte": 4}
        docs = collections.find(query)
        docs_list = list(docs)
        return render_template('result.html',docs=docs_list,count=len(docs_list))
    @app.route('/info/<dog_breed>')
    def info(dog_breed):
        doc = collections.find_one({"Breed":dog_breed})
        return render_template('info.html',doc=doc)
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0",debug=True)