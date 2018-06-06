#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name
    read_save_ir_rate
Purpose:
    Save all ionization and recombination rates into files
Update:
    Created on Sat Jan 20 11:46:12 2018
    @author: Chengcai Shen
"""
import ChiantiPy.core as ch
import numpy as np
import time as systime
#import matplotlib.pyplot as plt

# element name list: (...'cu', 'zn')
elem_list = ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne',
             'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar',
             'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni']

# Define temperature list
te_log_s = 4.0
te_log_e = 9.0
nte = 501
temperature = np.logspace(te_log_s, te_log_e, nte, dtype=np.float64)

c_out = np.ndarray(shape=(30, 30, nte), dtype=np.float64)
r_out = np.ndarray(shape=(30, 30, nte), dtype=np.float64)
for ite in range(nte):
    for iatom in range(30):
        for ion in range(30):
            c_out[ion, iatom, ite] = 0.0
            r_out[ion, iatom, ite] = 0.0

# element loop
for iatom in range(len(elem_list)):
    natom = iatom + 1
    nstat = natom + 1
    elemstr = elem_list[iatom]+'_'

    # array
    c_ori = np.ndarray(shape=(nstat, nte), dtype=np.float64)
    r_ori = np.ndarray(shape=(nstat, nte), dtype=np.float64)

    for ion in range(nstat):
        for ite in range(nte):
            c_ori[ion, ite] = 0
            r_ori[ion, ite] = 0

    # ionization ion loop
    for ion in range(1,nstat):
        ionstr = '{:d}'.format(ion)
        ionname = elemstr + ionstr

        #fe14 = ch.ion('fe_14',temperature=temperature,eDensity=1.e+9,em=1.e+27)
        ionicstruc = ch.ion(ionname, temperature=temperature,eDensity=1.e+9)

        ionicstruc.ionizRate()
        ionizrate = ionicstruc.IonizRate['rate']
        #print(ionname)
        #print('ioniz', ionizrate)

        # save into arraies
        for ite in range(nte):
            c_ori[ion-1, ite] = ionizrate[ite]
            # test negative value
            if ((ionizrate[ite] < -0.0) or (ionizrate[ite] >= 1.0)):
                print('Negative_ioniz', ion, ite, iatom, ionizrate[ite])
                systime.sleep(40)

    # recombination ion loop
    for ion in range(2,nstat+1):
        ionstr = '{:d}'.format(ion)
        ionname = elemstr + ionstr

        #fe14 = ch.ion('fe_14',temperature=temperature,eDensity=1.e+9,em=1.e+27)
        ionicstruc = ch.ion(ionname, temperature=temperature,eDensity=1.e+9)

        ionicstruc.recombRate()
        recombrate = ionicstruc.RecombRate['rate']
        #print(ionname)
        #print('recomb', recombrate)

        # save into arraies
        for ite in range(nte):
            r_ori[ion-2, ite] = recombrate[ite]
            # test negative value
            if ((recombrate[ite] < -0.0) or (recombrate[ite] >= 1.0)):
                print('Negative_recomb', ion, ite, iatom, recombrate[ite])
                systime.sleep(40)

    # write into outarray
    for ion in range(nstat):
        for ite in range(nte):
            c_out[ion, iatom, ite] = c_ori[ion, ite]
            r_out[ion, iatom, ite] = r_ori[ion, ite]

    print(ionname)
    print('c_max=',np.amax(c_ori), 'c_min=',np.amin(c_ori))
    print('r_max=',np.amax(r_ori), 'r_min=',np.amin(r_ori))

outname='ionrecomb_rate.dat'
fh = open(outname, 'w')
fh.write("%d \n" % (nte))

#fh.writelines(te_str)

#fh.writelines(c_str)
#fh.writelines(r_str)
for ite in range(nte-1):
    fh.write("%.14e " % (temperature[ite]))
fh.write("%.14e \n" % (temperature[nte-1]))

ntol = 30*30*nte
i = 0
for ite in range(nte):
    for iatom in range(30):
        for ion in range(30):
            i = i + 1
            if (i < ntol):
                fh.write("%.14e " % (c_out[ion, iatom, ite]))
            else:
                fh.write("%.14e \n" % (c_out[ion, iatom, ite]))

i = 0
for ite in range(nte):
    for iatom in range(30):
        for ion in range(30):
            i = i + 1
            if (i < ntol):
                fh.write("%.14e " % (r_out[ion, iatom, ite]))
            else:
                fh.write("%.14e \n" % (r_out[ion, iatom, ite]))
fh.close()
