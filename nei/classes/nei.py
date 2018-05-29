import numpy as np
import matplotlib.pyplot as plt
from typing import Union, Optional, List, Dict, Callable
import astropy.units as u
import plasmapy as pl
import collections
from scipy import interpolate
from .eigenvaluetable import EigenData2

class Results:
    """Contains results from a non-equilibrium ionization simulation."""
    def __init__(self, initial_states, max_steps=1000):

        self.times = np.ndarray((max_steps)) * u.s
        self.T_e = np.ndarray((max_steps)) * u.K
        self.n_e = np.ndarray((max_steps)) * u.m ** -3

        self.ionic_fractions = {}
        self.number_densities = {}
        for element in initial_states.elements:
            nstates = pl.atomic.atomic_number(element) + 1
            self.ionic_fractions[element] = np.full((nstates, max_steps), np.nan)
            self.number_densities[element] = np.full((nstates, max_steps), np.nan) * u.m ** -3

            #print(self.ionic_fractions[element])
            print(initial_states.ionic_fractions)

            self.ionic_fractions[element][:,0] == initial_states.ionic_fractions[element][:]

        # TODO: Add initial ionic fractions and number densities

class NEI:
    r"""
    Perform a non-equilibrium ionization simulation.

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

    #    >>> nei = NEI(inputs, T_e=T_e, n_H=n_H,scaling_factor=scale_factor, time_input=time_input)

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
            number_densities: u.Quantity = None,
            T_e: Union[Callable, u.Quantity] = None,
            n_H: Union[Callable, u.Quantity] = None,
            scaling_factor: Union[Callable, np.ndarray] = None,
            time_input: u.Quantity = None,
            time_start: Optional[u.Quantity] = None,
            time_max: Optional[u.Quantity] = None,
            max_steps: Union[int, np.integer] = 1000,
    ):

        self.time_input = time_input
        self.time_start = time_start
        self.time_max = time_max
        self.max_steps = max_steps
        self.T_e_input = T_e
        self.n_H = n_H  # finish implementing this  # have this be density normalization instead?
        self.abundances = abundances  # set this up
        self.number_densities = number_densities  # set this up  # as a function of time?
         # instead of scaling_factor, allow input of density vs. time
        self.scaling_factor = scaling_factor  # set this up

        try:
            T_e_init = self.electron_temperature(self.time_start)

        except Exception:
            raise ValueError(str(self.time_start))

        try:

            self.initial = pl.atomic.IonizationStates(
                inputs=inputs,
                abundances=abundances,
                T_e=T_e_init,
                n_H=n_H,
            )

            self._EigenDataDict = {element: EigenData2(element) for element in self.elements}

            for element in self.initial.elements:
                self.EigenDataDict[element].temperature = T_e_init.value
                self.initial.ionic_fractions[element] = self.EigenDataDict[element].eqi(T_e_init.value)

        except Exception:
            raise ValueError("Unable to create initial conditions.")

        try:
            self.elements = self.initial.elements
        except Exception:
            raise ValueError("Unable to set elements")

        try:

            self.abundances = self.initial.abundances
        except Exception:
            raise ValueError('Unable to set abundances')


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
            if self.time_input is not None:
                self._time_start = self.time_input[0]
            else:
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
            if self.time_input.min() > time:
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
            if self.time_input is not None:
                self._time_max = self.time_input[-1]
            else:
                self._time_max = None
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
            raise ValueError("Invalid time in electron_temperature.")
        return self._electron_temperature(time).to(u.K)

    @property
    def n_H(self):
        if 'H' in self.elements:
            return self._n_H
        else:
            raise ValueError

    @n_H.setter
    def n_H(self, n):
        if n is None:
            self._n_H = None
        elif isinstance(n, u.Quantity):
            try:
                self._n_H = n.to(u.m ** -3)
            except Exception:
                raise ValueError
        else:
            raise TypeError

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

    @property
    def results(self):
        try:
            return self._results
        except Exception:
            raise AttributeError("The simulation has not yet been performed.")

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
        """Perform a non-equilibrium ionization simulation."""

        self._initialize_simulation()

    def save(self, filename="nei.h5"):
        ...
