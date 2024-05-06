import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def txt_to_lists(content):
    T0, T1 = [], []
    for line in content.split('\n'):
        line0 = line.split()
        T0.append(float(line0[0]))
        T1.append(float(line0[1]))
    return T0, T1
"""    
def new_file():
    for widget in chart_frame.winfo_children():
        widget.destroy()
"""
def open_file():
    file_path = tk.filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        content = file.read()
    x, y = txt_to_lists(content)
    draw_chart(x, y)
    
    file_listbox.insert(tk.END, file_path.split('/')[-1])

def save_file():
    pass
    """
    file_path = tk.filedialog.asksaveasfilename()
    with open(file_path, 'w') as file:
        content = text.get("1.0", tk.END)
        file.write(content)
    """
"""
def about():
    tk.messagebox.showinfo("About", "This is a simple Tkinter GUI")
"""
def draw_chart(x, y):
    # Create a new Tkinter Toplevel widget
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Get the size of the Canvas in pixels
    canvas_width = chart_frame.winfo_width()
    canvas_height = chart_frame.winfo_height()

    # Convert the size from pixels to inches
    dpi = root.winfo_fpixels('1i')  # pixels per inch
    figure_width = canvas_width / dpi -0.2
    figure_height = canvas_height / dpi -0.2

    # Create a matplotlib figure with the same size as the Canvas
    fig = plt.Figure(figsize=(figure_width, figure_height))

    # Add a subplot to the figure
    ax = fig.add_subplot(111)

    # Draw a line plot in the subplot
    ax.plot(x, y)
    #ax.set_yscale('linear')
    
    # Remove margins
    fig.tight_layout()

    # Create a FigureCanvasTkAgg widget and add it to the pie_chart_frame
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    



root = tk.Tk()
root.title("Austral GUI")

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)


# Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

chart_frame = tk.Frame(root)
chart_frame.grid(column=1, columnspan=2, row=1, sticky='nsew')

# Create a frame for the file list
file_list_frame = tk.Frame(root)
file_list_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')

# Create a Listbox in the file_list_frame
file_listbox = tk.Listbox(file_list_frame)
file_listbox.pack(fill='both', expand=True)

# Create a label for the title
title_label = tk.Label(root, text="Title")
title_label.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)
# Create a label for the x-axis
x_label = tk.Label(root, text="Abscisse")
x_label.grid(row=2, column=1, columnspan=2, sticky='nsew', padx=10, pady=10)

# Create a label for the y-axis and rotate it
y_label = tk.Label(root, text="Ordonnées", width=20)
y_label.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

# Define the size of the figure in inches
figure_width = 5  # in inches
figure_height = 5  # in inches

# Convert the size from inches to pixels
dpi = root.winfo_fpixels('1i')  # pixels per inch
canvas_width = int(dpi * figure_width)
canvas_height = int(dpi * figure_height)

# Create a blank canvas in the frame with the same size as the figure
blank_canvas = tk.Canvas(chart_frame, width=canvas_width, height=canvas_height, bg='blanched almond')
blank_canvas.pack()



# Create a File menu
file_menu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=file_menu)
#file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

file_menu.add_command(label="Exit", command=root.destroy)

# Create a Help menu
#help_menu = tk.Menu(menubar)
#menubar.add_cascade(label="Help", menu=help_menu)
#help_menu.add_command(label="About", command=about)


root.mainloop()





