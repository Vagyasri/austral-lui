import pytest
from licel_treatment import get_data
from tk_testsV4 import *

def test_get_color():
    # Test the get_color function with different inputs
    inputs = ['355.p_AN', '387.o_AN', '408.p_AN', '460.p_PC', '530.o_PC', '532.p_AN', '1064.p_AN']
    expected_outputs = ['#A600D5', '#A600D5', '#8108FF', '#0051FF', '#BCFF00', '#BCFF00', '#AF0000']
    
    actual_outputs = [get_color(input_) for input_ in inputs]
    
    for i in range(len(expected_outputs)):
        assert expected_outputs[i] == actual_outputs[i]

def test_get_data():
    pass
    input_ = ...
    expected_output = ...
    
    actual_output = get_data(input_)
    
    assert get_data(input_) == expected_output