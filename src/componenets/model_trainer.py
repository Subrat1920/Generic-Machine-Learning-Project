import os
import sys
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging
from src.utils import save_objects, evaluate_models
from dataclasses import dataclass

from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet 
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifact','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array, preprocessor_path):
        ## if found any error in future just paste ( preprocessor_path) in the function parameters, if not present
        try:
            logging.info('Splitting training and test data')
            x_train, y_train, x_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            models = {
                'Linear Regression' : LinearRegression(),
                # 'Ridge Regression' : Ridge(),
                # 'Lasso Regression' : Lasso(),
                # 'Elastic Net Regression' : ElasticNet(),
                'K Nearest Neighbors' : KNeighborsRegressor(),
                # 'Support Vector Regressor' : SVR(),
                'Decision Tree Regressor': DecisionTreeRegressor(),
                'Random Forest Regressor' : RandomForestRegressor(),
                'Gradient Boost Regressor' : GradientBoostingRegressor(),
                'Cat Boost Regressor' : CatBoostRegressor(verbose=False),
                'XGBoost Regressor' : XGBRegressor()

            }

            params = {
                'Linear Regression': {
                    # 'fit_intercept': [True, False],
                    # 'normalize': [True, False],
                    # 'copy_X': [True, False]
                },
                'Ridge Regression': {
                    'alpha': [0.1, 1.0, 10.0],
                    'solver': ['lsqr', 'sparse_cg', 'sag', 'saga'] ## also we can add ['auto', 'svd', 'cholesky']
                },
                'Lasso Regression': {
                    'alpha': [0.1, 1.0, 10.0],
                    'max_iter': [1000, 5000, 10000],
                    'selection': ['cyclic', 'random']
                },
                'Elastic Net Regression': {
                    'alpha': [0.1, 1.0, 10.0],
                    'l1_ratio': [0.1, 0.5, 0.9],
                    'max_iter': [1000, 5000, 10000]
                },
                'K Nearest Neighbors': {
                    'n_neighbors': [3, 5, 7, 10],
                    'weights': ['uniform', 'distance'],
                    'algorithm': ['ball_tree', 'kd_tree']
                },
                'Support Vector Regressor': {
                    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                    'C': [0.1, 1.0, 10.0],
                    'epsilon': [0.1, 0.2, 0.5]
                },
                'Decision Tree Regressor': {
                    'criterion': ['squared_error', 'friedman_mse', 'poisson'],
                    'splitter': ['best', 'random'],
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10]
                },
                'Random Forest Regressor': {
                    'n_estimators': [100, 200, 300],
                    'criterion': ['squared_error', 'absolute_error', 'poisson'],
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10]
                },
                'Gradient Boost Regressor': {
                    'loss': ['squared_error', 'absolute_error'],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'n_estimators': [100, 200, 300],
                    'subsample': [0.5, 0.7, 1.0]
                },
                'Cat Boost Regressor': {
                    'iterations': [100, 500, 1000],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'depth': [4, 6, 10]
                },
                'XGBoost Regressor': {
                    'n_estimators': [100, 200, 300],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 6, 9],
                    'subsample': [0.5, 0.7, 1.0]
                }
}


            ## below code is getting changed for some error if not required, undo it 
            ## changing x=x_train, y=y_train to x_train=x_train, y_train=y_train
            model_report : dict = evaluate_models(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models = models, param=params)
            
            ## to get the best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## to get the best model name from the dictionary
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]

            if best_model_score<0.6: ## threshold value
                raise CustomException('No best model found')
            logging.info('Best found model on both training and test data')

            save_objects(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(x_test)
            r2 = r2_score(y_test, predicted)

            logging.info('Best model is pickled')
            return r2


        except Exception as e:
            raise CustomException(e, sys)
