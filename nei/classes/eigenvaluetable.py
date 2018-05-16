#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name
    Rate_eigenvalue_180402
Purpose:
    Get ionization rate and recombination rate from ChiantiPy,
    and calculate eigenvalues using scipy.
Author:
    Chengcai
Update:
    Created on April 2 10:55:12 2018
    @author: chshen
    2018-04-04
    rerange outputs.
    2018-05-10
    read hdf5 files: ionizrecombrates.h5.
"""
import warnings
import numpy as np
from numpy import linalg as LA
from scipy.io import FortranFile
from plasmapy import atomic
import astropy.units as u
from .. import __path__
import h5py

class EigenData2:
    """A class to contain eigenvalue and eigenvector information on the
    ionization and recombination rates for an element.
    Input arguments:
        (1) element = 'H': Input the element symbol. The defaut value
    is for Hydrogen.
        (2) temperature = None: Input temperature in unit of K.
    """

    def __init__(self, element='H', temperature=None):
        """Read in the """

        self._element = element
        self._temperature = temperature

        #
        # 1. Read ionization and recombination rates
        #
        data_dir = __path__[0] + '/data/ionizrecombrates/chianti_8.07/'
        filename = data_dir + 'ionrecomb_rate.h5'
        f = h5py.File(filename, 'r')

        atomic_numb = atomic.atomic_number(element)
        nstates = atomic_numb + 1

        self._temperature_grid = f['te_gird'][:]
        ntemp = len(self._temperature_grid)
        c_ori = f['ioniz_rate'][:]
        r_ori = f['recomb_rate'][:]
        f.close()

        #
        # Ionization and recombination rate for the current element
        #
        c_rate = np.zeros((ntemp, nstates))
        r_rate = np.zeros((ntemp, nstates))
        for ite in range(ntemp):
            for i in range(nstates-1):
                c_rate[ite, i] = c_ori[i, atomic_numb-1, ite]
            for i in range(1, nstates):
                r_rate[ite, i] = r_ori[i-1, atomic_numb-1, ite]

        #
        # 2. Definet the grid size
        #
        self._ntemp = ntemp
        self._atomic_numb = atomic_numb
        self._nstates = nstates

        # Get the current temperature index in the list of temperature gird
        if self._temperature:
            self._te_index = self._get_temperature_index(temperature)

        #
        # Compute eigenvalues and eigenvectors
        #
        self._ionization_rate = np.ndarray(shape=(ntemp, nstates),
                                           dtype=np.float64)

        self._recombination_rate = np.ndarray(shape=(ntemp, nstates),
                                              dtype=np.float64)

        self._equilibrium_states = np.ndarray(shape=(ntemp, nstates),
                                              dtype=np.float64)

        self._eigenvalues = np.ndarray(shape=(ntemp, nstates),
                                       dtype=np.float64)

        self._eigenvectors = np.ndarray(shape=(ntemp, nstates, nstates),
                                        dtype=np.float64)

        self._eigenvector_inverses = np.ndarray(shape=(ntemp, nstates, nstates),
                                                dtype=np.float64)

        #
        # Save ionization and recombination rates
        #
        self._ionization_rate = c_rate
        self._recombination_rate = r_rate

        #
        # Define the coefficients matrix A. The first dimension is
        # for elements, and the second number of equations.
        #
        neqs = nstates
        A = np.ndarray(shape=(nstates, neqs), dtype=np.float64)

        #
        # Enter temperature loop over the whole temperature grid
        #
        for ite in range(ntemp):
            # Ionization and recombination rate at Te(ite)
            carr = c_rate[ite, :]
            rarr = r_rate[ite, :]

            # Equilibirum
            eqi = self._function_eqi(carr, rarr, atomic_numb)

            # Initialize A to zero
            for ion in range(nstates):
                for jon in range(nstates):
                    A[ion, jon] = 0.0

            # Give coefficients
            for ion in range(1, nstates-1):
                A[ion, ion-1] = carr[ion-1]
                A[ion, ion  ] = -(carr[ion]+rarr[ion])
                A[ion, ion+1] = rarr[ion+1]

            # The first row
            A[0, 0] = -carr[0]
            A[0, 1] = rarr[1]

            # The last row
            A[nstates-1, nstates-2] = carr[nstates-2]
            A[nstates-1, nstates-1] = -rarr[nstates-1]

            # Compute eigenvalues and eigenvectors using Scipy
            la, v = LA.eig(A)

            # Rerange the eigenvalues. Try a simple way in here.
            idx = np.argsort(la)
            la = la[idx]
            v = v[:, idx]

            #print('----------------------------------------------------------')
            #print(f'Temperature = ', temperature[ite])
            #print('(a) Check line by line:')

            #for ion in range(nstates):
                #u = np.copy(v[:, ion])
                #lam = np.copy(la[ion])
                #print(f'eig=', lam)
                #print(f'u=', u)
                #print(f'Au-lamu:', np.dot(A, u)-lam*u)

            # Compute inverse of eigenvectors
            v_inverse = LA.inv(v)

            # Save eigenvalues and eigenvectors into arrays
            for j in range(nstates):
                self._eigenvalues[ite, j] = la[j]
                self._equilibrium_states[ite, j] = eqi[j]
                for i in range(nstates):
                    self._eigenvectors[ite, i, j] = v[i, j]
                    self._eigenvector_inverses[ite, i, j] = v_inverse[i, j]

    #---------------------------------------------------------------------------
    #   The following Functions is used to obtain the eigen values and relative
    #   def properties.
    #---------------------------------------------------------------------------
    def _get_temperature_index(self, T_e):
        """Returns the temperature index closest to a particular
        temperature."""
        T_e_array = self._temperature_grid

        # Check the temperature range
        T_e_grid_max = np.amax(T_e_array)
        T_e_grid_min = np.amin(T_e_array)

        if (T_e >= T_e_grid_max):
            warnings.warn('Temperature reaches/exceeds the Temperature grid Boundary: Temperature index will be reset to {:}'.format(self._ntemp-1), UserWarning)
            return self._ntemp-1
        if (T_e <= T_e_grid_min):
            warnings.warn('Temperature reaches/exceeds the Temperature grid Boundary: Temperature index will be reset to {:}'.format(0), UserWarning)
            return 0

        # TODO: Add a test to check that the temperature grid is monotonic

        res = np.where(T_e_array >= T_e)
        res_ind = res[0]
        index = res_ind[0]
        dte_l = abs(T_e - T_e_array[index - 1])  # re-check the neighbor point
        dte_r = abs(T_e - T_e_array[index])
        if (dte_l <= dte_r):
            index = index - 1
        return index

    @property
    def temperature(self):
        """Returns the electron temperature currently in use by this class,
        or None if the temperature has not been set."""
        return self._temperature

    @temperature.setter
    def temperature(self, T_e):
        """Sets the electron temperature and index on the temperature grid
        to be used by this class"""
        # TODO: Add checks for the temperature
        self._temperature = T_e
        self._index = self._get_temperature_index(T_e)

    @property
    def temperature_grid(self):
        """Returns the grid of temperatures corresponding to the eigendata."""
        return self._temperature_grid

    @property
    def eigenvalues(self):
        """Returns the eigenvalues for the ionization and recombination
        rates for the temperature specified in the class."""
        if self.temperature:
            return self._eigenvalues[self._te_index, :]
        else:
            raise AttributeError("The temperature has not been set.")

    @property
    def eigenvectors(self):
        """Returns the eigenvectors for the ionization and recombination
        rates for the temperature specified in the class."""
        if self.temperature:
            return self._eigenvectors[self._te_index, :, :]
        else:
            raise AttributeError("The temperature has not been set.")

    @property
    def eigenvector_inverses(self):
        """Returns the inverses of the eigenvectors for the ionization and
        recombination rates for the temperature specified in the class."""
        if self.temperature:
            return self._eigenvector_inverses[self._te_index, :, :]
        else:
            raise AttributeError("The temperature has not been set.")

    @property
    def equilibrium_state(self):
        """Returns the equilibrium charge state distribution for the
        temperature specified in the class."""
        if self.temperature:
            return self._equilibrium_states[self._te_index, :]
        else:
            raise AttributeError("The temperature has not been set.")

    def _function_eqi(self, ioniz_rate, recomb_rate, natom):
        """Compute the equilibrium charge state distribution for the
        temperature specified using ionization and recombinaiton rates."""
        nstates = natom + 1
        conce = np.zeros(nstates)
        f = np.zeros(nstates + 1)
        c = np.zeros(nstates + 1)
        r = np.zeros(nstates + 1)

        # The start index is 1.
        for i in range(nstates):
            c[i+1] = ioniz_rate[i]
            r[i+1] = recomb_rate[i]

        # Set f1
        f[1] = 1.0
        # f2 = c1*f1/r2
        f[2] = c[1]*f[1]/r[2]
        #
        # For Hydrogen, the following loop is not necessary.
        #
        if (natom <= 1):
            f[1] = 1.0/(1.0 + c[1]/r[2])
            f[2] = c[1]*f[1]/r[2]
            conce[0:1] = f[1:2]
            return conce

        #
        # For other elements with atomic number >= 2:
        #
        # f(i+1) = -(c(i-1)*f(i-1) - (c(i)+r(i)*f(i)))/r(i+1)
        for k in range (2,natom):
            f[k+1] = (-c[k-1]*f[k-1] + (c[k]+r[k])*f[k])/r[k+1]

        # f(natom+1) = c(natom)*f(natom)/r(natom+1)
        f[natom+1] = c[natom]*f[natom]/r[natom+1]
        # f1 = 1/sum(f(*))
        f[1] = 1.0/np.sum(f)
        # f2 = c1*f1/r2
        f[2] = c[1]*f[1]/r[2]
        # f(i+1) = -(c(i-1)*f(i-1) - (c(i)+r(i)*f(i)))/r(i+1)
        for k in range(2,natom):
            f[k+1] = (-c[k-1]*f[k-1] + (c[k]+r[k])*f[k])/r[k+1]

        # f(natom+1) = c(natom)*f(natom)/r(natom+1)
        f[natom+1] = c[natom]*f[natom]/r[natom+1]
        #
        conce[0:nstates] = f[1:nstates+1]
        return conce
