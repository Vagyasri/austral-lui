from pypr2.Pr2ObjectFactory import Pr2ObjectFactory
from pypr2.Pr2Object import Pr2Object, Pr2ObjectException
import numpy as np
from math import sin, cos
def get_config(config_dir, shift, bg_noise, e_noise, deadtime):
    config = Pr2ObjectFactory.get_default_config()
    #config.BACKGROUND_NOISE_MIN_ALTITUDE = 40000.0
    #config.BACKGROUND_NOISE_MAX_ALTITUDE = 60000.0
    #print(e_noise, bg_noise, shift, deadtime)
    config.apply_enoise_correction_if_available = e_noise
    config.enable_shift = shift
    config.enable_background_correction = bg_noise
    config.enable_dead_time_correction = deadtime
    config.altitude_correction_file = config_dir + '/correction_altitude.txt'
    config.calibration_file = config_dir + '/polarization_coefficient.txt'
    config.inclination_file = config_dir + '/lidar_angle.txt'
    config.dead_time_file = config_dir + '/Td_lidar.txt'
    return config
directory = r'./austral-data-sample/instruments/lilas/private/measurement/2023/05/28/'


def multiply_by_r2(distance, power, r2):
    if r2:
        distance[0] = 1.0e-32
        #power2 = np.zeros(power.shape)
        power2 = power / distance**2
        return distance.tolist(), power2.tolist()
    else:
        return distance.tolist(), power.tolist()

def get_data(filenames = [directory + file_name for file_name in ['l2352800.005799', 'l2352800.015859', 'l2352800.025916', 'l2352800.035973']], 
             config_dir=r'./austral-data-sample/instruments/lilas/private/config/lidar', 
             shift=False, bg_noise=False, e_noise=False, deadtime=False, r2=False, average=False):
    factory = Pr2ObjectFactory(filenames, config=get_config(config_dir, shift, bg_noise, e_noise, deadtime), return_type='dict')
    pr2_objects = factory.get_pr2_objects()
    #print(pr2_objects['532.p_PC'].get_concat_dataframe()[['range', 'power']], pr2_objects['532.p_AN'].get_concat_dataframe()[['range', 'power']])
    data = {}
    for channel in pr2_objects:
        pr2 = pr2_objects[channel]
        if average:
            df = pr2.compute_average_of_power_profiles()
        else:
            df = pr2.get_concat_dataframe()
        distance, power = (df['range'].values, df['power'].values)
        data[channel] = multiply_by_r2(distance, power, r2)
    return data

def decomp(channel):
    wv_len, can = channel.split('.')
    ang, nat = can.split('_')
    return (wv_len, nat), ang

def get_calibration_pairs(data):
    chan_p, chan_s = [], []
    for channel in data:
        ang = decomp(channel)[1]
        if ang == 'p':
            chan_p.append(channel)
        elif ang == 's':
            chan_s.append(channel)
    calibration_pairs = []
    for p in chan_p:
        can, ang = decomp(p)
        wv_len, nat = can
        try:
            s_index = chan_s.index(f'{wv_len}.s_{nat}')
            calibration_pairs.append((p, chan_s[s_index]))
        except ValueError:
            pass
    return calibration_pairs

def get_calibration_data(data):
    return {Pr2Object.get_calibration_header(p): (data[s][0], [data[s][1][i] / data[p][1][i] for i in range(min(len(data[s][0]), len(data[p][0])))]) for p, s in get_calibration_pairs(data)}

def get_polarization_data(paths, config_dir, shift, bg_noise, e_noise, deadtime):
    all_data = []
    for path in paths:
        all_data.append(get_calibration_data(get_data(path, config_dir, shift, bg_noise, e_noise, deadtime)))
    polar_data = {}
    for chan in all_data[0]:
        if chan in all_data[1]:
            polar_data[chan] = [all_data[0][chan], all_data[1][chan]]
            if len(all_data) == 3 and chan in all_data[2]:
                polar_data[chan].append(all_data[2][chan])
    return polar_data

def get_v_star_points(x1, y1, x2, y2):
    return (x1, [np.sqrt(a * b) if a >=0 and b >=0 else np.nan for a, b in zip(y1, y2)]) if x1 == x2 else (None, None)

def average_interval(data, interval):
    X, Y = data
    a, b = interval
    Y_interval = [y for x, y in zip(X, Y) if a <= x <= b]
    average = np.mean(Y_interval) if Y_interval else None
    return average

def get_V_star_constant(data_neg45, data_pos45, interval):
    neg45 = average_interval(data_neg45, interval)
    pos45 = average_interval(data_pos45, interval)
    return None if neg45 is None or pos45 is None else (neg45 * pos45) ** 0.5

def make_data_regular(x, y):
    if len(x) != len(y):
        x.pop()

def find_ylim(data_channel, xlim, num_std, i):
    if data_channel:
        X, Y = [], []
        for j in range((len(data_channel), 2)[i]):
            x, y = data_channel[j]
            make_data_regular(x, y)
            X.extend(x)
            Y.extend(y)
        xlim_min, xlim_max = xlim
        X = np.array(X)
        mask = (xlim_min <= X) & (X <= xlim_max)
        y_range = np.array(Y)[mask]
        y_range = np.where(y_range <= 0, np.nan, y_range)
        mean, std = np.nanmean(y_range), np.nanstd(y_range)
        return mean - num_std*std, mean + num_std*std
    else:
        return 0, 1

def is_a_supported_file(file_name):
    try:
        Pr2Object.find_type_of_file(file_name)
        return True
    except Pr2ObjectException:
        return False
    
def smooth(Y, nb_points=20):
    if Y == []:
        return []
    else:
        Y = np.array(Y)
        nb_points = nb_points // 2 * 2
        indices = np.arange(-nb_points//2, nb_points//2+1)
        Y_smooth = np.array([])
        for i in range(nb_points//2, len(Y) - nb_points//2):
            Y_avg = np.nanmean(Y[i + indices])
            Y_smooth = np.append(Y_smooth, Y_avg)
        Y_smooth = np.concatenate((Y[:nb_points//2], Y_smooth, Y[-nb_points//2:]))
        return Y_smooth.tolist()