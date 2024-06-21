from main import *
import pytest
from numpy import nan

config = get_config(r'./austral-data-sample/instruments/lilas/private/config/lidar', *([False] * 4))
config_dir=r'./austral-data-sample/instruments/lilas/private/config/lidar'
directory = r'./austral-data-sample/instruments/lilas/private/measurement/2023/05/28/'
filenames = [directory + file_name for file_name in ['l2352800.005799', 'l2352800.015859', 'l2352800.025916', 'l2352800.035973']]

def arrays_are_equal(a, b):
    a, b = np.array(a), np.array(b)
    return np.array_equal(np.isnan(a), np.isnan(b)) and np.array_equal(a[~np.isnan(a)], b[~np.isnan(b)])

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

def test_get_data_channel():
    gui = GUI()
    x = [0.0, 7.5, 15.0, 22.5, 30.0, 37.5, 45.0, 52.5, 60.0, 67.5]
    gui.data = {'355.p_PC': (x, [nan, 6629.143610087687, 24045.073478274382, 50584.3163825378, 85152.34296455736, 127712.71516168321, 183172.39912403014, 247537.54123870237, 328100.4641710749, 436172.8225525985]), 
                '532.p_AN': (x, [nan, 31.41683096314172, 178.93362920047088, 291.1104698020375, 555.0300163804803, 854.664429396303, 1250.3570048818103, 1728.3364680852949, 2287.699077314089, 3136.7493818906432]), 
                '532.s_PC': (x, [nan, 7047.089226594679, 25799.451957442358, 56338.89622675108, 106760.11672721925, 178901.92896022982, 270153.211173953, 382776.3527900255, 525404.9046152444, 734701.9282594664]), 
                '1064.s_AN': (x, [nan, 1104.2920457294047, 3920.0505358479586, 7348.229894247459, 11709.27162249289, 17995.708115393034, 25734.921724595017, 37090.60561352666, 54452.104889181355, 81389.44301660488])}
    gui.calibration_data = {'355PC': ((x, [nan, 13.52804226236677, 20.1376226817196, 29.261358718347832, 29.926095714395395, 29.071918735678906, 25.284197880056777, 20.391809402847173, 15.904435552870815, 12.67851111626257]),
                                      (x, [nan, 8.618018801865329, 16.814098170499296, 24.55907728100035, 27.553568920389946, 26.632198903579116, 23.449800662025993, 19.370503355938396, 14.951415108864364, 12.268668947329987]),
                                      (x, [nan, 1.354364582011431, 1.2687508932940177, 1.1474620482002995, 1.057923454476874, 0.9395524762177226, 0.8375438328594067, 0.7810237322549259, 0.7541869194481113, 0.7443846164504696])), 
                            '532PC': ((x, [nan, 1.433587950200549, 3.2649711958324565, 3.583693585976942, 3.554897611977041, 3.775924037060903, 3.9315395943594327, 4.215902103540052, 4.222147740704458, 3.9313457520486175]), 
                                      (x, [nan, 0.4179321321076305, 0.1510736122463078, 0.09692401277760998, 0.07221820413041087, 0.07171777829109006, 0.07817084213862786, 0.08677506416779981, 0.10689998058617778, 0.12523129495713417]),
                                      (x, [nan, 1.433587950200549, 3.2649711958324565, 3.583693585976942, 3.554897611977041, 3.775924037060903, 3.9315395943594327, 4.215902103540052, 4.222147740704458, 3.9313457520486175]))}
    gui.selected_chan.set('532PC')
    for chan in gui.data:
        gui.chan_listbox.insert(tk.END, chan)
    gui.chan_listbox.select_set(1, 2)
    expected_output0 = [(x, [nan, 31.41683096314172, 178.93362920047088, 291.1104698020375, 555.0300163804803, 854.664429396303, 1250.3570048818103, 1728.3364680852949, 2287.699077314089, 3136.7493818906432]), 
                        (x, [nan, 7047.089226594679, 25799.451957442358, 56338.89622675108, 106760.11672721925, 178901.92896022982, 270153.211173953, 382776.3527900255, 525404.9046152444, 734701.9282594664])]
    expected_output1 = ((x, [nan, 1.433587950200549, 3.2649711958324565, 3.583693585976942, 3.554897611977041, 3.775924037060903, 3.9315395943594327, 4.215902103540052, 4.222147740704458, 3.9313457520486175]), 
                        (x, [nan, 0.4179321321076305, 0.1510736122463078, 0.09692401277760998, 0.07221820413041087, 0.07171777829109006, 0.07817084213862786, 0.08677506416779981, 0.10689998058617778, 0.12523129495713417]), 
                        (x, [nan, 1.433587950200549, 3.2649711958324565, 3.583693585976942, 3.554897611977041, 3.775924037060903, 3.9315395943594327, 4.215902103540052, 4.222147740704458, 3.9313457520486175]))
    expected_output = (expected_output0, expected_output1)
    for i in range(2):
        actual_output = gui.get_data_channel(i)
        assert actual_output == expected_output[i]

