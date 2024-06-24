from licel_treatment import *
import numpy as np
from numpy import nan
import pytest
config = get_config(r'../austral-data-sample/instruments/lilas/private/config/lidar', *([False] * 4))
config_dir=r'../austral-data-sample/instruments/lilas/private/config/lidar'
directory = r'../austral-data-sample/instruments/lilas/private/measurement/2023/05/28/'
filenames = [directory + file_name for file_name in ['l2352800.005799', 'l2352800.015859', 'l2352800.025916', 'l2352800.035973']]

def arrays_are_equal(a, b):
    a, b = np.array(a), np.array(b)
    return np.array_equal(np.isnan(a), np.isnan(b)) and np.array_equal(a[~np.isnan(a)], b[~np.isnan(b)])

def test_get_data():
    expected_keys = ['355.p_AN', '355.p_PC', '355.s_AN', '355.s_PC', '371.o_PC', '387.o_AN', '387.o_PC', '408.p_AN', '408.p_PC', '408.s_AN', '408.s_PC', '460.p_PC', '460.s_AN', '460.s_PC', '530.o_AN', '530.o_PC', '532.p_AN', '532.p_PC', '532.s_AN', '532.s_PC', '1064.p_AN', '1064.s_AN']
    expected_sample = [([nan, 5.040793233965592, 5.040732234737231, 5.040711901661111, 5.039878245540194, 5.03078936051459, 5.219764969973131, 6.990165907734602, 7.0700545638097685, 6.376859332729442, 6.293392055257168, 6.145448593408627, 6.122533216621477, 6.043173220525428, 6.0145645824247, 6.025991771204095, 6.03237635710575, 6.058728023757167, 6.172288253886922, 6.3708814083501855], 
                        [nan, 75.43487161332223, 69.71027513527615, 66.93118324041076, 65.83285949752984, 62.17178035459338, 62.87071364551762, 62.13849781693033, 62.820789839023035, 65.26705635725784, 69.86004655475992, 76.91594453932834, 86.55123919278378, 98.33325752550651, 106.73709828542879, 112.49497730113794, 116.65529450902025, 122.16355449225645, 122.62951001953927, 126.04097013000276]),
                       ([nan, 1.2506454539886347, 1.1027019921400933, 1.0797866153529432, 1.0004266192568938, 0.9718179811561658, 0.9832451699355609, 0.9896297558372158, 1.0159814224886334, 1.1295416526183883, 1.3281348070816517, 1.679002368606998, 2.257417384990374, 3.017203440363441, 3.872636285804613, 4.730204104238376, 5.688847644064263, 6.616320578198313, 7.469964112940933, 8.340789097004883], 
                        [nan, 118.2526520532951, 104.76591238420065, 98.61231689811248, 96.24653025427082, 88.61736213441205, 90.04418052578784, 88.54975869720862, 89.9418103663431, 95.04196787645918, 105.10455763921543, 121.93327373893587, 148.063685533801, 186.2370814937663, 218.8751719111059, 244.54146155256038, 265.09276163360624, 295.35573968612033, 298.09420231239744, 319.08834245818497]),
                       ([nan, 283.5446194105645, 1134.164752815877, 2551.8604002159373, 4535.890420986175, 7074.547538223643, 10570.02406419559, 19266.644783193497, 25452.196429715168, 29054.56533474852, 35400.33031082157, 41827.45948888747, 49592.519054633965, 57447.915427619846, 66310.57452123231, 76266.45835430182, 86866.2195423228, 98492.19743620245, 112489.95342708916, 129368.71059831095], 
                        [nan, 4243.211528249375, 15684.811905437133, 33883.91151545795, 59249.573547776854, 87429.06612364695, 127313.19513217318, 171269.23460791423, 226154.84342048294, 297373.025527756, 392962.76187052455, 523509.1475208035, 701065.0374615487, 934780.5293518463, 1176776.5085968524, 1423764.556467527, 1679836.2409298916, 1985921.2827147439, 2234922.820106103, 2559419.4497023686]),
                       ([nan, 70.3488067868607, 248.107948231521, 546.6419740224275, 900.3839573312044, 1366.6190360008582, 1991.0714691195108, 2727.667014526326, 3657.5331209590804, 5146.474154742532, 7470.758289834291, 11427.709871331379, 18285.08081842203, 28682.290204954963, 42695.81505099586, 59866.64569426695, 81919.4060745254, 107556.56139933632, 136140.0959583485, 169370.1486010554], 
                        [nan, 6651.711677997849, 23572.330286445147, 49922.48542966945, 86621.87722884375, 124618.16550151694, 182339.46556472036, 244065.27240918126, 323790.5173188352, 433034.9661371171, 591213.1367205868, 829908.3443856322, 1199315.852823788, 1770416.255950116, 2413098.7703199424, 3094977.872774592, 3817335.76752393, 4801376.743272494, 5432766.8371434435, 6479487.654041518]),
                       ([nan, 5.040528903976031, 5.040513654168943, 5.04091523242231, 5.04114397952866, 5.0308605262810095, 5.222718349279549, 7.030557563446825, 7.094230591316355, 6.359794798595799, 6.30579523169032, 6.152646502355079, 6.113322333139154, 6.0425886445869805, 6.0197190172210995, 6.019957930865509, 6.033448926871076, 6.066830754590955, 6.1669914875576834, 6.364913650508989], 
                        [nan, 74.89403037629754, 70.30520049600332, 67.6758800206217, 65.31281984654454, 62.83327079064668, 62.68765968837079, 62.467162876353036, 63.399073930918675, 65.36690397024701, 69.34832753819039, 76.97418898023868, 86.85078203175132, 97.57191947646405, 107.3278633289481, 113.06910107582569, 117.3542277999445, 120.84889425456564, 122.98313698220926, 124.91768448387455]),
                       ([nan, 1.262750476186102, 1.1096017468508612, 1.0702775776349354, 0.9995438890827621, 0.9766742617168814, 0.9769131753612905, 0.990404171366858, 1.0237859990867373, 1.123946732053465, 1.3218688950047708, 1.685058300658789, 2.2428098284352966, 3.0076893193764027, 3.8517508919975083, 4.743432528891469, 5.659071612723724, 6.561651778417963, 7.457532195530687, 8.283126251765875], 
                        [nan, 116.93095344990367, 106.11800765652347, 100.24337297256466, 95.14453592078867, 89.97341576299355, 89.67283735166895, 89.22074522956397, 91.13441854810262, 95.26568060452036, 103.9609786942799, 122.09487237030702, 148.95098074586065, 183.53585414636945, 221.38024327596963, 247.28606804102645, 268.746020841017, 287.8600844037313, 300.2164630193293, 312.0470453071766]),
                       ([nan, 283.52975084865176, 1134.115572188012, 2551.9633364137944, 4537.029581575794, 7074.647615082669, 10576.004657291087, 19377.97428425031, 25539.230128738876, 28976.81505110211, 35470.09817825805, 41876.45025665426, 49517.910898427144, 57442.35830260498, 66367.40216486262, 76190.0925625166, 86881.66454694349, 98623.91745431922, 112393.41986073878, 129247.52781564817], 
                        [nan, 4212.789208666736, 15818.670111600746, 34260.914260439735, 58781.53786189009, 88359.2870493469, 126942.51086895086, 172175.11767794806, 228236.66615130723, 297827.95621443796, 390084.34240232094, 523905.57374674955, 703491.3344571857, 927543.0595231364, 1183289.6932016527, 1431030.8104909188, 1689900.8803192007, 1964549.8372257827, 2241367.671500764, 2536609.7305506775]),
                       ([nan, 71.02971428546823, 249.66039304144377, 541.828023677686, 899.5895001744859, 1373.4481805393646, 1978.2491801066133, 2729.8014973299023, 3685.6295967122546, 5120.9822979186, 7435.512534401835, 11468.928058858883, 18166.759610325902, 28591.84659232193, 42465.55358427253, 60034.06794378265, 81490.63122322163, 106667.85172290701, 135913.52426354677, 168199.2324499208], 
                        [nan, 6577.366131557082, 23876.55172271778, 50748.207567360856, 85630.0823287098, 126525.11591670968, 181587.4956371296, 245914.6790389857, 328083.9067731694, 434054.25725434587, 584780.5051553245, 831008.2250704021, 1206502.9440414712, 1744737.7134789245, 2440717.182117565, 3129714.298644241, 3869942.700110645, 4679525.497088158, 5471445.038527276, 6336505.313768854])]
    for i in range(8):
        filters, r2, avg = [bool((i >> j) & 1) for j in range(3)]
        input_ = [filenames, config_dir] + [filters] * 4 + [r2, avg]
        actual_output = get_data(*input_)
        assert list(actual_output.keys()) == expected_keys
        for j in range(2):
            assert arrays_are_equal(expected_sample[i][j], actual_output[expected_keys[j]][1][:20])

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

