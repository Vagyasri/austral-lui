from licel_treatment import *
from main import *
import numpy as np
from numpy import nan
config = get_config(r'./austral-data-sample/instruments/lilas/private/config/lidar', *([False] * 4))
config_dir=r'./austral-data-sample/instruments/lilas/private/config/lidar'
directory = r'./austral-data-sample/instruments/lilas/private/measurement/2023/05/28/'
filenames = [directory + file_name for file_name in ['l2352800.005799', 'l2352800.015859', 'l2352800.025916', 'l2352800.035973']]

def test_get_data():
    
    input_ = [filenames, config_dir] + [False] * 5
    expected_keys = ['355.p_AN', '355.p_PC', '355.s_AN', '355.s_PC', '371.o_PC', '387.o_AN', '387.o_PC', '408.p_AN', '408.p_PC', '408.s_AN', '408.s_PC', '460.p_PC', '460.s_AN', '460.s_PC', '530.o_AN', '530.o_PC', '532.p_AN', '532.p_PC', '532.s_AN', '532.s_PC', '1064.p_AN', '1064.s_AN']
    expected_sample = ([nan, 283.5446194105645, 1134.164752815877, 2551.8604002159373, 4535.890420986175, 7074.547538223643, 10570.02406419559, 19266.644783193497, 25452.196429715168, 29054.56533474852, 35400.33031082157, 41827.45948888747, 49592.519054633965, 57447.915427619846, 66310.57452123231, 76266.45835430182, 86866.2195423228, 98492.19743620245, 112489.95342708916, 129368.71059831095], [nan, 4243.211528249375, 15684.811905437133, 33883.91151545795, 59249.573547776854, 87429.06612364695, 127313.19513217318, 171269.23460791423, 226154.84342048294, 297373.025527756, 392962.76187052455, 523509.1475208035, 701065.0374615487, 934780.5293518463, 1176776.5085968524, 1423764.556467527, 1679836.2409298916, 1985921.2827147439, 2234922.820106103, 2559419.4497023686])
    actual_output = get_data(*input_)

    assert list(actual_output.keys()) == expected_keys
    print((actual_output[expected_keys[0]][1][:20], actual_output[expected_keys[1]][1][:20]))
    print(expected_sample)
    assert expected_sample == (actual_output[expected_keys[0]][1][:20], actual_output[expected_keys[1]][1][:20])


test_get_data()