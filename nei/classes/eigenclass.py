from scipy.io import FortranFile
import numpy as np
import astropy.units as u
from .. import __path__


class EigenData:
    """A class to contain eigenvalue and eigenvector information on the
    ionization and recombination rates for an element."""

    def __init__(self, element='Fe', temperature=None):
        """Read in the """

        self._element = element
        self._temperature = temperature

        if self._temperature:
            self._index = self._get_temperature_index(temperature)

        data_dir = __path__[0] + '/data/eigenvaluetables/chianti8/'
        filename = data_dir + element.lower() + 'eigen.dat'
        eigenfile = FortranFile(filename, 'r')

        ntemp, atomic_numb = eigenfile.read_ints(np.int32)
        nstates = atomic_numb + 1

        self._ntemp = ntemp
        self._atomic_numb = atomic_numb
        self._nstates = nstates

        self._temperature_grid = eigenfile.read_reals(np.float64)

        self._equilibrium_states = \
            eigenfile.read_reals(np.float64).reshape((ntemp, nstates))

        self._eigenvalues = \
            eigenfile.read_reals(np.float64).reshape((ntemp, nstates))

        self._eigenvectors = \
            eigenfile.read_reals(np.float64).reshape(ntemp, nstates, nstates)

        self._eigenvector_inverses = \
            eigenfile.read_reals(np.float64).reshape(ntemp, nstates, nstates)

        self._ionization_rate = \
            eigenfile.read_reals(np.float64).reshape((ntemp, nstates))

        self._recombination_rate = \
            eigenfile.read_reals(np.float64).reshape((ntemp, nstates))

    def _get_temperature_index(self, T_e):
        """Returns the temperature index closest to a particular
        temperature."""
        T_e_array = self._temperature_grid
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
            return self._eigenvalues[self._index, :]
        else:
            raise AttributeError("The temperature has not been set.")

    @property
    def eigenvectors(self):
        """Returns the eigenvectors for the ionization and recombination
        rates for the temperature specified in the class."""
        if self.temperature:
            return self._eigenvectors[self._index, :, :]
        else:
            raise AttributeError("The temperature has not been set.")

    @property
    def eigenvector_inverses(self):
        """Returns the inverses of the eigenvectors for the ionization and
        recombination rates for the temperature specified in the class."""
        if self.temperature:
            return self.eigenvector_inverses[self._index, :, :]
        else:
            raise AttributeError("The temperature has not been set.")

    @property
    def equilibrium_state(self):
        """Returns the equilibrium charge state distribution for the
        temperature specified in the class."""
        if self.temperature:
            return self._equilibrium_states[self._index, :]
        else:
            raise AttributeError("The temperature has not been set.")
