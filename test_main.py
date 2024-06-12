from main import *
import pytest

config = get_config(r'./austral-data-sample/instruments/lilas/private/config/lidar', *([False] * 4))
config_dir=r'./austral-data-sample/instruments/lilas/private/config/lidar'
directory = r'./austral-data-sample/instruments/lilas/private/measurement/2023/05/28/'
filenames = [directory + file_name for file_name in ['l2352800.005799', 'l2352800.015859', 'l2352800.025916', 'l2352800.035973']]

def test_select_all_chan():
    gui = GUI()
    for i in range(65, 91):
        gui.chan_listbox.insert(tk.END, chr(i))
    try:
        gui.select_all_chan()
    except KeyError:
        pass
    curselection = gui.chan_listbox.curselection()
    assert len(curselection) == gui.chan_listbox.size()

def test_unselect_all_chan():
    gui = GUI()
    for i in range(65, 91):
        gui.chan_listbox.insert(tk.END, chr(i))
    gui.chan_listbox.select_set(5, 20)
    try:
        gui.unselect_all_chan()
    except KeyError:
        pass
    assert len(gui.chan_listbox.curselection()) == 0

def test_select_all_files():
    gui = GUI()
    for i in range(65, 91):
        gui.file_listbox.insert(tk.END, chr(i))
    gui.select_all_files()
    curselection = gui.file_listbox.curselection()
    assert len(curselection) == gui.file_listbox.size()

def test_unselect_all_files():
    gui = GUI()
    for i in range(65, 91):
        gui.file_listbox.insert(tk.END, chr(i))
    gui.file_listbox.select_set(5, 20)
    gui.unselect_all_files()
    assert len(gui.chan_listbox.curselection()) == 0

def test_set_default_channels():
    gui = GUI()
    for i in range(65, 91):
        gui.chan_listbox.insert(tk.END, chr(i))
    gui.chan_listbox.select_set(0, 3)
    gui.set_default_channels()
    assert gui.default_channels == ['A', 'B', 'C', 'D']

def test_select_all_filters():
    gui = GUI()
    try:
        gui.select_all_filters()
    except IndexError:
        pass
    filters = [gui.e_noise, gui.bg_noise, gui.deadtime, gui.shift]
    for filter_ in filters:
        assert filter_.get() == 1

def test_unselect_all_filters():
    gui = GUI()
    try:
        gui.unselect_all_filters()
    except IndexError:
        pass
    filters = [gui.e_noise, gui.bg_noise, gui.deadtime, gui.shift]
    for filter_ in filters:
        assert filter_.get() == 0

def test_clean():
    root = tk.Tk()
    frame = tk.Frame(root)
    labels = []
    for i in range(3):
        labels.append(tk.Label(frame, text=str('label')))
    GUI.clean(frame)
    assert len(frame.winfo_children()) == 0

def test_toggle_selection():
    gui = GUI()
    Widgets = (gui.all_button, gui.avg_button, gui.select_all_files_button, gui.unselect_all_files_button)
    gui.multiple_selection_var.set(1)
    gui.toggle_selection()
    for widget in Widgets:
        assert widget.grid_info()
        assert gui.file_listbox.cget("selectmode") == 'multiple'
    gui.multiple_selection_var.set(0)
    gui.toggle_selection()
    for widget in Widgets:
        assert not widget.grid_info()
        assert gui.file_listbox.cget("selectmode") == 'single'

def test_delete_selected_files():
        gui = GUI()
        for i in range(10):
            gui.file_listbox.insert(tk.END, str(i))
            gui.paths[str(i)] = 'value ' + str(i)
        gui.file_listbox.select_set(3, 7)
        gui.delete_selected_files()
        rest = ('0', '1', '2', '8', '9')
        assert gui.file_listbox.get(0, tk.END) == rest
        assert gui.paths.keys() == dict.fromkeys(rest).keys()

def test_select():
    root = tk.Tk()
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
    for i in range(65, 91):
        listbox.insert(tk.END, chr(i))
    listbox.select_set(5)
    listbox.select_set(12)
    GUI.select(listbox)
    assert len(listbox.curselection()) == 8

def test():
    test_select_all_chan()
    test_unselect_all_chan()
    test_select_all_files()
    test_unselect_all_files()
    test_set_default_channels()
    test_select_all_filters()
    test_unselect_all_filters()
    test_clean()
    test_toggle_selection()
    test_delete_selected_files()
    test_select()
test()
