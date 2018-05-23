import astropy.units as u
from plasmapy.atomic import IonizationState, IonizationStates
from ..nei import NEI
import numpy as np
import pytest

tests = {

    'basic': {
        'inputs': {'H': [0.9, 0.1], 'He': [0.5, 0.3, 0.2]},
        'abundances': {'H': 1, 'He': 0.1},
        'T_e': np.array([1e4, 6e4]) * u.K,
        'n_H': 1e15 * u.m ** -3,
        'time_input': np.array([0, 1000]) * u.s,
        'time_start': 0 * u.s,
        'time_max': 800 * u.s,
        'max_steps': 10,
    },

}

test_names = tests.keys()


class TestNEI:

    @pytest.mark.parametrize('test_name', test_names)
    def test_instantiate_NEI(self, test_name):
        try:
            instance = NEI(**tests[test_name])
        except Exception:
            raise Exception(f"Problem with test {test_name}")

        assert isinstance(instance.initial, IonizationStates)
        assert isinstance(instance.abundances, dict)
        assert isinstance(instance.T_e_input, u.Quantity)
        assert isinstance(instance.n_H, u.Quantity)
        assert isinstance(instance.time_input, u.Quantity)

        instance._initialize_simulation()

#    @pytest.mark.parametrize('test_name', tests_names)
#    def test_initialize_simulation(self, test_name):
#        try:
#            self.instan
