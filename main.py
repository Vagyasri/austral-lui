import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from licel_treatment import get_data

def set_config_directory():
    global config_dir
    config_dir = tk.filedialog.askdirectory()
    
def get_color(channel):
    waveln = int(channel.split('.')[0])
    if waveln < 400:
        return '#A600D5'
    elif waveln == 408:
        return '#8108FF'
    elif waveln == 460:
        return '#0051FF'
    elif 529 < waveln < 533:
        return '#BCFF00'
    else:
        return '#AF0000'

def open_file():
    file_paths = tk.filedialog.askopenfilenames()
    for file_path in file_paths:
        file_name = file_path.split('/')[-1]
        if file_name not in paths:
            paths[file_name] = file_path
            file_listbox.insert(tk.END, file_path.split('/')[-1])

def load_files():
    selected_files = file_listbox.curselection()
    for widget in check_frame.winfo_children():
        widget.destroy()
    if selected_files != ():
        global data
        data |= get_data([paths[file_listbox.get(file_index)] for file_index in selected_files], config_dir, shift.get(), bg_noise.get(), e_noise.get(), deadtime.get())
    
        for channel in data:
            var = tk.IntVar()
            check = tk.Checkbutton(check_frame, text=channel, variable=var, command=draw_chart, bg='blanched almond')
            check.pack(side='top', anchor='w')
            check_vars[channel] = var



def draw_chart():
    # Clear the chart
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    # Get the size of the Canvas in pixels
    canvas_width = chart_frame.winfo_width()
    canvas_height = chart_frame.winfo_height()
    
    # Convert the size from pixels to inches
    dpi = root.winfo_fpixels('1i')  # pixels per inch
    figure_width = canvas_width / dpi -0.2
    figure_height = canvas_height / dpi -0.2
    
    fig = plt.Figure(figsize=(figure_width, figure_height))
    ax = fig.add_subplot(111)
    
    
    # Draw a line plot for each selected channel
    for channel in check_vars:
        if check_vars[channel].get():
            x, y = data[channel]
            ax.plot(x, y, label=channel, color=get_color(channel))

    ax.legend()
    fig.tight_layout()
    # Create a FigureCanvasTkAgg widget and add it to the frame
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
  
paths = {} 
data = {}
check_vars = {}
config_dir = r'\\wsl.localhost\Ubuntu-22.04\home\neuts\project\austral-data-sample\instruments\lilas\private\config\lidar'

root = tk.Tk()
root.title("Austral GUI")
root.config(bg='blanched almond')

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=0)


# Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

chart_frame = tk.Frame(root, bg='blanched almond')
chart_frame.grid(column=1, columnspan=2, row=1, sticky='nsew')

# Create a frame for the file list
file_list_frame = tk.Frame(root, bg='blanched almond')
file_list_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')

# Create a Listbox in the file_list_frame
file_listbox = tk.Listbox(file_list_frame, selectmode=tk.MULTIPLE)
file_listbox.pack(fill='both', expand=True)

# Create a Load button
load_button = tk.Button(root, text="Load", command=load_files, bg='white')
load_button.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

# Create a label for the title
title_label = tk.Label(root, background='blanched almond', foreground='blue', text="Data from files", font=('Times New Roman', 12))
title_label.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)
# Create a label for the x-axis
x_label = tk.Label(root, background='blanched almond', font=('Times New Roman', 12), text="distance (m)")
x_label.grid(row=2, column=1, columnspan=2, sticky='nsew', padx=10, pady=10)

# Create a label for the y-axis and rotate it
y_label = tk.Label(root, background='blanched almond', font=('Times New Roman', 12), text="Lidar Signal (mV)", width=20)
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

# Create a frame for the Checkbuttons
check_frame = tk.Frame(root, bg='blanched almond')
check_frame.grid(row=0, column=3, rowspan=3, sticky='nsew')


# Create a File menu
file_menu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Exit", command=root.destroy)


# Create a Config menu
config_menu = tk.Menu(menubar)
menubar.add_cascade(label="Config", menu=config_menu)

bg_noise = tk.IntVar()
e_noise = tk.IntVar()
shift = tk.IntVar()
deadtime = tk.IntVar()
config_menu.add_command(label="Set config directory", command=set_config_directory)
config_menu.add_checkbutton(label="E-Noise", variable=e_noise, command=load_files)
config_menu.add_checkbutton(label="Shift", variable=shift, command=load_files)
config_menu.add_checkbutton(label="Background Noise", variable=bg_noise, command=load_files)
config_menu.add_checkbutton(label="Deadtime", variable=deadtime, command=load_files)


root.mainloop()


