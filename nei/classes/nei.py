import numpy as np
import matplotlib.pyplot as plt
from typing import Union, Optional, List, Dict, Callable
import astropy.units as u
import plasmapy as pl
import collections
from scipy import interpolate
from .eigenvaluetable import EigenData2


class NEIError(Exception):
    pass


def _get_electron_density(ionic_fractions, abundances, n_H):
    try:
        ...

    except Exception:
        raise ValueError("Unable to get electron density")


class Results:
    """Contains results from a non-equilibrium ionization simulation."""

    def __init__(self, initial_states, max_steps=1000):

        self.times = np.ndarray((max_steps)) * u.s
        self.T_e = np.ndarray((max_steps)) * u.K
        self.n_e = np.ndarray((max_steps)) * u.m ** -3

        self._ionic_fractions = {}
        self._number_densities = {}
        for element in initial_states.elements:
            nstates = pl.atomic.atomic_number(element) + 1
            self.ionic_fractions[element] = np.full((nstates, max_steps), np.nan)
            self.number_densities[element] = np.full((nstates, max_steps), np.nan) * u.m ** -3

            #print(self.ionic_fractions[element])
            print(initial_states.ionic_fractions)

            self._ionic_fractions[element][:,0] == initial_states.ionic_fractions[element][:]

        # TODO: Add initial ionic fractions and number densities

    @property
    def T_e(self):
        return self._T_e

    @property
    def n_e(self):
        return self._n_e

    @property
    def ionic_fractions(self):
        return self._ionic_fractions

class Results2:

    def __init__(self, initial, max_steps=1000):

        elements = initial.elements
        abundances = initial.abundances

        self._ionic_fractions = {
            elem: np.full((nstates[elem], max_steps), np.nan, dtype=np.float64)
            for elem in elements
        }

        self._n_elem = {elem: np.full(max_steps, np.nan) * u.cm ** -3 for elem in elements}



    @property
    def ionic_fractions(self):
        return self._ionic_fractions

    @property
    def n_elem(self):
        return self._n_elem

    @property
    def n_e(self):
        return self._n_e



