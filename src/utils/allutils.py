import yaml
from datetime import datetime



###############  Lets define a function to  read yaml files ########################
def read_yaml(path_to_yaml:str)-> dict:
       '''
              This function takes a string as an input and returns a dictionary

       '''
       with open(path_to_yaml) as yaml_file:
              content = yaml.safe_load(yaml_file)
       # print(content)
       return content