def test_multiply_by_r2():
    distance = np.array([i for i in range(20)])
    power = np.array([i**2 for i in range(20)])
    expected_output = ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                        ([nan, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                         [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361]))
    for i in range(2):
        r2 = bool(i)
        actual_output = multiply_by_r2(distance, power, r2)
        assert arrays_are_equal(expected_output[0], actual_output[0])
        assert arrays_are_equal(expected_output[1][i], actual_output[1])

def get_calibration_data(data):
    pairs = get_calibration_pairs(data)
    return {Pr2Object.get_calibration_header(p): (data[s][0], [data[s][1][i] / data[p][1][i] for i in range(min(len(data[s][0]), len(data[p][0])))]) for p, s in pairs}

def test_get_calibration_data():
    ranges = [0.0, 7.5, 15.0, 22.5, 30.0, 37.5, 45.0, 52.5, 60.0, 67.5, 75.0, 82.5, 90.0, 97.5, 105.0, 112.5, 120.0, 127.5, 135.0, 142.5]
    input_ = {'355.p_AN': (ranges, [nan, 1.6587045088171637, 1.6090771110268065, 1.4764179681202254, 1.4774616632404012, 1.7581973401270403, 2.2181373001919695, 2.8314210976797156, 3.6341508181799935, 4.551101067797077, 5.639980252152393, 6.9168588347045565, 8.364036722772221, 9.98030542726887, 11.668424301091319, 13.410217180099892, 15.129024352543658, 16.754362828669436, 18.368800489095598, 19.840550988589165]),
              '355.s_AN': (ranges, [nan, 3.6341174579597855, 2.7089580274266982, 2.2480842348858223, 1.8674773109147393, 1.8450653314920127, 1.8550201077552115, 2.0986527282936063, 2.3397157836530873, 2.6752973339309634, 3.139656213685994, 3.7007125308032958, 4.446826368644203, 5.191994167048691, 5.956754137007363, 6.7564382208704, 7.581848473923744, 8.363362497127344, 9.114584947924902, 9.710730172912916]),
              '532.p_AN': (ranges, [nan, 5.045349891558877, 0.5232935924468425, 0.40871295799617524, 0.3593785272570953, 0.2400310747429346, 0.32566290243924634, 0.38081394984223055, 0.46179492559951196, 0.6106771189705835, 0.7210707659800768, 0.9045352783623599, 1.0530634698798034, 1.2524641691555347, 1.4399386680521777, 1.6214134458778675, 1.7793532039176005, 1.9552860216899584, 2.105645257277887, 2.2457201286699293]),
              '532.s_AN': (ranges, [nan, 3.847406014669823, 1.3443382529167325, 1.232369908006623, 1.2700772088981276, 1.3034083144611754, 1.3951741397936086, 2.4719135019616134, 2.867449538587379, 4.431362589628647, 5.103679247948805, 6.830475876020115, 8.032928620587331, 9.875386199110892, 11.45234849089448, 13.23164115246657, 14.804471388131098, 16.548968108883756, 18.075851345339597, 19.554291259170665])}
    expected_output = {'355A': (ranges, [nan, 2.190937227602586, 1.6835476739197541, 1.5226611186181118, 1.2639768309242945, 1.0494074182586897, 0.8362963408958806, 0.7412012045871255, 0.6438136171863204, 0.587835184074679, 0.5566785827818816, 0.5350279106804073, 0.5316603114064667, 0.5202239755972569, 0.510502016664773, 0.5038276509717251, 0.5011458966056195, 0.49917520484970473, 0.496199245744743, 0.48943853315857094]),
                       '532A': (ranges, [nan, 0.7625647571255119, 2.5689942936828407, 3.0152455015095354, 3.5340931985887094, 5.4301648895130885, 4.284105218444044, 6.491131700888888, 6.209356966980083, 7.2564739237300735, 7.077917298466403, 7.551364816181114, 7.628152386203473, 7.884765442646796, 7.953358531850672, 8.160559656209513, 8.320142035620643, 8.46370706142544, 8.584471331466107, 8.707358948931926])}
    actual_output = get_calibration_data(input_)
    assert expected_output.keys() == actual_output.keys()
    for chan in expected_output:
        assert arrays_are_equal(expected_output[chan], actual_output[chan])