class NEI:
    r"""
    Perform and analyze a non-equilibrium ionization simulation.

    Parameters
    ----------
    inputs

    T_e: `~astropy.units.Quantity` or `callable`
        The electron temperature, which may be a constant

    n_H: `~astropy.units.Quantity`
        The initial number density of hydrogen (including protons and
        neutrals).

    scaling_factor: `~astropy.units.Quantity` or `callable`
        The density scaling factor

    time

    abundances

    number_densities

    Examples
    --------

    >>> import numpy as np
    >>> import astropy.units as u

    >>> inputs = {'H': [0.9, 0.1], 'He': [0.9, 0.099, 0.001]}
    >>> n_H = 1e9 * u.m ** -3
    >>> abundances = {'H': 1, 'He': 0.085}
    >>> T_e = np.array([5000, 50000]) * u.K
    >>> scale_factor = [1.0, 0.1]
    >>> time_input = np.array([0, 10]) * u.min

    The initial conditions can be accessed using the initial attribute.

    #>>> nei.initial['H']

    After having inputted all of the necessary information, we can run
    the simulation.

    #>>> nei.simulate()

    The final results can be access with the `final` attribute.

    #>>> nei.final['H']
    #array([0.0, 1.0])
    #>>> nei.final.T_e
    #<Quantity 50000. K>

    """

    def __init__(
            self,
            inputs,
            abundances: Union[Dict, str] = None,
#            number_densities: u.Quantity = None,
            T_e: Union[Callable, u.Quantity] = None,
            n_H: Union[Callable, u.Quantity] = None,
#            scaling_factor: Union[Callable, np.ndarray] = None,
            time_input: u.Quantity = None,
            time_start: Optional[u.Quantity] = None,
            time_max: Optional[u.Quantity] = None,
            max_steps: Union[int, np.integer] = 1000,
            tol = 1e-15,
    ):

        try:

            self.time_input = time_input
            self.time_start = time_start
            self.time_max = time_max
            self.T_e_input = T_e
            self.n_H_input = n_H
            self.max_steps = max_steps

            T_e_init = self.electron_temperature(self.time_start)
            n_H_init = self.hydrogen_number_density(self.time_start)

            self.initial = pl.atomic.IonizationStates(
                inputs=inputs,
                abundances=abundances,
                T_e=T_e_init,
                n_H=n_H_init,
                tol = tol
            )

            self.tol = tol
            self.elements = self.initial.elements

            if 'H' not in self.elements:
                raise NEIError("Must have H in elements")

            self.abundances = self.initial.abundances

            self._EigenDataDict = {element: EigenData2(element) for element in self.elements}

            if self.T_e_input is not None and not isinstance(inputs, dict):
                for element in self.initial.elements:
                    self.initial.ionic_fractions[element] = \
                        self.EigenDataDict[element].equilibrium_state(T_e_init.value)

        except Exception:
            raise NEIError(
                f"Unable to create NEI instance for:\n"
                f"     inputs = {inputs}\n"
                f" abundances = {abundances}\n"
                f"        T_e = {T_e}\n"
                f"        n_H = {n_H}\n"
                f" time_input = {time_input}\n"
                f" time_start = {time_start}\n"
                f"   time_max = {time_max}\n"
                f"  max_steps = {max_steps}\n"
            )

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = elements

    @property
    def abundances(self):
        return self._abundances

    @abundances.setter
    def abundances(self, abund):
        self._abundances = abund

    @property
    def tol(self):
        return self._tol

    @tol.setter
    def tol(self, value):
        self._tol = value

    @property
    def time_input(self):
        return self._time_input

    @time_input.setter
    def time_input(self, times):
        if times is None:
            self._time_input = None
        elif isinstance(times, u.Quantity):
            if times.isscalar:
                raise ValueError("time_input must be an array")
            try:
                times = times.to(u.s)
            except u.UnitConversionError:
                raise u.UnitsError("time_input must have units of seconds") from None
            if not np.all(times[1:] > times[:-1]):
                raise ValueError("time_input must monotonically increase")
            self._time_input = times
        else:
            raise TypeError("Invalid time_input.")

    @property
    def time_start(self):
        return self._time_start

    @time_start.setter
    def time_start(self, time):
        if time is None:
            self._time_start = 0.0 * u.s
        elif isinstance(time, u.Quantity):
            if not time.isscalar:
                raise ValueError("time_start must be a scalar")
            try:
                time = time.to(u.s)
            except u.UnitConversionError:
                raise u.UnitsError("time_start must have units of seconds") from None
            if hasattr(self, '_time_max') \
                    and self._time_max is not None and self._time_max<=time:
                raise ValueError("time_start must be less than time_max")
            if self.time_input is not None and self.time_input.min() > time:
                raise ValueError("time_start must be less than min(time_input)")
            self._time_start = time
        else:
            raise TypeError("Invalid time_start.") from None

    @property
    def time_max(self):
        return self._time_max

    @time_max.setter
    def time_max(self, time):
        if time is None:
            self._time_max = None
