# "utils.py" typically refers to a file containing 
# a collection of small, reusable functions and 
# helper classes that perform common tasks across 
# different parts of the application, essentially 
# acting as a "utility belt" for frequently used 
# operations, thus reducing code duplication and 
# improving code organization. 

import os
import sys
import numpy as np
import pandas as pd
from src.exception import CustomException

import dill

from sklearn.metrics import r2_score


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
def evaluate_models(x_train,y_train,x_test, y_test,models):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            model.fit(x_train, y_train)

            ## making prediction
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score

            return report
    
    except:
        pass