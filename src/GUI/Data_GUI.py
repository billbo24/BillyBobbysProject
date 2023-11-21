#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 20:23:03 2023

@author: williamfloyd
I'm not sure if this is the best thing to do, but I think I'm going
to keep all the pages on separate programs and import them.  The connect page is
more or less fine for the moment I suppose

Gonna put the "clickable object" in the Cluster Page since that's where I plan on 
using it
"""

import sys
sys.path.insert(0, '/Users/williamfloyd/Documents/PythonCode/BillyBobbysProject/')

from src.GUI.ClusterPage import ClusterFrame
from src.GUI.ConnectPage import ConnectFrame
from src.GUI.CollectionsPage import CollectionsFrame


import tkinter as tk
from tkinter import messagebox
from pymongo.mongo_client import MongoClient
from src.config import get_mongo_host
from dotenv import load_dotenv


#Had the full filepath on my machine, but that's not helpful for everyone else.  
#Replace the .env string here

#load_dotenv('env')
load_dotenv('/Users/williamfloyd/Documents/PythonCode/BillyBobbysProject/env')

MongoClient(get_mongo_host())

class DataApp(tk.Tk):
    def __init__(self):
        super().__init__()

        #Basic 
        self.title("Data App")
        self.geometry("400x400")

        
        self.connect_frame = ConnectFrame(self,self)
        self.connect_frame.pack(fill=tk.BOTH, expand=True)
        
        self.cluster_frame = ClusterFrame(self,self.show_collection,self)
        
        #The collections frame needs to come with a few other things
        self.collections_frame= CollectionsFrame(self,self.show_cluster,None,None)
        
        #if self.connect_frame.is_connected:
            #self.show_cluster

        #self.clust_button = tk.Button(

            #text="go to cluster",
            #command=self.show_cluster,
        #)
        #self.clust_button.pack(side=tk.LEFT)
        
    def show_connect(self):
        self.connect_frame.pack(expand=True, fill=tk.BOTH)
        self.cluster_frame.pack_forget()
        self.collections_frame.pack_forget()


    def show_cluster(self):
        if self.connect_frame.is_connected:
            self.connect_frame.pack_forget()
            self.cluster_frame.pack(expand=True, fill=tk.BOTH)
            self.collections_frame.pack_forget()
        else:
            messagebox.showinfo("Error","You're Not Connected")

    
    def show_collection(self):
        self.cluster_frame.pack_forget()
        self.connect_frame.pack_forget()
        self.collections_frame.pack(expand=True, fill=tk.BOTH)





if __name__ == "__main__":
    app = DataApp()
    app.mainloop()