#        if time is None:
#            if self.time_input is not None:
#                self._time_max = self.time_input[-1]
#            else:
#                self._time_max = None
        elif isinstance(time, u.Quantity):
            if not time.isscalar:
                raise ValueError("time_max must be a scalar")
            try:
                time = time.to(u.s)
            except u.UnitConversionError:
                raise u.UnitsError("time_max must have units of seconds") from None
            if hasattr(self, '_time_start') and self._time_start is not None and \
                    self._time_start >= time:
                raise ValueError("time_max must be greater than time_start")
            self._time_max = time
        else:
            raise TypeError("Invalid time_max.") from None

    @property
    def max_steps(self):
        return self._max_steps

    @max_steps.setter
    def max_steps(self, n):
        if isinstance(n, (int, np.integer)) and n > 0:
            self._max_steps = n
        else:
            raise TypeError("max_steps must be an integer")

    @property
    def T_e_input(self):
        return self._T_e_input

    @T_e_input.setter
    def T_e_input(self, T_e: Optional[Union[Callable, u.Quantity]]):
        """Set the input electron temperature."""
        if isinstance(T_e, u.Quantity):
            try:
                T_e = T_e.to(u.K, equivalencies=u.temperature_energy())
            except u.UnitConversionError:
                raise u.UnitsError("Invalid electron temperature.") from None
            if T_e.isscalar:
                self._T_e_input = T_e
                self._electron_temperature = lambda time: T_e
            else:
                if self._time_input is None:
                    raise TypeError("Must define time_input prior to T_e for an array.")
                time_input = self.time_input
                if len(time_input) != len(T_e):
                    raise ValueError("len(T_e) is not equal to len(time_input).")
                f = interpolate.interp1d(time_input.value, T_e.value)
                self._electron_temperature = lambda time: f(time.value) * u.K
                self._T_e_input = T_e
        elif callable(T_e):
            if self.time_start is not None:
                try:
                    T_e(self.time_start).to(u.K)
                    T_e(self.time_max).to(u.K)
                except Exception:
                    raise ValueError("Invalid electron temperature function.")
            self._T_e_input = T_e
            self._electron_temperature = T_e
        elif T_e is None:
            self._electron_temperature = lambda: None
        else:
            raise TypeError("Invalid T_e")

    def electron_temperature(self, time):
        try:
            time = time.to(u.s)
        except (AttributeError, u.UnitsError):
            raise NEIError("Invalid time in electron_temperature.")
        return self._electron_temperature(time).to(u.K)


    @property
    def n_H_input(self) -> u.Quantity:
        """The hydrogen number density."""
        if 'H' in self.elements:
            return self._n_H_input
        else:
            raise ValueError

    @n_H_input.setter
    def n_H_input(self, n_H):
        if isinstance(n_H, u.Quantity):
            try:
                n_H = n_H.to(u.cm ** -3)
            except u.UnitConversionError:
                raise u.UnitsError("Invalid hydrogen density.")
            if n_H.isscalar:
                self._n_H_input = n_H
                self.hydrogen_number_density = lambda time: n_H
            else:
                if self._time_input is None:
                    raise TypeError("Must define time_input prior to n_H for an array.")
                time_input = self.time_input
                if len(time_input) != len(n_H):
                    raise ValueError("len(n_H) is not equal to len(time_input).")
                f = interpolate.interp1d(time_input.value, n_H.value)
                self._hydrogen_number_density = lambda time: f(time.value) * u.cm ** -3
                self._n_H_input = n_H
        elif callable(n_H):
            if self.time_start is not None:
                try:
                    n_H(self.time_start).to(u.cm ** -3)
                    n_H(self.time_max).to(u.cm ** -3)
                except Exception:
                    raise ValueError("Invalid hydrogen number density function.")
            self._n_H_input = n_H
            self._hydrogen_number_density = n_H
        elif n_H is None:
            self._hydrogen_number_density = lambda: None
        else:
            raise TypeError("Invalid n_H.")

    def hydrogen_number_density(self, time):
        try:
            time = time.to(u.s)
        except (AttributeError, u.UnitsError):
            raise NEIError("Invalid time in hydrogen_density")
        return self._hydrogen_number_density(time)

    @property
    def EigenDataDict(self):
        return self._EigenDataDict

    @EigenDataDict.setter
    def EigenDataDict(self):
        self._EigenDataDict = {element: EigenData2(element) for element in self.elements}

    @property
    def initial(self) -> pl.atomic.IonizationStates:
        """
        The ~plasmapy.atomic.IonizationStates instance representing the
        initial conditions of the simulation.
        """
        return self._initial

    @initial.setter
    def initial(self, initial_states: Optional[pl.atomic.IonizationStates]):
        if isinstance(initial_states, pl.atomic.IonizationStates):
            self._initial = initial_states
            self._elements = initial_states.elements
        elif initial_states is None:
            self._ionstates = None
        else:
            raise TypeError("Expecting an IonizationStates instance.")

    def equilibrate(self, T_e=None):
        if T_e is None:
            T_e = self.T_e_input

        try:
            T_e = T_e.to(u.K)
        except Exception:
            raise ValueError

        self._initial.ionic_fractions = {
            element: self.EigenDataDict[element].equilibrium_state(T_e)
        }
        pass

    @property
    def results(self):
        try:
            return self._results
        except Exception:
            raise AttributeError("The simulation has not yet been performed.")

    @results.setter
    def results(self, value):
        if isinstance(value, Results):
            self._results = value
        else:
            raise TypeError

    @property
    def final(self):
        try:
            return self._final
        except Exception:
            raise AttributeError("The simulation has not yet been performed.")

    def _initialize_simulation(self):

        self._results = Results(
            initial_states=self.initial,
            max_steps=self.max_steps,
        )

    def _finalize_simulation(self):
        ...

    def simulate(self):
        """
        Perform a non-equilibrium ionization simulation.
        """

        # Preliminaries to shorten code

        elements = self.elements
        max_steps = self.max_steps
        nstates = {elem: pl.atomic.atomic_number(elem) + 1 for elem in elements}

        # Set up all of the dictionaries and arrays that will be used to
        # store the results

        ionic_fractions = {
            elem: np.full((nstates[elem], max_steps), np.nan, dtype=np.float64)
            for elem in elements
        }

        number_densities = {
            elem: np.full((nstates[elem], max_steps), np.nan) * u.cm ** -3
            for elem in elements
        }

        n_elem = {elem: np.full(max_steps, np.nan) * u.cm ** -3 for elem in elements}
        n_H = self._n_H_input  # assume constant for now
        n_e = np.full(max_steps, np.nan) * u.cm ** -3
        T_e = np.full(max_steps, np.nan) * u.K
        time = np.full(max_steps, np.nan) * u.s

        # We will need the abundances relative to hydrogen in order to
        # calculate element number densities relative to hydrogen's
        # number density.

        relative_abundances = {
            elem: self.abundances[elem] / self.abundances['H']
            for elem in elements
        }

        # Set the initial conditions

        time[0] = self.time_start
        for elem in elements:
            ionic_fractions[elem][:, 0] = self.initial.ionic_fractions[elem]
            number_densities[elem][:, 0] = \
                self.hydrogen_number_density(self.time_start) \
                * relative_abundances[elem] \
                * ionic_fractions[elem][:, 0]


        # Do the time advance


        for step in range(max_steps):



            T_e[step] = self.electron_temperature(time[step])



        print(T_e)


        def time_advance(
                self,
                dt=None,
                T_e=None,
        ):



            # Calculate the temperature index
            #
            #        index = ...
            #        for element in self.elements:
            #            self.EigenDataDict[element][index]

            raise NotImplementedError

        # ------------------------------------------------------------------------------
        # function: Time-Advance solover
        # ------------------------------------------------------------------------------
        # def func_solver_eigenval(natom, te, ne, dt, f0, table):
        #    """
        #        The testing function for performing time_advance calculations.
        #    """

        # !! Change the following to use table.eigen*(T_e=...)

        #    table.temperature = te
        #    evals = table.eigenvalues  # find eigenvalues on the chosen Te node
        #    evect = table.eigenvectors
        #    evect_invers = table.eigenvector_inverses

        #    # define the temperary diagonal matrix
        #    diagona_evals = np.zeros((natom + 1, natom + 1))
        #    for ii in range(0, natom + 1):
        #        diagona_evals[ii, ii] = np.exp(evals[ii] * dt * ne)

        #    # matirx operation
        #    matrix_1 = np.dot(diagona_evals, evect)
        #    matrix_2 = np.dot(evect_invers, matrix_1)

        #    # get ions fraction at (time+dt)
        #    ft = np.dot(f0, matrix_2)

        #    # re-check the smallest value
        #    minconce = 1.0e-15
        #    for ii in np.arange(0, natom + 1, dtype=np.int):
        #        if (abs(ft[ii]) <= minconce):
        #            ft[ii] = 0.0
        #    return ft

    def save(self, filename="nei.h5"):
        ...
