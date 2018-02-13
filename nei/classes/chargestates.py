import numpy as np

import astropy.units as u

class ChargeStates:
    r""""""
    def __init__(self, element='Fe'):

        _atomic_number = 26

        self._n_e = 1e9 * u.cm ** -3
        self._T_e = 1e6 * u.K

        self._charge_states = np.zeros(_atomic_number + 1)

    def __str__(self):
        ...

    def __repr__(self):
        ...

    def ionization_equilibrium(self):
        ...

    @property
    def charge_states(self):
        return self._charge_states

