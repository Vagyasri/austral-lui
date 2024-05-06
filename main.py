import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from licel_treatment import get_data

class GUI:
    
    def set_config_directory(self):
        self.config_dir = tk.filedialog.askdirectory(initialdir=self.config_dir)
    
    def open_file(self):
        file_paths = tk.filedialog.askopenfilenames()
        for file_path in file_paths:
            file_name = file_path.split('/')[-1]
            if file_name not in self.paths:
                self.paths[file_name] = file_path
                self.file_listbox.insert(tk.END, file_path.split('/')[-1])
            
    def load_files(self):
        selected_files = self.file_listbox.curselection()
        for widget in self.check_frame.winfo_children():
                widget.destroy()
        if selected_files != ():
            self.data |= get_data([self.paths[self.file_listbox.get(file_index)] for file_index in selected_files], self.config_dir, self.shift.get(), self.bg_noise.get(), self.e_noise.get(), self.deadtime.get())
        
            for channel in self.data:
                var = tk.IntVar()
                check = tk.Checkbutton(self.check_frame, text=channel, variable=var, command=self.draw_chart, bg=self.bg)
                check.pack(side='top', anchor='w')
                self.check_vars[channel] = var
    
    @staticmethod
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
        
    def draw_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        frame_width = self.chart_frame.winfo_width()
        frame_height = self.chart_frame.winfo_height()
        figure_width, figure_height = frame_width / self.dpi - 0.2, frame_height / self.dpi - 0.2
        fig = plt.Figure(figsize=(figure_width, figure_height))
        ax = fig.add_subplot(111)
        
        for channel in self.check_vars:
            if self.check_vars[channel].get():
                x, y = self.data[channel]
                ax.plot(x, y, label=channel, color=GUI.get_color(channel))

        ax.legend()
        fig.tight_layout()
        # Create a FigureCanvasTkAgg widget and add it to the frame
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def configure_grid(self):
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=0)
    
    def place_elements(self):
        self.chart_frame.grid(column=1, columnspan=2, row=1, sticky='nsew')
        self.file_list_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.file_listbox.pack(fill='both', expand=True)
        self.load_button.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        self.title_label.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)
        self.x_label.grid(row=2, column=1, columnspan=2, sticky='nsew', padx=10, pady=10)
        self.y_label.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.blank_canvas.pack()
        self.check_frame.grid(row=0, column=3, rowspan=3, sticky='nsew')
        
    def configure_menubar(self):
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        ##########################
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Exit", command=self.root.destroy)


        self.menubar.add_cascade(label="Config", menu=self.config_menu)
        ##########################
        self.config_menu.add_command(label="Set config directory", command=self.set_config_directory)
        self.config_menu.add_checkbutton(label="Disable E-Noise", variable=self.e_noise, command=self.load_files)
        self.config_menu.add_checkbutton(label="Disable Shift", variable=self.shift, command=self.load_files)
        self.config_menu.add_checkbutton(label="Disable Background Noise", variable=self.bg_noise, command=self.load_files)
        self.config_menu.add_checkbutton(label="Disable Deadtime", variable=self.deadtime, command=self.load_files)
        
    def configure_root(self):
        self.root.title("Austral GUI")
        self.root.config(bg=self.bg)
        self.root.config(menu=self.menubar)
        
    def __init__(self):
        self.root = tk.Tk()
        
        self.data = {}
        self.config_dir = r'\\wsl.localhost\Ubuntu-22.04\home\neuts\project\austral-data-sample\instruments\lilas\private\config\lidar'
        self.paths = {} 
        self.check_vars = {}
        
        self.bg = 'blanched almond'
        self.figure_width = 5  # in inches
        self.figure_height = 5

        self.dpi = self.root.winfo_fpixels('1i')  # pixels per inch
        self.canvas_width = int(self.dpi * self.figure_width)
        self.canvas_height = int(self.dpi * self.figure_height)
        
        self.bg_noise = tk.IntVar()
        self.e_noise = tk.IntVar()
        self.shift = tk.IntVar()
        self.deadtime = tk.IntVar()
        
        
        self.menubar = tk.Menu(self.root)
        self.chart_frame = tk.Frame(self.root, bg=self.bg)
        self.file_list_frame = tk.Frame(self.root, bg=self.bg)
        self.file_listbox = tk.Listbox(self.file_list_frame, selectmode=tk.MULTIPLE)
        self.load_button = tk.Button(self.root, text="Load", command=self.load_files, bg='white')
        self.title_label = tk.Label(self.root, background=self.bg, foreground='blue', text="Data from files", font=('Times New Roman', 12))
        self.x_label = tk.Label(self.root, background=self.bg, font=('Times New Roman', 12), text="distance (m)")
        self.y_label = tk.Label(self.root, background=self.bg, font=('Times New Roman', 12), text="Lidar Signal (mV)", width=20)
        self.blank_canvas = tk.Canvas(self.chart_frame, width=self.canvas_width, height=self.canvas_height, bg=self.bg)
        self.check_frame = tk.Frame(self.root, bg=self.bg)
        self.file_menu = tk.Menu(self.menubar)
        self.config_menu = tk.Menu(self.menubar)


        self.configure_grid()
        self.configure_root()
        self.place_elements()
        self.configure_menubar()
        
        
        self.root.mainloop()
    
        
gui = GUI()


