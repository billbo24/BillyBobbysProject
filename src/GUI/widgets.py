# I started with buttons but I think I like this more
import tkinter as tk


class DatabaseLabel(tk.Label):
    def __init__(self, parent, label_text, label_click):
        super().__init__(parent, text=label_text, foreground="white", background="red",cursor="hand2")
        
        #Alright, this is a bit confusing but this is how
        #You tell it to do something when you click on it
        self.bind("<Button-1>", lambda event: label_click(label_text))
        self.bind("<Enter>", lambda event: self.config(background="blue"))
        self.bind("<Leave>", lambda event: self.config(background="red"))