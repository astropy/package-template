#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name
    test_eigenvaluetable
Purpose:
    Test all functions in Class: eigenvaluetable.
Author:
    Chengcai
Update:
    Created on May 10 10:55:12 2018
    @author: chshen
"""
import numpy as np
from plasmapy import atomic
import nei as nei

def test_element_range():
    """
    Function test_element_range:
        This function is used to test element including Hydrogen to Iron.
    """
    atomic_numb = np.linspace(1, 26, 26, endpoint=True)
    for i in atomic_numb:
        element_symbol = atomic.atomic_symbol(int(i))
        eigen = nei.EigenData2(element=element_symbol)
        print(f'Element: ', element_symbol)

def test_temperature_range():
    """
    Function test_temperature_range:
        This function is used to test Te inputs.
    """
    logte_array = np.linspace(2.0, 10.0, 100, endpoint=True)
    for i in logte_array:
        te = 10.0**(i)
        eigen = nei.EigenData2(temperature=te)
        print(f'Te: ', te)
