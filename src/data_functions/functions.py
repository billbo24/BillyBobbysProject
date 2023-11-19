#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 19:53:34 2023

@author: williamfloyd
A collection of functions that will interface with the data.  

"""


import json


def prepare_pandas_for_mongo(input_pandas): 
    #We can alter the orient argument if we like, but generally this is 
    #how I like to think about pandas data, not by columns
    a = input_pandas.to_json(orient='records')
    b = json.loads(a) 
    
    #b is not ready to be pushed into the database, it's already in 
    #a python array
    return b
    
