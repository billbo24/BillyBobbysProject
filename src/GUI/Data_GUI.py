#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 20:23:03 2023

@author: williamfloyd
"""

import tkinter as tk
from tkinter import messagebox
from pymongo.mongo_client import MongoClient
from src.config import get_mongo_host
from dotenv import load_dotenv

#Had the full filepath on my machine, but that's not helpful for everyone else.  
#Replace the .env string here

load_dotenv('env')
MongoClient(get_mongo_host())

class DataApp(tk.Tk):
    def __init__(self):
        super().__init__()

        #Basic 
        self.title("Data App")
        self.geometry("400x400")

        
        self.connect_frame = ConnectFrame(self,self)
        self.connect_frame.pack(fill=tk.BOTH, expand=True)
        
        self.cluster_frame = ClusterFrame(self)
        
        #if self.connect_frame.is_connected:
            #self.show_cluster

        #self.clust_button = tk.Button(

            #text="go to cluster",
            #command=self.show_cluster,
        #)
        #self.clust_button.pack(side=tk.LEFT)
        
    def show_connect(self):
        self.cluster_frame.pack_forget()
        self.connect_frame.pack(expand=True, fill=tk.BOTH)

    def show_cluster(self):
        if self.connect_frame.is_connected:
            self.connect_frame.pack_forget()
            self.cluster_frame.pack(expand=True, fill=tk.BOTH)
        else:
            messagebox.showinfo("Error","You're Not Connected")


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
            messagebox.showinfo("Result","CONNECTED")
            #Then I'd like to tell it to go to the cluster page  from here
            #Okay I think this works! 
            self.controller.show_cluster()
            
            #Looks dumb but whatever
            self.parent.cluster_frame.client = self.client
            
        else:
            messagebox.showinfo("Result","WTF")


class ClusterFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        label = tk.Label(self, text="Cluster View", font=("Helvetica", 16))
        label.pack(pady=10)
        
        #We've got an empty client
        self.client = None

        #add_button = tk.Button(self, text="Add", command=self.perform_addition)
        #add_button.pack(pady=10)
        

        view_databases = tk.Button(self, text="View Databases", command=self.print_database)
        view_databases.pack(pady=10)
        
        self.my_variable = tk.StringVar()
        self.my_variable.set("Initial Value")
        
        self.label = tk.Label(self,textvariable=self.my_variable)
        self.label.pack(pady=10)

    
    def print_database(self):
        #print(self.client.list_database_names())
        b = self.client.list_database_names()
        a = self.pretty_up_database_names(b)
        self.my_variable.set(a)
    
    #no fuckin clue why we need the self argument here
    def pretty_up_database_names(self,names):
        ans = ''
        for i in names:
            ans += i + '\n '
        return ans

if __name__ == "__main__":
    app = DataApp()
    app.mainloop()