def test_get_selected_licels():
    gui = GUI()
    for i in range(5):
        gui.file_listbox.insert(tk.END, str(i))
        gui.paths[str(i)] = 'value ' + str(i)
    gui.file_listbox.select_set(1, 3)
    expected_output = ['value ' + str(i) for i in range(1, 4)]
    actual_output = gui.get_selected_licels()
    assert actual_output == expected_output

def test_set_chan_listbox():
    gui = GUI()
    gui.data = {'355.p_PC': None,
                 '355.s_PC': None,
                 '532.p_AN': None, 
                 '532.s_PC': None, 
                 '1064.s_AN': None}
    gui.default_channels = ['355.p_PC', '532.p_AN', '1064.s_AN', 'odd one out']
    try:
        gui.set_chan_listbox()
    except TypeError:
        pass
    assert len(gui.chan_listbox.get(0, tk.END)) == 5
    assert len(gui.chan_listbox.curselection()) == 3
    assert gui.chan_listbox.grid_info()
    assert gui.selectall_button.grid_info()
    assert gui.unselectall_button.grid_info()
    assert gui.default_button.grid_info()


def test_validate():
    assert GUI.validate('')
    assert GUI.validate('5446816')
    assert not GUI.validate('5446816.5')
    assert not GUI.validate('-5446816')
    assert not GUI.validate('abcd')

def test_set_v_star_interval():
    gui = GUI()
    x = [i*500+2500 for i in range(7)]
    gui.calibration_data = {'355PC': ((x, [i for i in range(7)]), (x, [i*0.8 for i in range(7)]), (None, None)),
                            '1064A': ((x, [i*0.7 for i in range(7)]), (x, [i*0.9 for i in range(7)]), (None, None))}
    gui.selected_chan.set('355PC')
    try:
        gui.set_v_star_interval()
    except TypeError:
        pass
    expected_v_star = '0.4472135954999579'
    actual_v_star = gui.v_star.get()
    assert actual_v_star == expected_v_star

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

def test_set_data_with_selected_files():
    gui = GUI()
    for file_path in filenames:
        file_name = file_path.split('/')[-1]
        gui.paths[file_name] = file_path
        gui.file_listbox.insert(tk.END, file_path.split('/')[-1])
    gui.file_listbox.select_set(0, tk.END)
    gui.set_data_with_selected_files(False)
    expected_data = [nan, 4.678408131673821, 18.713632526695285, -0.030861447352592785, 74.85453010678114, 93.5450945967458, 100.99144491503156, 183.34838540962176, 359.36838273302374, 378.9510586655796, 467.8408131673822, 226.14301056101039, 403.96577966012626, 1265.6295535300737, 4409.300582805835, 4005.7474090967476, 5518.7383889636785, 12207.357967871427, 10942.138054648343, 16268.391145289654]
    expected_keys = dict.fromkeys(['355.p_AN', '355.p_PC', '355.s_AN', '355.s_PC', '371.o_PC', '387.o_AN', '387.o_PC', '408.p_AN', '408.p_PC', '408.s_AN', '408.s_PC', '460.p_PC', '460.s_AN', '460.s_PC', '530.o_AN', '530.o_PC', '532.p_AN', '532.p_PC', '532.s_AN', '532.s_PC', '1064.p_AN', '1064.s_AN']).keys()
    assert expected_keys == gui.data.keys()
    assert arrays_are_equal(expected_data, gui.data['371.o_PC'][1][:20])

def test_place_elements():
    gui = GUI()
    Widgets = (
        list(gui.chart_frames) + list(gui.scale_entries_frames) + list(gui.titles_frames) + list(gui.titles_labels) +
        [w for widgets in gui.scale_labels for w in widgets] + 
        [w for widgets in gui.scale_entries for w in widgets] + 
        list(gui.scale_buttons) + list(gui.scale_log_buttons) + 
        [gui.notebook, gui.chan_listbox_frame, gui.licel_selection_frame, gui.channel_selection_frame, gui.v_star_frame]
    )
    for widget in Widgets:
        assert widget.grid_info()
    

"""
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
    test_get_data_channel()
    test_get_selected_licels()
    test_set_chan_listbox()
    test_validate()
    test_set_v_star_interval()
    test_set_data_with_selected_files()
    test_place_elements()
test()
"""