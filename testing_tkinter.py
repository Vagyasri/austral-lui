#!/usr/bin/env python3
import os
import tkinter as tk

os.environ["DISPLAY"] = ":0.0"
root = tk.Tk()

label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

root.mainloop()