def test_get_polarisation_data():
    paths = ['../austral-data-sample/instruments/lilas/private/calibration/20210112/200449/l2111220.082534', 
             '../austral-data-sample/instruments/lilas/private/calibration/20210112/200449/l2111220.123147', 
             '../austral-data-sample/instruments/lilas/private/calibration/20210112/200449/l2111220.195610'] 
    input_ = (paths, config_dir)
    expected_output = (([nan, 1.0069961318471805, 1.0065612948905076, 1.0063249375067305, 1.0067051509260394, 1.0035520315328734, 1.0241617283625588, 0.9544049414521795, 0.7847005138430861, 0.4089363559478913, 0.7874193611384155, 0.6745356927148777, 0.8026248879451309, 0.7617550510101169, 0.7214268312948414, 0.692768228612746, 0.5760597147104406, 0.5555081459344821, 0.45725471354554237, 0.4362832432870485],
                        [nan, 1.007020490849987, 1.0067263032713825, 1.00662108251663, 1.0067074798598006, 1.0025909288841015, 1.0271325683551824, 0.9568529118462541, 0.87825805059208, 0.43545057856446595, 0.7136101149236365, 0.7459648197608151, 0.7732133879284664, 0.8265834988248988, 0.7257273275794223, 0.7548410329719497, 0.6108929553401281, 0.6112824587908661, 0.501399607041626, 0.48033966529991323],
                        [nan, 1.006679330279707, 1.0068579089393443, 1.0063827373934922, 1.0062587141395614, 1.002890832406197, 1.0257125849950777, 0.9573352266767787, 1.267474767244792, 0.8879554507562674, 1.1464804603337733, 1.1498623973301039, 1.1664711205383549, 1.1974682711548479, 1.1955618186824757, 1.3726685424199359, 1.4217980743579175, 1.6495550767307599, 1.7306151655314335, 1.9567880434676137]),
                       ([nan, 0.01695920757390985, 0.2497627280616271, -0.08090552752519219, 0.23328087218495092, 0.05397328999007669, 0.04248833946552293, 0.14969607514470784, 0.045108862820194044, 0.1421537834157741, 0.06310055919141362, 0.11415187896029039, 0.08195366062513229, 0.09863339502834328, 0.09109444995912719, 0.097340164770108, 0.08890140567532334, 0.0945679810172921, 0.09056715596751116, 0.0939565785861339],
                        [nan, 0.035788560270053275, 0.1338392291135402, -0.0056640374430187365, 0.09076580968302048, 0.2039285642916861, -0.06838509578103596, 0.21862437508187266, 0.007772074323577741, 0.163364699778158, 0.059921865607132474, 0.11970815273604363, 0.0854129049584699, 0.10191781327955847, 0.09236241032866278, 0.0983816783076475, 0.09088267613244447, 0.09366948721392918, 0.09082575693613698, 0.09333150563310827],
                        [nan, 0.7625647571255119, 2.5689942936828407, 3.0152455015095354, 3.5340931985887094, 5.4301648895130885, 4.284105218444044, 6.491131700888888, 6.209356966980083, 7.2564739237300735, 7.077917298466403, 7.551364816181114, 7.628152386203473, 7.884765442646796, 7.953358531850672, 8.160559656209513, 8.320142035620643, 8.46370706142544, 8.584471331466107, 8.707358948931926]))
    for i in range(2):
        actual_output = get_polarization_data(paths, config_dir, *[i]*4)
        for j, data in enumerate(actual_output['532A']):
            y = data[1]
            assert arrays_are_equal(expected_output[i][j], y[:20])

