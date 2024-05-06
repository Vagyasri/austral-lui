from pypr2.Pr2ObjectFactory import Pr2ObjectFactory
from pypr2.Pr2Object import Pr2Object
def get_config(config_dir, shift, bg_noise, e_noise, deadtime):
    config = Pr2ObjectFactory.get_default_config()
    config.apply_enoise_correction_if_available = e_noise
    config.enable_shift = shift
    config.enable_background_correction = bg_noise
    config.enable_dead_time_correction = deadtime
    config.altitude_correction_file = config_dir + '/correction_altitude.txt'
    config.calibration_file = config_dir + '/polarization_coefficient.txt'
    config.inclination_file = config_dir + '/lidar_angle.txt'
    config.dead_time_file = config_dir + '/Td_lidar.txt'
    return config
directory = r'\\wsl.localhost\Ubuntu-22.04\home\neuts\project\austral-data-sample\instruments\lilas\private\measurement\2023\05\28'
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

