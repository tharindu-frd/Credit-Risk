import json
import argparse
import os 
import pandas as pd 

class CsvValidator:
    def __init__(self):
        pass

    def load_schema(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_file = os.path.join(current_dir, 'schema_training.json')

            with open(schema_file, 'r') as file:
                self.schema = json.load(file)
                print("Schema loaded successfully.")
        except FileNotFoundError:
            print(f"Error: Schema file '{schema_file}' not found.")
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in schema file '{schema_file}': {e}")
        except Exception as e:
            print(f"Error loading schema from '{schema_file}': {e}")

    def validate_csv(self):
        try:
            self.load_schema() 
            artifacts_path = os.path.join(os.getcwd(), 'artifacts')
            validateddata_folder = os.path.join(artifacts_path, 'validateddata')

            # Print out the path where the validateddata folder will be created
            print("Creating 'validateddata' folder at:", validateddata_folder)

            # Check if the validateddata folder exists, if not, create it
            if not os.path.exists(validateddata_folder):
                os.makedirs(validateddata_folder)
                print("Successfully created 'validateddata' folder!")
            else:
                print("The 'validateddata' folder already exists.")

            csv_file = os.path.join(artifacts_path, 'data.csv')
            df = pd.read_csv(csv_file)
            df.columns = ['id', 'status', 'duration', 'credit_history', 'purpose', 'amount', 'savings', 'employment_duration', 'installment_rate', 'personal_status_sex', 'other_debtors', 'present_residence', 'property', 'age', 'other_installment_plans', 'housing', 'number_credits', 'job', 'people_liable', 'telephone', 'foreign_worker', 'credit_risk']
            df.columns = map(str.lower, df.columns)
            
            # Check the number of columns
            if len(df.columns) != self.schema['NumberofColumns']:
                print(f"Error: Number of columns in {csv_file} doesn't match the schema.")
                return False

            # Check column names and data types
            for col_name, col_dtype in self.schema['ColName'].items():
                if col_name not in df.columns:
                    print(f"Error: Column '{col_name}' is missing in {csv_file}.")
                    return False
                if df[col_name].dtype.name != col_dtype:
                    print(f"Error: Data type of column '{col_name}' in {csv_file} is incorrect.")
                    return False
                
            # Save validated CSV file in the 'validateddata' subfolder
            validated_csv_file = os.path.join(validateddata_folder, 'validated_data.csv')
            df.to_csv(validated_csv_file, index=False)
            print(f"Validated CSV file saved to: {validated_csv_file}")

            return True
        except Exception as e:
            print("An error occurred:", e)
            return False

if __name__ == "__main__":
    obj = CsvValidator()
    obj.load_schema()
    obj.validate_csv()

   

    
                      

