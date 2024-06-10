from licel_treatment import *
from main import *
import numpy as np
from numpy import nan

config = get_config(r'./austral-data-sample/instruments/lilas/private/config/lidar', *([False] * 4))
config_dir=r'./austral-data-sample/instruments/lilas/private/config/lidar'
directory = r'./austral-data-sample/instruments/lilas/private/measurement/2023/05/28/'
filenames = [directory + file_name for file_name in ['l2352800.005799', 'l2352800.015859', 'l2352800.025916', 'l2352800.035973']]

def arrays_are_equal(a, b):
    a, b = np.array(a), np.array(b)
    return np.array_equal(np.isnan(a), np.isnan(b)) and np.array_equal(a[~np.isnan(a)], b[~np.isnan(b)])

def test_get_data():
    for i in range(8):
        filters, r2, avg = [bool((i >> j) & 1) for j in range(3)]
        input_ = [filenames, config_dir] + [filters] * 4 + [r2, avg]
        expected_keys = ['355.p_AN', '355.p_PC', '355.s_AN', '355.s_PC', '371.o_PC', '387.o_AN', '387.o_PC', '408.p_AN', '408.p_PC', '408.s_AN', '408.s_PC', '460.p_PC', '460.s_AN', '460.s_PC', '530.o_AN', '530.o_PC', '532.p_AN', '532.p_PC', '532.s_AN', '532.s_PC', '1064.p_AN', '1064.s_AN']
        expected_sample = ([nan, 283.5446194105645, 1134.164752815877, 2551.8604002159373, 4535.890420986175, 7074.547538223643, 10570.02406419559, 19266.644783193497, 25452.196429715168, 29054.56533474852, 35400.33031082157, 41827.45948888747, 49592.519054633965, 57447.915427619846, 66310.57452123231, 76266.45835430182, 86866.2195423228, 98492.19743620245, 112489.95342708916, 129368.71059831095], [nan, 4243.211528249375, 15684.811905437133, 33883.91151545795, 59249.573547776854, 87429.06612364695, 127313.19513217318, 171269.23460791423, 226154.84342048294, 297373.025527756, 392962.76187052455, 523509.1475208035, 701065.0374615487, 934780.5293518463, 1176776.5085968524, 1423764.556467527, 1679836.2409298916, 1985921.2827147439, 2234922.820106103, 2559419.4497023686])
        actual_output = get_data(*input_)
        print(actual_output[expected_keys[i]][1][:20])
        assert list(actual_output.keys()) == expected_keys
        for i in range(2):
            assert arrays_are_equal(expected_sample[i], actual_output[expected_keys[i]][1][:20])

test_get_data()

def test_decomp():
    input_ = ['355.p_AN', '355.p_PC', '355.s_AN', '355.s_PC', '371.o_PC', '387.o_AN', '387.o_PC', '408.p_AN', '408.p_PC', '408.s_AN', '408.s_PC', '460.p_PC', '460.s_AN', '460.s_PC', '530.o_AN', '530.o_PC', '532.p_AN', '532.p_PC', '532.s_AN', '532.s_PC', '1064.p_AN', '1064.s_AN']
    expected_output = [(('355', 'AN'), 'p'), (('355', 'PC'), 'p'), (('355', 'AN'), 's'), (('355', 'PC'), 's'), (('371', 'PC'), 'o'), (('387', 'AN'), 'o'), (('387', 'PC'), 'o'), (('408', 'AN'), 'p'), (('408', 'PC'), 'p'), (('408', 'AN'), 's'), (('408', 'PC'), 's'), (('460', 'PC'), 'p'), (('460', 'AN'), 's'), (('460', 'PC'), 's'), (('530', 'AN'), 'o'), (('530', 'PC'), 'o'), (('532', 'AN'), 'p'), (('532', 'PC'), 'p'), (('532', 'AN'), 's'), (('532', 'PC'), 's'), (('1064', 'AN'), 'p'), (('1064', 'AN'), 's')]
    actual_output = [decomp(channel) for channel in input_]
    assert expected_output == actual_output

def test_get_calibration_pairs():
    input_ = {'355.p_AN': None, '355.p_PC': None, '355.s_AN': None, '355.s_PC': None, '371.o_PC': None, '387.o_AN': None, '387.o_PC': None, '408.p_AN': None, '408.p_PC': None, '408.s_AN': None, '408.s_PC': None, '460.p_PC': None, '460.s_AN': None, '460.s_PC': None, '530.o_AN': None, '530.o_PC': None, '532.p_AN': None, '532.p_PC': None, '532.s_AN': None, '532.s_PC': None, '1064.p_AN': None, '1064.s_AN': None}
    expected_output = [('355.p_AN', '355.s_AN'), ('355.p_PC', '355.s_PC'), ('408.p_AN', '408.s_AN'), ('408.p_PC', '408.s_PC'), ('460.p_PC', '460.s_PC'), ('532.p_AN', '532.s_AN'), ('532.p_PC', '532.s_PC'), ('1064.p_AN', '1064.s_AN')]
    actual_output = get_calibration_pairs(input_)
    assert expected_output == actual_output
"""
def test_multiply_by_r2():
    input_ = 
    expected_output = [('355.p_AN', '355.s_AN'), ('355.p_PC', '355.s_PC'), ('408.p_AN', '408.s_AN'), ('408.p_PC', '408.s_PC'), ('460.p_PC', '460.s_PC'), ('532.p_AN', '532.s_AN'), ('532.p_PC', '532.s_PC'), ('1064.p_AN', '1064.s_AN')]
    actual_output = get_calibration_pairs(input_)
    assert expected_output == actual_output

"""
