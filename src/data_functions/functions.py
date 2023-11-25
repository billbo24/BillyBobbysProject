#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 19:53:34 2023

@author: williamfloyd
A collection of functions that will interface with the data.  

"""


import json
import pandas as pd

def prepare_pandas_for_mongo(input_pandas): 
    #We can alter the orient argument if we like, but generally this is 
    #how I like to think about pandas data, not by columns
    a = input_pandas.to_json(orient='records')
    b = json.loads(a) 
    
    #b is not ready to be pushed into the database, it's already in 
    #a python array
    return b
    



# Example usage:
NEW_DATA ={
  "name": "John",
  "age": 30,
  "address": {
    "city": "New York",
    "zip_code": "10001"
  },
  "contacts": [
    {
      "type": "email",
      "value": "john@example.com"
    },
    {
      "type": "phone",
      "value": "+1 123-456-7890"
    }
  ],
  "friends": [
    {
      "name": "Alice",
      "age": 28,
      "hobbies": ["reading", "painting"],
      "address": {
        "city": "San Francisco",
        "zip_code": "94105"
      }
    },
    {
      "name": "Bob",
      "age": 32,
      "hobbies": ["sports", "music"],
      "address": {
        "city": "Los Angeles",
        "zip_code": "90001"
      }
    }
  ]
}



#Alright found this online.  It completely flattens a JSON object.  Not exactly what I want, but it's a valid option
#I'd like to modify this to split dictionaries across columns and arrays across rows.  Note this works with dictionaries.
#Leaving the bit that flattens arrays commented out so I can make my own method that splits them into rows
def flatten_json(nested_json, exclude=['']):
    """Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
            exclude: Keys to exclude from output.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude: flatten(x[a], name + a + '_')
        
        #Commenting this out for now.  Want to leave the arrays unsplit
        #elif type(x) is list:
            #i = 0
            #for a in x:
                #flatten(a, name + str(i) + '_')
                #i += 1 
        else:
            out[name[:-1]] = x

    flatten(nested_json) #Recursive call
    return out


#Now this will take a single "row" of data and split it into multiple.  Note that in this instance a row will be a dictionary
def split_rows(nested_json):
    #Okay I think I've got it.  This is a pretty bad "split rows" method
    for row_num in range(len(nested_json)): #This will allow us to iterate through each "row"
        row = nested_json[row_num]
        for x in row.keys(): 

            if type(row[x]) is list:
                #If we have a list, say  num = [1,2,3], then we take 3 copies of the rest of the data, and give num = 1,2,3
                
                items = row[x]
                shell = copy.deepcopy(row)
                del shell[x] #remove the array
                
                ans = [] 
                
                for item in items:
                    
                    new_data = copy.deepcopy(shell) #Stale reference BS here
                    new_data[x] = item
                    ans.append(new_data)
                nested_json.pop(row_num) #remove the object we split
                
                #Rebuild data with split rows
                ans = ans+nested_json
                return split_rows(ans) #create a new array with the split items and the remaining "rows"
    return nested_json #this means there were no arrays


#Now all we really need is a subroutine that goes "okay"
#Take the data, split dictionaries, then look for arrays and split those.  I believe any new arrays will also get split
#Then look at the results for new dictionaries or new

#egg = pd.json_normalize(NEW_DATA)

#egg_list = has_list(egg)

#print(egg)
#print(egg_list)


banana = flatten_json(NEW_DATA)
#banana = pd.DataFrame([flatten_json(NEW_DATA)])
#print(banana)

tomato = split_rows([banana])
print(tomato)

output = pd.DataFrame(tomato)
# Write the DataFrame to a CSV file
output.to_csv('check.csv', index=False)
