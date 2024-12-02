# "utils.py" typically refers to a file containing a collection of small, reusable functions and 
# helper classes that perform common tasks across different parts of the application, essentially acting as a "utility belt" for frequently used 
# operations, thus reducing code duplication and improving code organization. 

import os
import sys
import numpy as np
import pandas as pd
from src.exception import CustomException

import dill

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


## save_object fuction that is been used in 
## data_transformation.py to save the objects 
def save_objects(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    

## this function is used in model_training.py
## for evalution of the training data
def evaluate_models(x_train,y_train,x_test, y_test,models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]
            
            ## Grid Search CV
            gs = GridSearchCV(estimator=model, param_grid=para, cv=5)

            ## fixing with grid search CV
            gs.fit(x_train, y_train)
            
            ## setting the best params from hyper-parameter tunning to mode
            model.set_params(**gs.best_params_)

            ## training the model
            model.fit(x_train, y_train)

            ## making prediction
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score

            return report

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    
    except Exception as e:
        raise CustomException(e, sys)
