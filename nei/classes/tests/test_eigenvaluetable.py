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
import warnings
import numpy as np
from plasmapy import atomic
import nei as nei

#------------------------------------------------------------------------------
# function: Time-Advance solover
#------------------------------------------------------------------------------
def func_solver_eigenval(natom, te, ne, dt, f0):

    table = nei.EigenData2(element=natom,
                           temperature=te)
    evals = table.eigenvalues # find eigenvalues on the chosen Te node
    evect = table.eigenvectors
    evect_invers = table.eigenvector_inverses

    # define the temperary diagonal matrix
    diagona_evals = np.zeros((natom+1, natom+1))
    for ii in range(0, natom+1):
        print(ii, ne, dt, evals[ii], evals[ii]*dt*ne, np.exp(evals[ii]*dt*ne))
        diagona_evals[ii,ii] = np.exp(evals[ii]*dt*ne)

    print(f'evals', evals)
    print(f'evect', evect)
    print(f'evect_invers', evect_invers)
    print(f'diagona_evals', diagona_evals)

    # matirx operation
    matrix_1 = np.dot(diagona_evals, evect)
    matrix_2 = np.dot(evect_invers, matrix_1)

    # get ions fraction at (time+dt)
    ft = np.dot(f0, matrix_2)

    # re-check the smallest value
    minconce = 1.0e-15
    for ii in np.arange(0, natom+1, dtype=np.int):
        if (abs(ft[ii]) <= minconce):
            ft[ii] = 0.0
    return ft

def test_equlibrium_state_vs_chiantipy(natom=8,
                                       temperatures=[1.0e5, 1.0e6]):
    """
        Test equilibrium states saved in EigenData2 and compare them with
        Outputs from ChiantiPy.
        Note:
        This test requires ChiantiPy to be installed (see details in: https://github.com/chianti-atomic/ChiantiPy).
    """
    try:
        import ChiantiPy.core as ch
    except ImportError:
        warnings.warn('ChiantiPy is required in this test.', UserWarning)
        return

    eqi_ch = ch.ioneq(natom)
    eqi_ch.calculate(temperatures)
    conce = eqi_ch.Ioneq
    for i in range(2):

        ch_conce = conce[:, i]
        table_sta = nei.EigenData2(element=natom,
                                       temperature=temperatures[i])
        table_conce = table_sta.equilibrium_state
        print(f'Te=', temperatures[i])
        print(f'Fraction (ChiantiPy):', ch_conce)
        print(f'Fraction (EigenData2):', table_conce)

    return

def test_reachequlibrium_state(natom=2):
    """
        Starting the random initial distribution, the charge states will reach
        to equilibrium cases after a long time.
        In this test, we set the ionization and recombination rates at
        Te0=2.0e6 K and plasma density ne0=1.0e+7. A random charge states
        distribution will be finally closed to equilibrium distribution at
        2.0e6K.
    """
    #
    # Initial conditions, set plasma temperature, density and dt
    #
    element_symbol = atomic.atomic_symbol(int(natom))
    te0 = 2.0e+6
    ne0 = 1.0e+7

    # Start from any ionizaiont states, e.g., Te = 4.0d4 K,
    time = 0
    table_sta = nei.EigenData2(element=natom, temperature=4.0e+4)
    f0 = table_sta.equilibrium_state

    print('START-------------------------------')
    print(f'time_sta = ', time)
    print(f0)
    print(f'Sum(f0) = ', np.sum(f0))

    # After time + dt:
    dt = 1.0e+6
    ft = func_solver_eigenval(natom, te0, ne0, time+dt, f0)

    print('END---------------------------------')
    print(f'time_end = ', time+dt)
    print(ft)
    print(f'Sum(ft) = ', np.sum(ft))

    print('EQI---------------------------------')
    table_end = nei.EigenData2(element=natom, temperature=te0)
    print(table_end.equilibrium_state)
    print('************************************')

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
