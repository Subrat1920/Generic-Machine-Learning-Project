from flask import Flask, request, url_for, render_template
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.pipeline.predict_pipeline import CustomData, PredictPipline


application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # Collect data from the form
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethinicty=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            writing_score=int(request.form.get('writing_score')),
            reading_score=int(request.form.get('reading_score'))
        )
        
        # Prepare data for prediction
        pred_df = data.get_data_as_data_frame()

        # Run the prediction pipeline
        predict_pipeline = PredictPipline()
        results = predict_pipeline.predict(pred_df)
        
        return render_template('home.html', results=results[0])


if __name__=='__main__':
    application.run(debug=True)