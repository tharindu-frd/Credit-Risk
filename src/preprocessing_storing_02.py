#######  Get all the csv files from  artifacts->ValidatedTrainingData  and store them
### inside the database  



import os 
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import ADASYN
from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np



      

class StoringData:
    def __init__(self):
        pass

    def preprocessing_and_storing(self):
        try:
            artifacts_path = os.path.join(os.getcwd(), 'artifacts')
            validateddata_folder = os.path.join(artifacts_path, 'validateddata')
            validated_csv_file = os.path.join(validateddata_folder, 'validated_data.csv')

            # Read the validated CSV file into a DataFrame
            data = pd.read_csv(validated_csv_file)

            data= data.drop_duplicates()


       
            ## apply_transformations(self,data):
            columns = ['amount','age','duration']
            data['amount'] = round(np.log(data['amount']),2)
            data['age'] = round(np.log(data['age']),2)
            data['duration'] = round(np.log(data['duration']),2)
            data.drop(columns,axis=1,inplace=True)
            

            ## seperate_label_feature(self,data):
            # "credit_risk"
            X = data.drop('credit_risk',axis=1)
            y = data['credit_risk']
           
            ## splitting_data:
            x_train, x_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
          
            


            #########   handling_missing_values:
            # Get numerical and categorical features
            numerical_features = x_train.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_features = x_train.select_dtypes(include=['object']).columns

            # Impute numerical features using KNN
            numerical_imputer = KNNImputer(n_neighbors=5)
            x_train[numerical_features] = numerical_imputer.fit_transform(x_train[numerical_features])
            x_test[numerical_features] = numerical_imputer.transform(x_test[numerical_features])

            # Check if there are any categorical features
            if len(categorical_features) >= 1:
                     # Impute categorical features using Random Forest
                     categorical_imputer = RandomForestClassifier(n_estimators=100, random_state=42)

                     # Fit the imputer on the observed categorical data
                     categorical_imputer.fit(x_train[categorical_features], y_train)

                     # Predict missing values in both training and test sets
                     x_train[categorical_features] = categorical_imputer.predict(x_train[categorical_features])
                     x_test[categorical_features] = categorical_imputer.predict(x_test[categorical_features])

            
            # Handling class imbalances using ADASYN
            class_counts = np.bincount(y_train)
            threshold = 30  # 30%
            total_instances = len(y_train)
            for class_label, count in enumerate(class_counts):
                class_percentage = (count / total_instances) * 100
                if class_percentage < threshold:
                    ada = ADASYN(sampling_strategy='minority', random_state=42, n_neighbors=7)
                    x_res, y_res = ada.fit_resample(x_train, y_train)
                    x_train = pd.DataFrame(x_res, columns=x_train.columns)
                    y_train = pd.Series(y_res)

            # Save x_train, x_test, y_train, y_test as CSV files
            x_train.to_csv(os.path.join(artifacts_path, 'X_train.csv'), index=False)
            x_test.to_csv(os.path.join(artifacts_path, 'X_test.csv'), index=False)
            y_train.to_csv(os.path.join(artifacts_path, 'y_train.csv'), index=False)
            y_test.to_csv(os.path.join(artifacts_path, 'y_test.csv'), index=False)

        except Exception as e:
            raise
       






if __name__ == "__main__":
     dt = StoringData()
     dt.preprocessing_and_storing()
    