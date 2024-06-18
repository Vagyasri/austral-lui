import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from licel_treatment import *
import numpy as np
from pypr2.Pr2Object import Pr2Object


class GUI:
    
    def set_config_directory(self):
        print(self.config_dir)
        self.config_dir = './austral-data-sample/instruments/lilas/private/config/lidar'
        print(self.config_dir)
        self.config_dir = tk.filedialog.askdirectory(initialdir=self.config_dir)
#r'./au stral-data-sample/instruments/lilas/private/measurement/2023/05/28')

    def open_file(self):
        file_paths = tk.filedialog.askopenfilenames(initialdir=self.initial_dir)
        for file_path in file_paths:
            file_name = file_path.split('/')[-1]
            if file_name not in self.paths:
                self.paths[file_name] = file_path
                self.file_listbox.insert(tk.END, file_path.split('/')[-1])
        if file_paths:
            self.set_licel_pull_down_menu()
        
    def select_all_chan(self):
        self.chan_listbox.select_set(0, tk.END)
        self.plot_main_data()

    def unselect_all_chan(self):
        self.chan_listbox.select_clear(0, tk.END)
        self.plot_main_data()

    def select_all_files(self):
        self.file_listbox.select_set(0, tk.END)

    def unselect_all_files(self):
        self.file_listbox.select_clear(0, tk.END)

    def set_default_channels(self):
        self.default_channels = []
        selected_channels = self.chan_listbox.curselection()
        for channel_index in selected_channels:
            self.default_channels.append(self.chan_listbox.get(channel_index))

    def on_filter(self):
        self.load_data()
        if self.selected_chan.get():
            self.set_channel_pull_down_menu()
        


    def select_all_filters(self):
        # Set all variables to True
        self.e_noise.set(1)
        self.shift.set(1)
        self.bg_noise.set(1)
        self.deadtime.set(1)
        self.on_filter()
    
    def unselect_all_filters(self):
        # Set all variables to True
        self.e_noise.set(0)
        self.shift.set(0)
        self.bg_noise.set(0)
        self.deadtime.set(0)
        self.on_filter()

    @staticmethod
    def clean(object_):
        for widget in object_.winfo_children():
            widget.destroy()

    def toggle_selection(self):
        if self.multiple_selection_var.get():
            self.all_button.grid(row=0, column=0, sticky='nsew')
            self.avg_button.grid(row=1, column=0, sticky='nsew')
            self.select_all_files_button.grid(row=2, column=0, sticky='nsew')
            self.unselect_all_files_button.grid(row=3, column=0, sticky='nsew')
            self.file_listbox.config(selectmode=tk.MULTIPLE)
            self.file_listbox.unbind('<<ListboxSelect>>')
        else:
            self.avg_button.grid_remove()
            self.all_button.grid_remove()
            self.select_all_files_button.grid_remove()
            self.unselect_all_files_button.grid_remove()
            self.file_listbox.select_clear(0, tk.END)
            self.file_listbox.config(selectmode=tk.SINGLE)
            self.file_listbox.bind('<<ListboxSelect>>', self.on_select)

    def delete_selected_files(self):
        for i in self.file_listbox.curselection()[::-1]:
            self.paths.pop(self.file_listbox.get(i))
            self.file_listbox.delete(i)
            
    @staticmethod
    def select(listbox):
        curselection = listbox.curselection()
        if len(curselection) == 2:
            a, b = curselection
            listbox.select_set(a, b)
    """
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
    """
    def get_new_fig(self):
        fig = plt.Figure()
        fig.tight_layout()
        ax = fig.add_subplot(111)
        return fig, ax
    
    def configure_ax(self, ax, xlab, ylab, tit, i, data_channel, there_are_data=True):
        if there_are_data:
            ax.set_yscale(self.curve_type[i])
        ylim = find_ylim(data_channel, self.xlim[i], self.num_std, i)
        if self.curve_type[i] == 'log':
            ylim = (max(ylim[0], ylim[1]*self.y_log_low_lim), ylim[1])
        ax.set_ylim(*ylim)
        ax.set_xlabel(fontdict=self.plot_label_font, xlabel=xlab)   
        ax.set_ylabel(fontdict=self.plot_label_font, ylabel=ylab)
        ax.set_title(fontdict=self.plot_label_font, label=tit)  
        ax.grid(True)
        if there_are_data:
            ax.legend()
            #ax.set_xlim(-1000, 5000)
            self.axes[i] = ax
        return ax
    
    def get_main_figure(self):
        selected_channels = self.chan_listbox.curselection()
        fig, ax = self.get_new_fig()
        ax.set_xlim(*self.xlim[0])
        for channel_index in selected_channels:
            channel = self.chan_listbox.get(channel_index)
            x, y = self.data[channel]
            ax.plot(x, y, label=channel)
        there_are_data = selected_channels != ()
        ax = self.configure_ax(ax, "Distance (m)", "Lidar Signal (mV)", "Lidar Profile", 0, self.get_data_channel(0), there_are_data)
        return fig
    
    def get_data_channel(self, i):
        return self.calibration_data[self.selected_chan.get()] if i else [self.data[self.chan_listbox.get(channel_index)] for channel_index in self.chan_listbox.curselection()]

    def set_scale(self, event=None, i=1):
        a, b = self.scale_entries[i][0].get(), self.scale_entries[i][1].get()
        if a!= b and a!= '' and b!= '' and self.axes[i] is not None:
            xlim = tuple(sorted([float(a), float(b)]))
            data_channel = self.get_data_channel(i)
            self.axes[i].set_xlim(*xlim)
            ylim = find_ylim(data_channel, xlim, self.num_std, i)
            if self.curve_type[i] == 'log':
                ylim = (max(ylim[0], ylim[1]*self.y_log_low_lim), ylim[1])
            self.axes[i].set_ylim(*ylim)
            self.axes[i].figure.canvas.draw()

    def toggle_log(self, i):
        if self.axes[i]:
            ylim = find_ylim(self.get_data_channel(i), self.axes[i].get_xlim(), self.num_std, i)
            if self.curve_type[i] == 'log':
                self.curve_type[i] = 'linear'
            else:
                self.curve_type[i] = 'log'
                ylim = (max(ylim[0], ylim[1]*self.y_log_low_lim), ylim[1])
            self.axes[i].set_yscale(self.curve_type[i])
            self.axes[i].set_ylim(*ylim)
            self.axes[i].figure.canvas.draw()

    def get_ax_with_calibration_curves(self, ax, x1, y1, x2, y2):
        if self.smooth:
            y1, y2 = smooth(y1, self.smooth_lvl), smooth(y2, self.smooth_lvl)
        if not self.unplot_var.get():
            curve1, = ax.plot(x1, y1, label='+45')
            curve2, = ax.plot(x2, y2, label='-45')
            self.calib_curves = [curve1, curve2]
            x, y = get_v_star_points(x1, y1, x2, y2)
            if y:
                curve, = ax.plot(x, y, label='V* (-)')
                self.calib_curves.append(curve)
        return ax

    def get_ax_with_verification_curves(self, ax, calibration_data_channel):
        v_star = self.v_star.get()
        if v_star:
            v_star = float(v_star)
            ax.axhline(y=v_star, linestyle='--', label='V* in elected interval')
            if len(calibration_data_channel) > 2:
                ax.axhline(y=self.c_star, linestyle='--', label='c*', color='pink')
                x3, y3 = calibration_data_channel[2]
                y3 = [y * v_star for y in y3]
                if self.smooth:
                    y3 = smooth(y3, self.smooth_lvl)
                ax.plot(x3, y3, label='corrected 0')
        return ax
    
    def get_calibration_figure(self):
        fig, ax = self.get_new_fig()
        calibration_data_channel = self.get_data_channel(1)
        x1, y1 = calibration_data_channel[0]
        x2, y2 = calibration_data_channel[1]
        ax = self.get_ax_with_calibration_curves(ax, x1, y1, x2, y2)
        ax = self.get_ax_with_verification_curves(ax, calibration_data_channel)            
        ax.set_xlim(*self.xlim[1])
        ax = self.configure_ax(ax, "Distance (m)", "δ* (-)", "Calibration", 1, calibration_data_channel)
        return fig
    
    def get_selected_licels(self):
        return [self.paths[self.file_listbox.get(i)] for i in self.file_listbox.curselection()]

    def create_canvas_with_chart(self, fig, i):
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frames[i])
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frames[i])
        toolbar.update()

    def plot_data(self, i):
        GUI.clean(self.chart_frames[i])
        self.axes[i] = None
        fig = (self.get_main_figure, self.get_calibration_figure)[i]()
        self.create_canvas_with_chart(fig, i)

    def plot_main_data(self, event=None):
        self.plot_data(0)

    def plot_calibration_data(self):
        self.plot_data(1)

    def set_chan_listbox(self):
        self.chan_listbox.delete(0, tk.END)
        for channel in self.data:
            self.chan_listbox.insert(tk.END, channel)
        self.chan_listbox.grid(sticky='nsew')
        self.selectall_button.grid(row=1, column=1, sticky='nsew')
        self.unselectall_button.grid(row=2, column=1, sticky='nsew')
        self.default_button.grid(row=4, column=1, sticky='nsew')
        items = self.chan_listbox.get(0, tk.END)
        for channel in self.default_channels:
            try:
                index = items.index(channel)
                self.chan_listbox.selection_set(index)
            except ValueError:
                pass
        self.plot_main_data()
    
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
        set_button = tk.Button(self.licel_selection_frame, text="Set", command=self.set_channel_pull_down_menu, bg='white')
        set_button.grid(sticky='ew')

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
            
    def unplot_45(self):
        if self.unplot_var.get():
            for calib_curve in self.calib_curves:
                calib_curve.remove()
            self.axes[1].legend()
            self.axes[1].figure.canvas.draw()
        else:
            self.plot_calibration_data()
                

    @staticmethod
    def validate(P):
        # P is the value of the Entry after the edit. If it's empty or an integer, allow the edit.
        return P == "" or P.isdigit()

    def set_v_star_interval(self):
        data_neg45, data_pos45 = self.calibration_data[self.selected_chan.get()][:2]
        interval = (int(self.v_star_min.get()), int(self.v_star_max.get()))
        V_star = get_V_star_constant(data_neg45, data_pos45, interval)
        if V_star is not None:
            self.v_star.set(str(V_star))
        self.plot_calibration_data()

    def set_v_star_menu(self):
        GUI.clean(self.v_star_frame)
        min_entry = tk.Entry(self.v_star_frame, textvariable=self.v_star_min, width=10, validate="key", validatecommand=(self.vcmd, '%P'))
        max_entry = tk.Entry(self.v_star_frame, textvariable=self.v_star_max, width=10, validate="key", validatecommand=(self.vcmd, '%P'))
        v_star_entry = tk.Entry(self.v_star_frame, textvariable=self.v_star, width=10, state='readonly')
        min_label = tk.Label(self.v_star_frame, text="Select Min :", **self.label_style, anchor='e')
        max_label = tk.Label(self.v_star_frame, text="Select Max :", **self.label_style, anchor='e')
        v_star_label = tk.Label(self.v_star_frame, text="V* : ", **self.label_style, anchor='e')
        checkbutton_unplot_45 = tk.Checkbutton(self.v_star_frame, text="Unplot", variable=self.unplot_var, command=self.unplot_45, bg='white')
        button_set_interval = tk.Button(self.v_star_frame, text="Set Interval", command=self.set_v_star_interval, bg='white')
        min_entry.grid(column=1, row=0, sticky='nsew')
        max_entry.grid(column=1, row=1, sticky='nsew')
        v_star_entry.grid(column=1, row=3, sticky='nsew')
        min_label.grid(column=0, row=0, sticky='nsew', padx=5, pady=(5, 0))
        max_label.grid(column=0, row=1, sticky='nsew', padx=5, pady=5)
        v_star_label.grid(column=0, row=3, sticky='nsew', padx=5, pady=5)
        checkbutton_unplot_45.grid(column=0, row=4, columnspan=2, sticky='nsew')
        button_set_interval.grid(column=0, row=2, columnspan=2, sticky='nsew')
    
    def set_v_star_menu_and_plot_calibration_data(self, event):
        self.set_v_star_menu()
        self.set_v_star_interval()
        self.plot_calibration_data()
            

    def set_data_with_selected_files(self, average):
        selected_files_indexes = self.file_listbox.curselection()
        selected_files= []
        for file_index in selected_files_indexes:
            file_path = self.paths[self.file_listbox.get(file_index)]
            if is_a_supported_file(file_path):
                selected_files.append(file_path)
            else:
                print(f'File {file_path} is not supported')
        self.data = get_data(selected_files, self.config_dir, self.shift.get(), self.bg_noise.get(), self.e_noise.get(), self.deadtime.get(), self.r2.get(), average) if selected_files != [] else {}

    def load_data(self, average=False):
        GUI.clean(self.chart_frames[0])
        self.axes = [None, None]
        self.set_data_with_selected_files(average)
        self.set_chan_listbox()
    
    def on_select(self, event):
        self.load_data()

    @staticmethod
    def rowconfigure(tk_obj, config):
        for i, weight in enumerate(config):
            tk_obj.grid_rowconfigure(i, weight=weight)

    @staticmethod
    def columnconfigure(tk_obj, config):
        for i, weight in enumerate(config):
            tk_obj.grid_columnconfigure(i, weight=weight)
                
    def configure_grid(self):
        GUI.rowconfigure(self.root, (0, 1, 0, 0))
        GUI.columnconfigure(self.root, (0, 1))
        GUI.rowconfigure(self.tabs[0], (0, 0, 0, 1, 0))
        GUI.columnconfigure(self.tabs[0], (1, 0))
        GUI.rowconfigure(self.tabs[1], (0, 0, 0, 1, 0))
        GUI.columnconfigure(self.tabs[1], (1, 0))
        self.licel_selection_frame.grid_columnconfigure(0, weight=1)
        self.channel_selection_frame.grid_columnconfigure(0, weight=1)
        for title_frame in self.titles_frames:
            title_frame.grid_columnconfigure(0, weight=1)
        self.chan_listbox_frame.grid_rowconfigure(0, weight=1)
        self.chan_listbox_frame.grid_columnconfigure(0, weight=1)
        for i in range(2):
            for j in range(6):
                self.scale_entries_frames[i].grid_columnconfigure(j, weight=1)
        self.multiple_selection_frame.grid_columnconfigure(0, weight=1)
        self.multiple_selection_frame.grid_rowconfigure(0, weight=1)
    
    def place_elements(self):
        self.notebook.grid(row=0, rowspan=4, column=1, sticky='nsew')
        self.chart_frames[0].grid(column=0, row=1, rowspan=3, sticky='nsew')
        self.chart_frames[1].grid(column=0, row=1, rowspan=3, sticky='nsew')
        self.scale_entries_frames[0].grid(column=0, row=4, sticky='nsew')
        self.scale_entries_frames[1].grid(column=0, row=4, sticky='nsew')
        for i in range(2):
            self.titles_frames[i].grid(row=0, column=0,columnspan=2, sticky='new')
            self.titles_labels[i].grid(sticky='nsew', padx=5, pady=5)
            for j in range(2):
                self.scale_labels[i][j].grid(row=0, column=2*j, sticky='nsew', padx=5, pady=5)
                self.scale_entries[i][j].grid(row=0, column=2*j+1, sticky='nsew')
            self.scale_buttons[i].grid(row=0, column=4, sticky='nsew')
            self.scale_log_buttons[i].grid(row=0, column=5, sticky='nsew')
        self.chan_listbox_frame.grid(row=3, column=1, sticky='nsew')
        self.licel_selection_frame.grid(row=1, column=1, sticky='nsew')
        self.channel_selection_frame.grid(row=2, column=1, sticky='nsew')
        self.v_star_frame.grid(row=3, rowspan=2, column=1, sticky='nsew')
        
        self.file_listbox.pack(fill='both', expand=True)

        self.multiple_selection_checkbutton.grid(row=0, column=0, sticky='nsew')
        self.file_listbox_frame.grid(row=1, column=0, sticky='nsew')
        self.delete_button.grid(row=2, column=0, sticky='nsew')
        self.multiple_selection_frame.grid(row=3, column=0, sticky='nsew')
        
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
        self.config_menu.add_checkbutton(label="E-Noise", variable=self.e_noise, command=self.on_filter)
        self.config_menu.add_checkbutton(label="Shift", variable=self.shift, command=self.on_filter)
        self.config_menu.add_checkbutton(label="Background Noise", variable=self.bg_noise, command=self.on_filter)
        self.config_menu.add_checkbutton(label="Deadtime", variable=self.deadtime, command=self.on_filter)
        self.config_menu.add_checkbutton(label="PR2", variable=self.r2, command=self.on_filter)
        
    def configure_root(self):
        self.root.title("Austral GUI")
        #self.root.geometry(f'{self.w}x{self.h}')
        self.root.config(bg=self.bg)
        self.root.config(menu=self.menubar)
        #self.root.wm_attributes('-zoomed', True)  # This line maximizes the window.
        #self.root.state('zoomed') same for windows
    
    @staticmethod
    def get_gui_config():
        values = []
        with open('./gui_config.txt', 'r') as file:
            lines = file.readlines()
        default_values = ['./austral-data-sample/instruments/lilas/private/calibration/20210112/200449/',
                           './austral-data-sample/instruments/lilas/private/config/lidar',
                           (0, 5000), (0, 5000), 3, True, 20, 0.004]
        for i, line in enumerate(lines):
            try:
                value = line.split(': ')[1]
                if ',' in value:
                    values.append(tuple(map(int, value.split(', '))))
                elif value.strip().isdigit():
                    values.append(int(value.strip()))
                elif value.strip() == 'Yes' or value.strip() == 'No':
                    values.append(True if value.strip() == 'Yes' else False)
                elif value.strip().replace('.', '', 1).isdigit():
                    values.append(float(value.strip()))
                else:
                    values.append(value.strip())
            except:
                values.append(default_values[i])
        b, a = values.pop(), values.pop()
        values.append((a, b))
        return values

    def __init__(self):
        self.root = tk.Tk()

        self.initial_dir, self.config_dir, self.num_std, self.smooth, self.smooth_lvl, self.c_star, self.xlim = GUI.get_gui_config()
        self.data = {}
        self.calibration_data = {}
        self.paths = {} 
        self.selection_vars = []
        self.y_log_low_lim = 0.0001
        self.axes = [None, None]
        self.default_channels = []
        self.calib_curves = []
    
        
        self.bg = '#de755e'
        self.colour = '#B8614E'
        self.w, self.h = 700, 500
        self.curve_type = ['linear', 'linear'] #linear, log, etc
        self.plot_label_font = {'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 12}
        self.label_style = {'background':self.bg, 'font':('Times New Roman', 12)}
        
        self.bg_noise = tk.IntVar(value=1)
        self.e_noise = tk.IntVar(value=1)
        self.shift = tk.IntVar(value=1)
        self.deadtime = tk.IntVar(value=1)
        self.r2 = tk.IntVar(value=1)
        self.selected_chan = tk.StringVar()
        self.multiple_selection_var = tk.IntVar()
        self.v_star_min = tk.StringVar(value="1000")
        self.v_star_max = tk.StringVar(value="3000")
        self.v_star = tk.StringVar()
        self.unplot_var = tk.IntVar()
        self.vcmd = self.root.register(GUI.validate)
        
        self.notebook = ttk.Notebook(self.root)
        self.tabs = (ttk.Frame(self.notebook), ttk.Frame(self.notebook))
        self.notebook.add(self.tabs[0], text='Lidar Profiles')
        self.notebook.add(self.tabs[1], text='Calibration Depolarization')
        
        
        self.chart_frames = tuple([tk.Frame(tab, bg=self.colour) for tab in self.tabs])
        self.licel_selection_frame = tk.Frame(self.tabs[1], bg=self.colour)
        self.channel_selection_frame = tk.Frame(self.tabs[1], bg=self.colour)
        self.v_star_frame = tk.Frame(self.tabs[1], bg=self.colour)
        self.scale_entries_frames = tuple([tk.Frame(tab, bg=self.colour) for tab in self.tabs])
        self.file_listbox_frame = tk.Frame(self.root, bg=self.colour)
        self.chan_listbox_frame = tk.Frame(self.tabs[0], bg=self.colour)
        self.titles_frames = tuple([tk.Frame(tab, bg=self.colour) for tab in self.tabs])
        self.multiple_selection_frame = tk.Frame(self.root, bg=self.colour)

        self.file_listbox = tk.Listbox(self.file_listbox_frame, width=16, selectmode=tk.SINGLE, exportselection=False) #or selectmode=tk.MULTIPLE
        self.chan_listbox = tk.Listbox(self.chan_listbox_frame, width = 10, selectmode=tk.MULTIPLE, exportselection=False)

        self.multiple_selection_checkbutton = tk.Checkbutton(self.root, text="Multiple Selection", variable=self.multiple_selection_var, command=self.toggle_selection, bg='white')

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_selected_files, bg='white')
        self.selectall_button = tk.Button(self.tabs[0], text="Select All", command=self.select_all_chan, bg='white')
        self.unselectall_button = tk.Button(self.tabs[0], text="Unselect All", command=self.unselect_all_chan, bg='white')
        self.default_button = tk.Button(self.tabs[0], text="Set Default", command=self.set_default_channels, bg='white')
        self.scale_buttons = tuple([tk.Button(self.scale_entries_frames[i], text='Set Scale', command=lambda event=None, x=i: self.set_scale(i=x)) for i in range(2)])
        self.scale_log_buttons = tuple([tk.Button(self.scale_entries_frames[i], text='Log', command=lambda i=i: self.toggle_log(i)) for i in range(2)])
        self.avg_button = tk.Button(self.multiple_selection_frame, text="Average", command=lambda : self.load_data(True), bg='white')
        self.all_button = tk.Button(self.multiple_selection_frame, text="Load singles", command=self.load_data, bg='white')
        self.select_all_files_button = tk.Button(self.multiple_selection_frame, text="Select All", command=self.select_all_files, bg='white')
        self.unselect_all_files_button = tk.Button(self.multiple_selection_frame, text="Unselect All", command=self.unselect_all_files, bg='white')

        self.titles_labels = (tk.Label(self.titles_frames[0], text="Data from files", **self.label_style, anchor='center'),
                              tk.Label(self.titles_frames[1], text="Calibration", **self.label_style, anchor='center'))
        self.scale_labels =  tuple([tuple([tk.Label(self.scale_entries_frames[j], text=('Min :', 'Max :')[i], **self.label_style, anchor='e') for i in range(2)]) for j in range(2)])
        self.scale_entries = tuple([tuple([tk.Entry(self.scale_entries_frames[j], width=8, validate="key", validatecommand=(self.vcmd, '%P')) for i in range(2)]) for j in range(2)])
        
        
        self.menubar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menubar)
        self.config_menu = tk.Menu(self.menubar)


        self.configure_grid()
        self.configure_root()
        self.place_elements()
        self.configure_menubar()
        for i in range(2):
            for j in range(2):
                self.scale_entries[i][j].bind('<Return>', lambda event, x=i: self.set_scale(i=x))
        
        self.file_listbox.bind('<<ListboxSelect>>', self.on_select)
        self.file_listbox.bind('<a>', lambda event: GUI.select(self.file_listbox))
        self.chan_listbox.bind('<<ListboxSelect>>', self.plot_main_data)
        self.chan_listbox.bind('<a>', lambda event: GUI.select(self.chan_listbox))
        
    def run(self):
        self.root.mainloop()
    
if __name__ == '__main__':   
    gui = GUI()
    gui.run()