def test_get_v_star_points():
    x = [i for i in range(10)]
    y1, y2 = [nan]+[i**2 for i in range(1, 10)], [nan]+[i**2 for i in range(2, 11)]
    expected_output = (x, [nan]+[i*i+i for i in range(1, 10)])
    actual_output = get_v_star_points(x, y1, x, y2)
    assert expected_output == actual_output

def test_average_interval():
    x = [0.0, 7.5, 15.0, 22.5, 30.0, 37.5, 45.0, 52.5, 60.0, 67.5, 75.0, 82.5, 90.0, 97.5, 105.0, 112.5, 120.0, 127.5, 135.0, 142.5]
    y = [nan, 77.2355141382399, 121.24605418865595, 69.5541352109456, 101.52957837324448, 73.13233731621308, 72.16862726291066, 71.83396862625638, 69.29290600924898, 70.58220877566575, 69.15013661686716, 71.88673771078146, 70.96130571692542, 72.45757852523636, 73.044034384553, 73.42840986330587, 71.60606325270618, 69.51517757295996, 65.27805501006938, 60.963416613824414]
    interval = (15, 120)
    actual_output = average_interval((x, y), interval)
    expected_output = 76.79160545556776
    assert expected_output == actual_output

def test_get_V_star_constant():
    x = [0.0, 7.5, 15.0, 22.5, 30.0, 37.5, 45.0, 52.5, 60.0, 67.5, 75.0, 82.5, 90.0, 97.5, 105.0, 112.5, 120.0, 127.5, 135.0, 142.5]
    y1 = [nan, 77.2355141382399, 121.24605418865595, 69.5541352109456, 101.52957837324448, 73.13233731621308, 72.16862726291066, 71.83396862625638, 69.29290600924898, 70.58220877566575, 69.15013661686716, 71.88673771078146, 70.96130571692542, 72.45757852523636, 73.044034384553, 73.42840986330587, 71.60606325270618, 69.51517757295996, 65.27805501006938, 60.963416613824414] 
    y2 = [nan, 73.22358859297711, 98.14230191282981, 70.15518659156514, 80.74845566698251, 76.08094439262128, 67.26325871541032, 71.98161023245088, 65.79527667506538, 69.79187248780681, 67.37178222134446, 69.57293828932639, 69.04076010549181, 68.94735764054217, 68.61470033972537, 69.59783226816694, 67.28000864967976, 63.684174781253674, 59.125224242698756, 55.01080302126245]
    interval = (15, 120)
    input_ = ((x, y1), (x, y2), interval)
    expected_output = 74.37044388080594
    actual_output = get_V_star_constant(*input_)
    assert expected_output == actual_output

