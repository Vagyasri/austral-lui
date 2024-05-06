#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import tkinter as tk
from tkinter import filedialog, Text, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def new_file():
    text.delete("1.0", tk.END)

def open_file():
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        content = file.read()
    text.delete("1.0", tk.END)
    text.insert('insert', content)

def save_file():
    file_path = filedialog.asksaveasfilename()
    with open(file_path, 'w') as file:
        content = text.get("1.0", tk.END)
        file.write(content)

def about():
    messagebox.showinfo("About", "This is a simple Tkinter GUI")
    
def draw_pie_chart():
    # Create a new Tkinter Toplevel widget
    top = tk.Toplevel(root)

    # Create a matplotlib figure
    fig = plt.Figure(figsize=(5, 5))

    # Create some data
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]

    # Add a subplot to the figure
    ax = fig.add_subplot(111)

    # Draw a pie chart in the subplot
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Create a FigureCanvasTkAgg widget and add it to the Toplevel widget
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title("Simple Tkinter GUI")

# Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create a pie chart
menubar.add_command(label="Draw Pie Chart", command=draw_pie_chart)

# Create a File menu
file_menu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

# Create a Help menu
help_menu = tk.Menu(menubar)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

# Create a text widget
text = Text(root)
text.pack(expand=True, fill='both')

# Create a status bar
statusbar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
statusbar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()

