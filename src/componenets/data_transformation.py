import os
import sys
from src.exception import CustomException
from src.logger import logging

import pandas as pd
from sklearn.preprocessing import StandardScaler,  OneHotEncoder
from sklearn.compose import ColumnTransformer

## The imputer is an estimator used to fill the missing values in datasets
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
import numpy as np 

from src.utils import save_objects

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifact', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
    
        '''
        This function is responsible for data transformation based on various types of columns in the dataset
        '''
        logging.info('Data Transformation Initiated')
        try:
            numerical_features = [
                'writing score',
                'reading score'
            ]
            categorical_features = [
                'gender',
                'race/ethnicity',
                'parental level of education',
                'lunch',
                'test preparation course'
            ]

            num_pipline = Pipeline(
                steps=[
                    ('Imputer', SimpleImputer(strategy='mean')),
                    ('Scaler', StandardScaler())
                ]
            )
            cat_pipline = Pipeline(
                steps=[
                    ('Imputer', SimpleImputer(strategy='most_frequent')),
                    ('One_Hot_Encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),  # Fix applied
                    ('Standard_Scaler', StandardScaler())
                ]
            )
            logging.info(f'Numerical Features {numerical_features}')
            logging.info(f'Categorical Features {categorical_features}')

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipline, numerical_features),
                    ('cat_pipeline', cat_pipline, categorical_features)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info('The train and test data has been successfully read')
            logging.info('Obtaining Preprocessing object')

            preprocessor_obj = self.get_data_transformer_object()

            target_column_name = 'math score'
            numerical_columns =  ['writing score',
                'reading score']
            categorical_columns = ['gender',
                'race/ethnicity',
                'parental level of education',
                'lunch',
                'test preparation course']

            input_feature_train_df = train_df.drop(columns=target_column_name, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=target_column_name, axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f'Applying preprocessing object on training dataframe and testing dataframe'
                )

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)

            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            ## "np.c_" is a function used to concatenate arrays column-wise, essentially stacking multiple arrays vertically to create a new array where each input array becomes a column in the resulting array; it's a convenient way to combine arrays along their second axis (columns) using slice notation.
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]
            logging.info('Saving preprocessed object')
            
            save_objects(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            
        except Exception as e:
            raise CustomException(e, sys)

    