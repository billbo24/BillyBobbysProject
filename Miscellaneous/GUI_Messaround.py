#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 11:25:00 2023

@author: williamfloyd
"""
import tkinter as tk
from tkinter import messagebox

class MathApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Math Operations App")
        self.geometry("400x200")

        self.addition_frame = AdditionFrame(self)
        self.multiplication_frame = MultiplicationFrame(self)
        
        self.add_btn = tk.Button(
            text="show_addition",
            command=self.show_addition,
        )
        
        
        
        self.mult_btn = tk.Button(

            text="show_multiplication",
            command=self.show_multiplication,
        )
        
        self.add_btn.pack(side=tk.LEFT)
        self.mult_btn.pack(side=tk.RIGHT)
        

        self.addition_frame.pack(fill=tk.BOTH, expand=True)
        #self.multiplication_frame.pack(fill=tk.BOTH, expand=True)



        # Add a button to toggle between views
        #toggle_button = tk.Button(self, text="Toggle View", command=self.toggle_view)
        #toggle_button.pack(pady=10)

            
            
    def show_addition(self):
        self.multiplication_frame.pack_forget()
        self.addition_frame.pack(expand=True, fill=tk.BOTH)

    def show_multiplication(self):
        self.addition_frame.pack_forget()
        self.multiplication_frame.pack(expand=True, fill=tk.BOTH)

class AdditionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Addition View", font=("Helvetica", 16))
        label.pack(pady=10)

        self.entry1 = tk.Entry(self)
        self.entry2 = tk.Entry(self)

        self.entry1.pack(pady=5)
        self.entry2.pack(pady=5)

        add_button = tk.Button(self, text="Add", command=self.perform_addition)
        add_button.pack(pady=10)

    def perform_addition(self):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            result = num1 + num2
            messagebox.showinfo("Result", f"The sum is: {result}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")





class MultiplicationFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Multiplication View", font=("Helvetica", 16))
        label.pack(pady=10)

        self.entry1 = tk.Entry(self)
        self.entry2 = tk.Entry(self)

        self.entry1.pack(pady=5)
        self.entry2.pack(pady=5)

        multiply_button = tk.Button(self, text="Multiply", command=self.perform_multiplication)
        multiply_button.pack(pady=10)

    def perform_multiplication(self):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            result = num1 * num2
            messagebox.showinfo("Result", f"The product is: {result}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    app = MathApp()
    app.mainloop()










class Base(object):
    def __init__(self):
        print("Base created")
        
class ChildA(Base):
    def __init__(self):
        Base.__init__(self)
        
class ChildB(Base):
    def __init__(self):
        super(ChildB, self).__init__()
        
ChildA() 
ChildB()
