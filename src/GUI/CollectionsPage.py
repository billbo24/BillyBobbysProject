#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 22:57:12 2023

@author: williamfloyd
"""

import tkinter as tk
from tkinter import ttk  # Import themed Tkinter

class CollectionsFrame(tk.Frame):
    def __init__(self, parent,send_back_function,client,database):
        super().__init__(parent)
        
        #Note at this point we can only be here if we're connected, so we may as well
        #Pass the mongo client in
        self.client = client
        
        label = tk.Label(self, text=f"The {database} database", font=("Helvetica", 16))
        label.pack(pady=10)
        
        
        #view_databases = ttk.Button(self, text="View Databases", command=self.print_database)
        #view_databases.pack(pady=10)
        
        #Make a list displaying the collections
        self.my_variable = tk.StringVar()
        
        #I passed the database as a string.  I did pass a none client in the make a 
        #Blank version of this in the initial phase though, so I have to 
        #do it this way.  
        try:
            print(self.client[f'{database}'].list_collection_names())
            self.pretty_up_collections_names(database)
            #self.my_variable.set()
            
        except:
            self.my_variable.set("Something has gone very wrong")
        
        self.label = tk.Label(self, textvariable=self.my_variable)
        self.label.pack(pady=10)


        # add_button = ttk.Button(self, text="Add", command=self.perform_addition)
        # add_button.pack(pady=10)

        GO_BACK = ttk.Button(self, text="Go Back", command=send_back_function)
        GO_BACK.pack(pady=10)
        
  
    def pretty_up_collections_names(self,database):
        names = self.client[f'{database}'].list_collection_names()
        print("ANYTHING")
        ans = ''
        for i in names:
            ans += i + '\n '
        self.my_variable.set(ans)
            