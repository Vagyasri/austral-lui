import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from licel_treatment import get_data, get_data2, get_calibration_data, get_polarization_data, get_V_star
import numpy as np
class GUI:
    
    def set_config_directory(self):
        self.config_dir = tk.filedialog.askdirectory(initialdir=self.config_dir)
#r'./au stral-data-sample/instruments/lilas/private/measurement/2023/05/28')
    def open_file(self):
        file_paths = tk.filedialog.askopenfilenames(initialdir=r'./austral-data-sample/instruments/lilas/private/calibration/20210112/200449')
        for file_path in file_paths:
            file_name = file_path.split('/')[-1]
            if file_name not in self.paths:
                self.paths[file_name] = file_path
                self.file_listbox.insert(tk.END, file_path.split('/')[-1])
        self.set_licel_pull_down_menu()
        
    def select_all(self):
        self.file_listbox.select_set(0, tk.END)

    def unselect_all(self):
        self.file_listbox.select_clear(0, tk.END)

    def select_all_filters(self):
        # Set all variables to True
        self.e_noise.set(1)
        self.shift.set(1)
        self.bg_noise.set(1)
        self.deadtime.set(1)
        self.load_data()
    
    def unselect_all_filters(self):
        # Set all variables to True
        self.e_noise.set(0)
        self.shift.set(0)
        self.bg_noise.set(0)
        self.deadtime.set(0)
        self.load_data()

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
    
    def configure_ax(self, ax, xlab, ylab, tit, there_are_data=True):
        ax.set_xlabel(fontdict=self.plot_label_font, xlabel=xlab)   
        ax.set_ylabel(fontdict=self.plot_label_font, ylabel=ylab)
        ax.set_title(fontdict=self.plot_label_font, label=tit)  
        ax.set_yscale(self.curve_type)
        if there_are_data:
            ax.legend()
            #ax.set_xlim(-1000, 5000)
        return ax
    
    def get_main_figure_with_ploted_data(self):
        selected_channels = self.chan_listbox.curselection()
        fig, ax = self.get_new_fig()
        ax.set_xlim(-100, self.main_xlim)
        for channel_index in selected_channels:
            channel = self.chan_listbox.get(channel_index)
            x, y = self.data[channel]
            ax.plot(x, y, label=channel)
        there_are_data = selected_channels != ()
        ax = self.configure_ax(ax, "Distance (m)", "Lidar Signal (mV)", "Lidar Profile", there_are_data)
        return fig
    @staticmethod
    def make_data_regular(x, y):
        if len(x) != len(y):
            x.pop()

    def find_ylim(self, channel):
        X, Y = [], []
        for i in range(2):
            x, y = self.calibration_data[channel][i]
            GUI.make_data_regular(x, y)
            X.extend(x)
            Y.extend(y)
        mask = (np.array(X) <= self.calib_xlim)
        y_range = np.array(Y)[mask]
        mean, std = np.nanmean(y_range), np.nanstd(y_range)
        return mean - self.num_std*std, mean + self.num_std*std
        
    def get_calibration_figure_with_ploted_data(self):
        fig, ax = self.get_new_fig()
        ax.set_xlim(-100, self.calib_xlim)
        channel = self.selected_chan.get()
        y_minmax = self.find_ylim(channel)
        for i, T in enumerate(self.calibration_data[channel]):
            x, y = T
            ax.plot(x, y, label=('+45', '-45', '0')[i])
        if self.v_star.get():
            ax.axhline(y=float(self.v_star.get()), linestyle='--', label='V*')
        ax.set_xlim(-100, self.calib_xlim)
        ax.set_ylim(*y_minmax)
        ax = self.configure_ax(ax, "Distance (m)", "δ* (-)", "Calibration")
        return fig

    def create_canvas_with_chart(self, fig, i):
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frames[i])
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frames[i])
        toolbar.update()

    def plot_main_data(self, event):
        GUI.clean(self.chart_frames[0])
        fig = self.get_main_figure_with_ploted_data()
        self.create_canvas_with_chart(fig, 0)

    def plot_calibration_data(self):
        GUI.clean(self.chart_frames[1])
        fig = self.get_calibration_figure_with_ploted_data()
        self.create_canvas_with_chart(fig, 1)

    def set_chan_listbox(self):
        self.chan_listbox.delete(0, tk.END)
        for channel in self.data:
            self.chan_listbox.insert(tk.END, channel)
            self.chan_listbox.grid(sticky='nsew')
    
    def set_licel_pull_down_menu(self):
        GUI.clean(self.licel_selection_frame)
        GUI.clean(self.channel_selection_frame)
        self.selection_vars = []
        selected_files = self.file_listbox.get(0, tk.END)
        txt_labels = ['Select file +45 :', 'Select file -45 :', 'Select file 0 :']
        for i in range(3):
            selected_option = tk.StringVar()
            option_menu = tk.OptionMenu(self.licel_selection_frame, selected_option, *selected_files)
            label = tk.Label(self.licel_selection_frame, text=txt_labels[i], **self.label_style, anchor='center')
            label.grid(sticky='ew', padx=5, pady=5)
            option_menu.grid(sticky='nsew')
            self.selection_vars.append(selected_option)
        self.set_button = tk.Button(self.licel_selection_frame, text="Set", command=self.set_channel_pull_down_menu, bg='white')
        self.set_button.grid(sticky='ew')

    def set_channel_pull_down_menu(self):
        GUI.clean(self.channel_selection_frame)
        GUI.clean(self.v_star_frame)
        self.selected_chan.set('')
        file_names = [var.get() for var in self.selection_vars]
        if file_names[0] != '' and file_names[1] != '':
            if file_names[2] == '':
                file_names.pop()
            file_names = [self.paths[file_name] for file_name in file_names]
            self.calibration_data = get_polarization_data(file_names, self.config_dir, self.shift.get(), self.bg_noise.get(), self.e_noise.get(), self.deadtime.get())
            option_menu = tk.OptionMenu(self.channel_selection_frame, self.selected_chan, *self.calibration_data.keys(), command=self.set_v_star_menu_and_plot_calibration_data)
            chan_label = tk.Label(self.channel_selection_frame, text="Select channel :", **self.label_style, anchor='center')
            chan_label.grid(sticky='ew', padx=5, pady=5)
            option_menu.grid(sticky='nsew')
            
    
    @staticmethod
    def validate(P):
        # P is the value of the Entry after the edit. If it's empty or an integer, allow the edit.
        return P == "" or P.isdigit()

    def set_v_star_interval(self):
        data_neg45, data_pos45 = self.calibration_data[self.selected_chan.get()][:2]
        interval = (int(self.v_star_min.get()), int(self.v_star_max.get()))
        V_star = get_V_star(data_neg45, data_pos45, interval)
        if V_star is not None:
            self.v_star.set(str(V_star))

    def set_v_star_menu(self):
        GUI.clean(self.v_star_frame)
        min_entry = tk.Entry(self.v_star_frame, textvariable=self.v_star_min, width=10, validate="key", validatecommand=(self.vcmd, '%P'))
        max_entry = tk.Entry(self.v_star_frame, textvariable=self.v_star_max, width=10, validate="key", validatecommand=(self.vcmd, '%P'))
        v_star_entry = tk.Entry(self.v_star_frame, textvariable=self.v_star, width=10, state='readonly')
        min_label = tk.Label(self.v_star_frame, text="Select Min :", **self.label_style, anchor='e')
        max_label = tk.Label(self.v_star_frame, text="Select Max :", **self.label_style, anchor='e')
        v_star_label = tk.Label(self.v_star_frame, text="V* : ", **self.label_style, anchor='e')
        button_plot_v_star = tk.Button(self.v_star_frame, text="Plot V*", command=self.plot_calibration_data, bg='white')
        button_set_intervals = tk.Button(self.v_star_frame, text="Set Interval", command=self.set_v_star_interval, bg='white')
        min_entry.grid(column=1, row=0, sticky='nsew')
        max_entry.grid(column=1, row=1, sticky='nsew')
        v_star_entry.grid(column=1, row=3, sticky='nsew')
        min_label.grid(column=0, row=0, sticky='nsew', padx=5, pady=(5, 0))
        max_label.grid(column=0, row=1, sticky='nsew', padx=5, pady=5)
        v_star_label.grid(column=0, row=3, sticky='nsew', padx=5, pady=5)
        button_plot_v_star.grid(column=0, row=4, columnspan=2, sticky='nsew')
        button_set_intervals.grid(column=0, row=2, columnspan=2, sticky='nsew')
    
    def set_v_star_menu_and_plot_calibration_data(self, event):
        self.set_v_star_menu()
        self.set_v_star_interval()
        self.plot_calibration_data()
            

    def set_data_with_selected_files(self):
        selected_files = self.file_listbox.curselection()
        if selected_files != ():
            self.data = get_data2([self.paths[self.file_listbox.get(file_index)] for file_index in selected_files], self.config_dir, self.shift.get(), self.bg_noise.get(), self.e_noise.get(), self.deadtime.get())
        else:
            self.data = {}

    def load_data(self):
        print('0')
        for i in range(2):
            GUI.clean(self.chart_frames[i])
        self.set_data_with_selected_files()
        self.set_chan_listbox()
    
    def on_select(self, event):
        self.load_data()

                
    def configure_grid(self):
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
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
        self.tabs[1].grid_rowconfigure(1, weight=0)
        self.tabs[1].grid_rowconfigure(2, weight=0)
        self.tabs[1].grid_rowconfigure(3, weight=1)
        self.tabs[1].grid_columnconfigure(0, weight=1)
        self.tabs[1].grid_columnconfigure(1, weight=0) 
        self.licel_selection_frame.grid_columnconfigure(0, weight=1)
        self.channel_selection_frame.grid_columnconfigure(0, weight=1)
        self.v_star_frame.grid_columnconfigure(0, weight=1)
        for title_frame in self.titles_frames:
            title_frame.grid_columnconfigure(0, weight=1)
        self.chan_listbox_frame.grid_rowconfigure(0, weight=1)
        self.chan_listbox_frame.grid_columnconfigure(0, weight=1)
    
    def place_elements(self):
        self.notebook.grid(row=0, column=1, rowspan = 4, sticky='nsew')
        self.chart_frames[0].grid(column=0, row=1, sticky='nsew')
        self.chart_frames[1].grid(column=0, row=1, rowspan=3, sticky='nsew')
        for i in range(2):
            self.titles_frames[i].grid(row=0, column=0, sticky='new')
            self.titles_labels[i].grid(sticky='nsew', padx=5, pady=5)
        self.chan_listbox_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.licel_selection_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.channel_selection_frame.grid(row=2, column=1, sticky='nsew')
        self.v_star_frame.grid(row=3, column=1, sticky='nsew')
        self.file_list_frame.grid(row=2, column=0, sticky='nsew')
        self.file_listbox.pack(fill='both', expand=True)
        self.selectall_button.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.unselectall_button.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        
    def configure_menubar(self):
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        ##########################
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Exit", command=self.root.destroy)


        self.menubar.add_cascade(label="Config", menu=self.config_menu)
        ##########################
        self.config_menu.add_command(label="Set config directory", command=self.set_config_directory)
        self.config_menu.add_command(label = "Select all filters", command=self.select_all_filters)
        self.config_menu.add_command(label = "Unselect all filters", command=self.unselect_all_filters)
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
        self.selection_vars = []
        self.main_xlim = 5000
        self.calib_xlim = 5000
        self.num_std = 3
        self.default_channels = []
        
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
        self.v_star_min = tk.StringVar(value="1000")
        self.v_star_max = tk.StringVar(value="3000")
        self.v_star = tk.StringVar()

        self.notebook = ttk.Notebook(self.root)
        self.tabs = (ttk.Frame(self.notebook), ttk.Frame(self.notebook))
        self.notebook.add(self.tabs[0], text='Lidar Profiles')
        self.notebook.add(self.tabs[1], text='Calibration Depolarization')
        
        self.menubar = tk.Menu(self.root)
        self.chart_frames = tuple([tk.Frame(tab, bg='#B8614E') for tab in self.tabs])
        self.file_list_frame = tk.Frame(self.root, bg='#B8614E')
        self.file_listbox = tk.Listbox(self.file_list_frame, selectmode=tk.SINGLE, exportselection=False) #or selectmode=tk.MULTIPLE
        self.chan_listbox_frame = tk.Frame(self.tabs[0], bg='#B8614E')
        self.chan_listbox = tk.Listbox(self.chan_listbox_frame, selectmode=tk.MULTIPLE, exportselection=False)
        self.selectall_button = tk.Button(self.root, text="Select All", command=self.select_all, bg='white')
        self.unselectall_button = tk.Button(self.root, text="Unselect All", command=self.unselect_all, bg='white')
        
        self.titles_frames = tuple([tk.Frame(tab, bg='#B8614E') for tab in self.tabs])
        self.titles_labels = (tk.Label(self.titles_frames[0], text="Data from files", **self.label_style, anchor='center'),
                             tk.Label(self.titles_frames[1], text="Calibration", **self.label_style, anchor='center'))
        
        self.licel_selection_frame = tk.Frame(self.tabs[1], bg='#B8614E')
        self.channel_selection_frame = tk.Frame(self.tabs[1], bg='#B8614E')
        self.v_star_frame = tk.Frame(self.tabs[1], bg='#B8614E')
        
        self.vcmd = self.root.register(GUI.validate)

        self.file_menu = tk.Menu(self.menubar)
        self.config_menu = tk.Menu(self.menubar)


        self.configure_grid()
        self.configure_root()
        self.place_elements()
        self.configure_menubar()
        self.file_listbox.bind('<<ListboxSelect>>', self.on_select)
        self.chan_listbox.bind('<<ListboxSelect>>', self.plot_main_data)
        
        self.root.mainloop()
    
        
gui = GUI()