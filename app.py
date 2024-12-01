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
    pipeline = [
        {"$group": {
            "_id": "$Breed", 
            "count": {"$sum": 1},  # Count occurrences of each breed
            "ids": {"$push": "$_id"}  # Collect document IDs for each breed
        }},
        {"$match": {"count": {"$gt": 1}}}  # Only include breeds with duplicates
    ]

    duplicates = list(collections.aggregate(pipeline))
    for duplicate in duplicates:
        ids_to_delete = duplicate["ids"][1:]  # Keep the first document, delete the rest
        collections.delete_many({"_id": {"$in": ids_to_delete}})
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
        docs = collections.find(query,{"_id": 0, "Breed":1})
        #docs = collections.find({"Breed":"Retrievers (Labrador)"},{"Breed": 1,"Affectionate With Family":1,"Good With Young Children":1,"Good With Other Dogs":1})
        docs_list = list(docs)
        return render_template('result.html',docs=docs_list,count=len(docs_list))
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0",debug=True)