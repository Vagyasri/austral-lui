from pypr2.Pr2ObjectFactory import Pr2ObjectFactory
from pypr2.Pr2Object import Pr2Object
import numpy
from math import sin, cos
def get_config(config_dir, shift, bg_noise, e_noise, deadtime):
    config = Pr2ObjectFactory.get_default_config()
    config.BACKGROUND_NOISE_MIN_ALTITUDE = 40000.0
    config.BACKGROUND_NOISE_MAX_ALTITUDE = 60000.0
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
def get_data2(filenames = [directory + file_name for file_name in ['l2352800.005799', 'l2352800.015859', 'l2352800.025916', 'l2352800.035973']], config_dir=r'./austral-data-sample/instruments/lilas/private/config/lidar', shift=False, bg_noise=False, e_noise=False, deadtime=False):

    factory = Pr2ObjectFactory(filenames, config=get_config(config_dir, shift, bg_noise, e_noise, deadtime), return_type='dict')
    pr2_objects = factory.get_pr2_objects()
    #print(pr2_objects['355.p_AN'].get_concat_dataframe().columns)
    data = {}
    for channel in pr2_objects:
        pr2 = pr2_objects[channel]
        df = pr2.get_concat_dataframe()
        distance, power = (df['range'].values, df['power'].values)
        distance[0] = 1.0e-32
        power2 = numpy.zeros(power.shape)
        power2 = power / distance**2
        data[channel] = (distance, power2)
    return data

def get_data(filenames = [directory + file_name for file_name in ['\l2352800.005799', '\l2352800.015859', '\l2352800.025916', '\l2352800.035973']], config_dir=r'\\wsl.localhost\Ubuntu-22.04\home\neuts\project\austral-data-sample\instruments\lilas\private\config\lidar', shift=False, bg_noise=False, e_noise=False, deadtime=False):

    factory = Pr2ObjectFactory(filenames, config=get_config(config_dir, shift, bg_noise, e_noise, deadtime), return_type='dict')
    pr2_objects = factory.get_pr2_objects()
    """
    {channel:(range, power)}
    """
    data = {}
    for channel in pr2_objects:
        pr2 = pr2_objects[channel]
        df = pr2.get_concat_dataframe()
        data[channel] = (df['range'].tolist(), df['power'].tolist())
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
    return {Pr2Object.get_calibration_header(p): (data[s][0], [data[s][1][i] / data[p][1][i] for i in range(len(data[s][0]))]) for p, s in get_calibration_pairs(data)}

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
