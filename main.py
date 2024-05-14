import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from licel_treatment import get_data, get_data2, get_calibration_data, get_polarization_data

class GUI:
    
    def set_config_directory(self):
        self.config_dir = tk.filedialog.askdirectory(initialdir=self.config_dir)
    
    def open_file(self):
        file_paths = tk.filedialog.askopenfilenames(initialdir=r'./austral-data-sample/instruments/lilas/private/measurement/2023/05/28')
        for file_path in file_paths:
            file_name = file_path.split('/')[-1]
            if file_name not in self.paths:
                self.paths[file_name] = file_path
                self.file_listbox.insert(tk.END, file_path.split('/')[-1])

    def select_all(self):
        self.file_listbox.select_set(0, tk.END)

    def unselect_all(self):
        self.file_listbox.select_clear(0, tk.END)

    @staticmethod
    def clean(object):
        for widget in object.winfo_children():
            widget.destroy()

    @staticmethod
    def get_color(channel, i):
        if i:
            waveln = int(channel.split('A')[0].split('P')[0])
        else:
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
    
    def get_new_fig(self):
        fig = plt.Figure()
        fig.tight_layout()
        ax = fig.add_subplot(111)
        return fig, ax
    
    def configure_ax(self, ax, xlab, ylab, tit):
        ax.set_xlabel(fontdict=self.plot_label_font, xlabel=xlab)   
        ax.set_ylabel(fontdict=self.plot_label_font, ylabel=ylab)
        ax.set_title(fontdict=self.plot_label_font, label=tit)  
        ax.set_yscale(self.curve_type)
        ax.legend()
        return ax
    
    def get_main_figure_with_ploted_data(self):
        fig, ax = self.get_new_fig()
        for channel in self.check_vars:
            if self.check_vars[channel].get():
                x, y = self.data[channel]
                ax.plot(x, y, label=channel)
        ax = self.configure_ax(ax, "Distance (m)", "Lidar Signal (mV)", "Lidar Profile")
        return fig
    
    def get_calibration_figure_with_ploted_data(self):
        fig, ax = self.get_new_fig()
        channel = self.selected_chan.get()
        for i, T in enumerate(self.calibration_data[channel]):
            x, y = T
            ax.plot(x, y, label=('+45', '-45', '0')[i])
        ax = self.configure_ax(ax, "Distance (m)", "δ* (-)", "Calibration")
        return fig

    def create_canvas_with_chart(self, fig, i):
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frames[i])
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frames[i])
        toolbar.update()

    def plot_main_data(self):
        GUI.clean(self.chart_frames[0])
        fig = self.get_main_figure_with_ploted_data()
        self.create_canvas_with_chart(fig, 0)

    def plot_calibration_data(self, event):
        GUI.clean(self.chart_frames[1])
        fig = self.get_calibration_figure_with_ploted_data()
        self.create_canvas_with_chart(fig, 1)
    
    def set_channel_box_vars(self):
        GUI.clean(self.check_frame)
        for channel in (self.data, self.calibration_data)[0]:
            var = tk.IntVar()
            check = tk.Checkbutton(self.check_frame, text=channel, variable=var, command=self.plot_main_data, bg=self.bg)
            check.pack(side='top', anchor='w')
            self.check_vars[channel] = var
    
    def set_licel_pull_down_menu(self):
        GUI.clean(self.licel_selection_frame)
        self.selection_vars = []
        selected_files = [self.file_listbox.get(file_index) for file_index in self.file_listbox.curselection()]
        for i in range(3):
            selected_option = tk.StringVar()
            option_menu = tk.OptionMenu(self.licel_selection_frame, selected_option, *selected_files)
            option_menu.grid(column=0, row=2*i+1, sticky='nsew')
            self.selection_vars.append(selected_option)
        self.set_button = tk.Button(self.licel_selection_frame, text="Set", command=self.set_channel_pull_down_menu, bg='white')
        self.set_button.grid(column=0, row=6, sticky='nsew')

    def set_channel_pull_down_menu(self):
        GUI.clean(self.channel_selection_frame)
        file_names = [var.get() for var in self.selection_vars]
        if file_names[0] != '' and file_names[1] != '':
            if file_names[2] == '':
                file_names.pop()
            file_names = [self.paths[file_name] for file_name in file_names]
            self.calibration_data = get_polarization_data(file_names, self.config_dir, self.shift, self.bg_noise, self.e_noise, self.deadtime)
            option_menu = tk.OptionMenu(self.channel_selection_frame, self.selected_chan, *self.calibration_data.keys(), command=self.plot_calibration_data)
            option_menu.grid(column=0, row=1, sticky='nsew')
    
    def set_data_with_selected_files(self):
        selected_files = self.file_listbox.curselection()
        if selected_files != ():
            self.data = get_data2([self.paths[self.file_listbox.get(file_index)] for file_index in selected_files], self.config_dir, not self.shift.get(), self.bg_noise.get(), not self.e_noise.get(), not self.deadtime.get())
        else:
            self.data = {}

    def load_data(self):
        for i in range(2):
            GUI.clean(self.chart_frames[i])
        self.set_data_with_selected_files()
        self.set_channel_box_vars()
        self.set_licel_pull_down_menu()
    
    def on_select(self, event):
        self.load_data()

                
    def configure_grid(self):
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=0)
        self.root.grid_columnconfigure(3, weight=0)
        self.tabs[0].grid_rowconfigure(0, weight=0)
        self.tabs[0].grid_rowconfigure(1, weight=1)
        self.tabs[0].grid_rowconfigure(2, weight=0)
        self.tabs[0].grid_columnconfigure(0, weight=1)
        self.tabs[0].grid_columnconfigure(1, weight=0) 
        self.tabs[1].grid_rowconfigure(0, weight=0)
        self.tabs[1].grid_rowconfigure(1, weight=1)
        self.tabs[1].grid_rowconfigure(2, weight=0)
        self.tabs[1].grid_columnconfigure(0, weight=1)
        self.tabs[1].grid_columnconfigure(1, weight=0) 
    
    def place_elements(self):
        self.notebook.grid(row=0, column=1, rowspan = 4, sticky='nsew')
        for i in range(2):
            self.chart_frames[i].grid(column=0, row=1, sticky='nsew')
            self.title_labels[i].grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.check_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.licel_selection_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.channel_selection_frame.grid(row=2, column=1, sticky='nsew')
        self.file_list_frame.grid(row=1, column=0, sticky='nsew')
        self.file_listbox.pack(fill='both', expand=True)
        self.load_button.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.selectall_button.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        self.unselectall_button.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        
    def configure_menubar(self):
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        ##########################
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Exit", command=self.root.destroy)


        self.menubar.add_cascade(label="Config", menu=self.config_menu)
        ##########################
        self.config_menu.add_command(label="Set config directory", command=self.set_config_directory)
        self.config_menu.add_checkbutton(label="E-Noise", variable=self.e_noise, command=self.load_data)
        self.config_menu.add_checkbutton(label="Shift", variable=self.shift, command=self.load_data)
        self.config_menu.add_checkbutton(label="Background Noise", variable=self.bg_noise, command=self.load_data)
        self.config_menu.add_checkbutton(label="Deadtime", variable=self.deadtime, command=self.load_data)
        
    def configure_root(self):
        self.root.title("Austral GUI")
        #self.root.geometry(f'{self.w}x{self.h}')
        self.root.config(bg=self.bg)
        self.root.config(menu=self.menubar)
        #self.root.state('zoomed') for windows
        #self.root.wm_attributes('-zoomed', True)  # This line maximizes the window.


    @staticmethod
    def rien():
        pass
    
    def toggle_log(self):
        if self.curve_type == 'log':
            self.curve_type = 'linear'
        else:
             self.curve_type = 'log'
        self.load_data()

    def __init__(self):
        self.root = tk.Tk()
        
        self.data = {}
        self.calibration_data = {}
        self.config_dir = r'./austral-data-sample/instruments/lilas/private/config/lidar'
        self.paths = {} 
        self.check_vars = {}
        self.selection_vars = []
        
        self.bg = '#de755e'
        self.w, self.h = 700, 500
        self.figure_width = 5  # in inches
        self.figure_height = 5
        self.curve_type = 'linear' #linear, log, etc
        self.plot_label_font = {'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 12}
        self.label_style = {'background':self.bg, 'font':('Times New Roman', 12)}
        self.dpi = self.root.winfo_fpixels('1i')  # pixels per inch
        self.canvas_width = int(self.dpi * self.figure_width)
        self.canvas_height = int(self.dpi * self.figure_height)
        
        self.bg_noise = tk.IntVar()
        self.e_noise = tk.IntVar()
        self.shift = tk.IntVar()
        self.deadtime = tk.IntVar()
        self.selected_chan = tk.StringVar()

        self.notebook = ttk.Notebook(self.root)
        self.tabs = (ttk.Frame(self.notebook), ttk.Frame(self.notebook))
        self.notebook.add(self.tabs[0], text='Lidar Profiles')
        self.notebook.add(self.tabs[1], text='Calibration Depolarization')
        
        self.menubar = tk.Menu(self.root)
        self.chart_frames = tuple([tk.Frame(tab, bg=self.bg) for tab in self.tabs])
        self.file_list_frame = tk.Frame(self.root, bg=self.bg)
        self.file_listbox = tk.Listbox(self.file_list_frame, selectmode=tk.MULTIPLE)
        self.load_button = tk.Button(self.root, text="Load", command=self.load_data, bg='white')
        self.selectall_button = tk.Button(self.root, text="Select All", command=self.select_all, bg='white')
        self.unselectall_button = tk.Button(self.root, text="Unselect All", command=self.unselect_all, bg='white')
        
        self.title_labels = (tk.Label(self.tabs[0], text="Data from files", **self.label_style),
                             tk.Label(self.tabs[1], text="Calibration", **self.label_style))
        self.check_frame = tk.Frame(self.tabs[0], bg=self.bg)
        self.licel_selection_frame = tk.Frame(self.tabs[1], bg=self.bg)
        self.channel_selection_frame = tk.Frame(self.tabs[1], bg=self.bg)
        
        

        self.file_menu = tk.Menu(self.menubar)
        self.config_menu = tk.Menu(self.menubar)


        self.configure_grid()
        self.configure_root()
        self.place_elements()
        self.configure_menubar()
        #self.file_listbox.bind('<<ListboxSelect>>', self.on_select)
        
        self.root.mainloop()
    
        
gui = GUI()