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