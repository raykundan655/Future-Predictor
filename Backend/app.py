from flask import Flask,request,jsonify
from flask_cors import CORS
import pickle
import pandas  as pd
import numpy as np
from Preparation.Budgetrecommendations import recommend_savings
from Preparation.MoveRecommendation import recommend_movie
import os

# os lets you find, create, delete, or check files and folders.

Base_DIR=os.path.dirname(__file__) #yeah address store kara ga app.py file kaha hai 
# __file__ → is a special variable It stores the full path of the current Python file that’s being executed


with open(os.path.join(Base_DIR,"StudentPerformance.pkl"),"rb") as fb:
    studentModel=pickle.load(fb)

# BASE_DIR = "C:/Users/USER/OneDrive/Desktop/Python/FuturePredicator/Backend"
# os.path.join(BASE_DIR, "StudentPerformance.pkl") = "C:/Users/USER/OneDrive/Desktop/Python/FuturePredicator/Backend/StudentPerformance.pkl"
# Python now knows exactly where the file is, no matter from which folder you run the script.

with open(os.path.join(Base_DIR,"placementAnalysis.pkl"),"rb") as fb:
    placementModel=pickle.load(fb)

with open(os.path.join(Base_DIR,"BudgetScale.pkl"),"rb") as fb:
    BudgetScale=pickle.load(fb)

with open(os.path.join(Base_DIR,"BudgetClusterModel.pkl"),"rb") as fb:
    BudgetClusterModel=pickle.load(fb)

centroids=BudgetScale.inverse_transform(BudgetClusterModel.cluster_centers_)
cluster_profiles=pd.DataFrame(centroids,columns=["Eating_Out", "Entertainment", "Miscellaneous", "Groceries", "Transport",'Desired_Savings',      
       'Disposable_Income'])



app=Flask(__name__)

CORS(app)

@app.route("/")
def home():
    return "welcome to Future Predictor"

@app.route("/placementPrediction",methods=["POST"])
def placement():
    try:
        data=request.get_json()

        req_feild=['CGPA', 'Internships', 'Projects', 'Workshops/Certifications',
        'AptitudeTestScore', 'SoftSkillsRating', 'ExtracurricularActivities',
        'PlacementTraining', 'SSC_Marks', 'HSC_Marks']
    
        missing=[f for f in req_feild if f not in data]

        if missing:
            return jsonify({"error":f'Missing feild: {missing}'})
    
        df=pd.DataFrame([data])

        # ensure the order
        feature=df[['CGPA', 'Internships', 'Projects', 'Workshops/Certifications',
        'AptitudeTestScore', 'SoftSkillsRating', 'ExtracurricularActivities',
        'PlacementTraining', 'SSC_Marks', 'HSC_Marks']]

        pred=placementModel.predict(feature)
    # it will first scale the numeric data then do encoding of cat data then after complition of preprocessing  model will predict

        res=pred[0]

        return jsonify({"prediction":res})
    
    except Exception as e:
        return jsonify({"error": str(e)}),400
    


@app.route("/Studentperformance",methods=["POST"])
def studentperformance():
    try:

        data=request.get_json()

        req_col=['Hours Studied', 'Previous Scores', 'Extracurricular Activities',
       'Sleep Hours', 'Sample Question Papers Practiced']
        
        missing=[f for f in req_col if f not in data]

        if missing:
            return jsonify({"error":f'Missing feild: {missing}'})
        
        # making json data into dataframe
        df=pd.DataFrame([data])

        # reorder
        feature=df[['Hours Studied', 'Previous Scores', 'Extracurricular Activities',
       'Sleep Hours', 'Sample Question Papers Practiced']]
        
        pred=studentModel.predict(feature)

        return jsonify({"prediction":pred[0]})


    except Exception as e:
       return jsonify({"error": str(e)}),400 
    

# the golden line 🌟:
# GET → Use when you just retrieve existing data from the server.
# POST → Use when you send new data to the server for processing or storage.

@app.route("/BudgetAnalysis",methods=["POST"])
def BudgetAnalysis():
    try:
        data=request.get_json()
        # request is not something you created — Flask creates a Request object for every incoming HTTP request and makes it available to you.
        # request is an object that represents the HTTP request sent by the client
        # lets your backend code access what the client sent.

        req_col=["Eating_Out", "Entertainment", "Miscellaneous",
                         "Groceries", "Transport", "Desired_Savings", "Disposable_Income"]
        
        missing=[col for col in req_col if col not in data]

        if missing:
            return jsonify({"error":f"missing field:{missing}"})
        
        df=pd.DataFrame([data])
        
        df = df.apply(pd.to_numeric, errors="coerce")

        # Ensure correct column order
        df = df[req_col]

        rec=recommend_savings(df,BudgetScale,BudgetClusterModel,cluster_profiles)

        return jsonify({"recommendation":rec})

    except Exception as e:
       return jsonify({"error": str(e)}),400  


@app.route("/moveRecommendation",methods=["GET"])
def moveRecommendation():
    try:
        title=request.args.get("title")
        
        if not title:
            return jsonify({"error": "Please provide a movie title"}), 400
        
        rec=recommend_movie(title)

        return jsonify({"input_movie": title, "recommendations": rec})


    except Exception as e:
       return jsonify({"error": str(e)}),400


if __name__=="__main__":
    app.run(debug=True)





# When a user searches for a movie or clicks on a movie to check recommendations,
# the frontend is only retrieving already processed information from your backend.
# No new data is being created or stored.
# No preprocessing step is being triggered from the user’s side.
# The backend is just fetching results (recommendations) and returning them.
# 👉 That’s exactly why GET method is the right choice for your movie recommendation endpoint



# Concept	Definition	                               Example Use
# Script	Python file executed directly python       game.py
# Module	Python file imported into another file	   import game