def test_make_data_regular():
    x, y = ([0,1,2], [5,8])
    input_ = (x, y)
    expected_output = ([0,1], [5,8])
    make_data_regular(*input_)
    assert (x, y) == expected_output

def test_find_ylim():
    x = [0.0, 7.5, 15.0, 22.5, 30.0, 37.5, 45.0, 52.5, 60.0, 67.5, 75.0, 82.5, 90.0, 97.5, 105.0, 112.5, 120.0, 127.5, 135.0, 142.5]
    y1 = [nan, 77.2355141382399, 121.24605418865595, 69.5541352109456, 101.52957837324448, 73.13233731621308, 72.16862726291066, 71.83396862625638, 69.29290600924898, 70.58220877566575, 69.15013661686716, 71.88673771078146, 70.96130571692542, 72.45757852523636, 73.044034384553, 73.42840986330587, 71.60606325270618, 69.51517757295996, 65.27805501006938, 60.963416613824414] 
    y2 = [nan, 73.22358859297711, 98.14230191282981, 70.15518659156514, 80.74845566698251, 76.08094439262128, 67.26325871541032, 71.98161023245088, 65.79527667506538, 69.79187248780681, 67.37178222134446, 69.57293828932639, 69.04076010549181, 68.94735764054217, 68.61470033972537, 69.59783226816694, 67.28000864967976, 63.684174781253674, 59.125224242698756, 55.01080302126245]
    data_channel = ((x, y1), (x, y2))
    xlim = (7, 130)
    num_std = 5
    input_ = (data_channel, xlim, num_std, 0)
    expected_output = (18.25507324009014, 129.74003400155436)
    actual_output = find_ylim(*input_)
    assert actual_output == expected_output


