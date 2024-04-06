import os
import joblib
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

class Model_Training:
    def __init__(self):
        self.best_model = None
        self.best_model_accuracy = 0.0
        self.scoring = 'accuracy'

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
                ('xgboost', XGBClassifier(), {'n_estimators': [50, 100, 150], 'learning_rate': [0.01, 0.1, 0.2]}),
            ]

            for name, model, param_grid in models:
                grid_search = GridSearchCV(model, param_grid, cv=5, scoring=self.scoring)
                grid_search.fit(x_train, y_train)
                best_model = grid_search.best_estimator_

                y_pred_proba = best_model.predict_proba(x_test)[:, 1]
                accuracy = accuracy_score(y_test, y_pred_proba.round())

                print(f"{name} - Best Parameters: {grid_search.best_params_}, Best Accuracy: {accuracy}")

                if accuracy > self.best_model_accuracy:
                    self.best_model = best_model
                    self.best_model_accuracy = accuracy

            best_model_path = os.path.join(artifacts_path, 'best_model.joblib')
            joblib.dump(self.best_model, best_model_path)

        except Exception as e:
            raise e

# Example usage:
if __name__ == "__main__":
    model_trainer = Model_Training()
    model_trainer.training()