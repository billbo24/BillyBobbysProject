#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 22:12:36 2023

@author: williamfloyd
"""

import tkinter as tk
from pymongo.mongo_client import MongoClient
from src.config import get_mongo_host
from tkinter import messagebox


class ConnectFrame(tk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        
        label = tk.Label(self, text="Database View", font=("Helvetica", 16))
        label.pack(pady=10)
        self.controller = controller
        self.parent = parent

        #add_button = tk.Button(self, text="Add", command=self.perform_addition)
        #add_button.pack(pady=10)
        
        connect_to_mongo = tk.Button(self, text="Connect to Mongo", command=self.connect_to_mongo)
        connect_to_mongo.pack(pady=10)
        self.is_connected = False
        self.databases = []

    def connect_to_mongo(self):
        #Create a mongo client
        self.client = MongoClient(get_mongo_host())
        self.databases = self.client.list_database_names()
        
        
    
        #not 100% sure but I think this can work as a connection check
        #It checks if it's connected to a server that can accept writes??
        if len(self.databases) > 0:
            self.is_connected = True
            #messagebox.showinfo("Result","CONNECTED")
            #Then I'd like to tell it to go to the cluster page  from here
            #Okay I think this works! 
            self.controller.show_cluster()
            
            #Looks dumb but whatever
            self.parent.cluster_frame.client = self.client
            
        else:
            messagebox.showinfo("Result","WTF")