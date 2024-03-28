

from sklearn.linear_model import SGDClassifier,LogisticRegression
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_predict, cross_val_score,KFold, RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier, AdaBoostClassifier
from sklearn.metrics import accuracy_score
import pickle
import os 
import pandas as pd

class Model_Training:
    def __init__(self):
        self.best_models = []
        self.best_params = []
        self.scoring = 'accuracy'
        self.best_model = None 

    def training(self):
        try:
            artifacts_path = os.path.join(os.getcwd(), 'artifacts')

            # Read CSV files into DataFrame variables
            x_train = pd.read_csv(os.path.join(artifacts_path, 'X_train.csv'))
            x_test = pd.read_csv(os.path.join(artifacts_path, 'X_test.csv'))
            y_train = pd.read_csv(os.path.join(artifacts_path, 'y_train.csv'))
            y_test = pd.read_csv(os.path.join(artifacts_path, 'y_test.csv'))
            y_train = y_train.values.ravel()
            models = [
                ('RF', RandomForestClassifier(), {'n_estimators': [10, 50, 100, 200]}),
                #('SVC', SVC(), {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']}),
                ('xgboost', XGBClassifier(), {'n_estimators': [50, 100, 150], 'learning_rate': [0.01, 0.1, 0.2]}),
                #('lightgbm', LGBMClassifier(), {'n_estimators': [50, 100, 150], 'learning_rate': [0.01, 0.1, 0.2]}),
               
            ]

            for name, model, param_grid in models:
                grid_search = GridSearchCV(model, param_grid, cv=5, scoring=self.scoring)
                grid_search.fit(x_train, y_train)
                best_model = grid_search.best_estimator_
                best_param = grid_search.best_params_
                self.best_models.append((name, best_model))
                self.best_params.append((name, best_param))

            for name, model in self.best_models:
                y_pred_proba = model.predict_proba(x_test)[:, 1]
                accuracy = accuracy_score(y_test, y_pred_proba.round())
                if self.best_model is None or accuracy > self.best_model[1]:
                    self.best_model = (model, accuracy)

            best_model_path = os.path.join(artifacts_path, 'best_model.pkl')
            with open(best_model_path, 'wb') as f:
                pickle.dump(self.best_model, f)

        except Exception as e:
            raise



if __name__ == "__main__":
     obj = Model_Training()
     obj.training()
    