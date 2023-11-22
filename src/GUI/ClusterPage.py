#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 22:12:36 2023

@author: williamfloyd
"""


import tkinter as tk
from tkinter import ttk  # Import themed Tkinter
from src.GUI.CollectionsPage import CollectionsFrame


class ClusterFrame(tk.Frame):
    def __init__(self, parent,show_collections,data_app):
        super().__init__(parent)
        
        label = tk.Label(self, text="Connection Successful", font=("Helvetica", 16))
        label.pack(pady=10)
        
        label = tk.Label(self, text="Cluster View", font=("Helvetica", 16))
        label.pack(pady=10)
        
        #We've got an empty client, although by the time we actually see this page it has one
        self.client = None
        self.show_collections_function = show_collections
        self.parent = parent #This is overall app, we'd like to pass it to the collection page
        self.data_app = data_app

        view_databases = ttk.Button(self, text="View Databases", command=self.print_database)
        view_databases.pack(pady=10)
        
        self.my_variable = tk.StringVar()
        self.my_variable.set("Initial Value")
        
        self.label = tk.Label(self, textvariable=self.my_variable)
        self.label.pack(pady=10)

    #This is where we print the databases
    def print_database(self):
        
        b = self.client.list_database_names()
        #a = self.pretty_up_database_names(b)
        

        for db in b:
            DatabaseLabel(self, db, self.on_label_click)
        # self.my_variable.set(a)

    
    
    def on_label_click(self,database_name):
        self.data_app.collections_frame = CollectionsFrame(self.parent,self.data_app.show_cluster,self.client,database_name)
        self.show_collections_function()
        



# I started with buttons but I think I like this more
class DatabaseLabel(tk.Label):
    def __init__(self, parent, label_text, label_click):
        super().__init__(parent, text=label_text, foreground="white", background="red",cursor="hand2")
        self.pack(pady=5)
        
        #Alright, this is a bit confusing but this is how
        #You tell it to do something when you click on it
        self.bind("<Button-1>", lambda event: label_click(label_text))
        self.bind("<Enter>", lambda event: self.config(background="blue"))
        self.bind("<Leave>", lambda event: self.config(background="red"))
        
        
style = ttk.Style()
style.configure('TButton', padding=6, relief="flat")  # You can adjust padding and relief      
        
        
        
        