def test_is_a_supported_file():
    supported_file = '../austral-data-sample/instruments/lilas/private/calibration/20210112/200449/l2111220.082534'
    not_supported_file = '../austral-data-sample/instruments/lilas/private/calibration/20210112/200449/temp.dat'
    for expected_output, input_ in enumerate((not_supported_file, supported_file)):
        actual_output = is_a_supported_file(input_) 
        assert expected_output == actual_output

def test_smooth():
    input_ = ([0.19665518, 0.50681873, 0.3431207, -0.20730004, 0.40436148, 0.79788613, 1.48482336, 0.77745675, 0.70173037, 1.22708082, 1.29175892, 0.57910521, 0.7952736, 0.91258831, 1.08316924, 1.24769848, 0.49634497, 0.81089573, 1.07329307, 0.64548538, 0.5950947, 0.04875953, 0.33373195, 0.5202903, -0.41516863, 0.04359212, -0.18160384, -0.15161349, -0.15073139, -0.90997117, -0.66215456, -0.90316299, -0.13746771, -0.7979537, -0.61711439, -1.23316213, -1.0822021, -0.40306, -1.01802977, -0.48083434, -0.7667645, -1.07325031, -1.19189657, -0.73657067, -1.00630723, -0.72121741, -0.0236818, -1.15940372, -0.34784528, 0.09341173], 5)
    expected_output = [0.34886487000000005, 0.20982364250000002, 0.24873121, 0.3689774, 0.564578326, 0.651445536, 0.8332516179999999, 0.997795486, 1.096570044, 0.915426414, 0.9189897840000001, 0.961161372, 0.9323790559999999, 0.923566968, 0.9070149200000002, 0.910139346, 0.942280298, 0.854743526, 0.7242227699999999, 0.6347056819999999, 0.539272926, 0.428672372, 0.21654157000000002, 0.10624105399999999, 0.06016838, -0.03690070799999999, -0.171105046, -0.270065554, -0.41121489, -0.5555267199999999, -0.552697564, -0.682142026, -0.62357067, -0.737772184, -0.773580006, -0.826698464, -0.8707136779999999, -0.8434576680000001, -0.750178142, -0.748387784, -0.9061550979999999, -0.8498632779999999, -0.954957856, -0.9458484379999998, -0.7359347359999999, -0.7294361659999999, -0.651691088, -0.431747296, -0.35937976750000006, -0.47127909000000007]
    actual_output = smooth(*input_)
    assert expected_output == actual_output.tolist()
"""
def test():
    test_get_data()
    test_decomp()
    test_get_calibration_pairs()
    test_multiply_by_r2()
    test_get_calibration_data()
    test_get_polarisation_data()
    test_get_v_star_points()
    test_average_interval()
    test_get_V_star_constant()
    test_make_data_regular()
    test_find_ylim()
    test_is_a_supported_file()
    test_smooth()

test()
"""