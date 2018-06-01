import astropy.units as u
from ..ionization_states import IonizationStates, particle_symbol
from ..nei import NEI
import numpy as np
import pytest

inputs_dict = {'H': [0.9, 0.1], 'He': [0.5, 0.3, 0.2]}
abundances = {'H': 1, 'He': 0.1}

time_array = np.array([-3, 90]) * u.s
T_e_array = np.array([4e4, 6e4]) * u.K
n_H_array = np.array([1e9, 5e8]) * u.cm ** -3


tests = {

    'basic': {
        'inputs': inputs_dict,
        'abundances': abundances,
        'T_e': T_e_array,
        'n_H': n_H_array,
        'time_input': time_array,
        'time_start': 0 * u.s,
        'time_max': 800 * u.s,
        'max_steps': 5,
    },

    'T_e constant': {
        'inputs': inputs_dict,
        'abundances': abundances,
        'T_e': 1 * u.MK,
        'n_H': n_H_array,
        'time_input': time_array,
        'time_start': 0 * u.s,
        'time_max': 800 * u.s,
        'max_steps': 5,
    },

    'n_e constant': {
        'inputs': inputs_dict,
        'abundances': abundances,
        'T_e': T_e_array,
        'n_H': 1e9 * u.cm ** -3,
        'time_input': time_array,
        'time_start': 0 * u.s,
        'time_max': 800 * u.s,
        'max_steps': 5,
    },

    'T_e function': {
        'inputs': inputs_dict,
        'abundances': abundances,
        'T_e': lambda time: 1e4 * (1 + time/u.s) * u.K,
        'n_H': 1e15 * u.cm **-3,
        'time_max': 800 * u.s,
        'max_steps': 5,
    },

    'n_H function': {
        'inputs': inputs_dict,
        'abundances': abundances,
        'T_e': 6e4 * u.K,
        'n_H': lambda time: 1e9 * (1 + time/u.s) * u.cm ** -3,
        'time_start': 0 * u.s,
        'time_max': 800 * u.s,

    }

}

test_names = list(tests.keys())


class TestNEI:

    @classmethod
    def setup_class(cls):
        cls.instances = {}

    @pytest.mark.parametrize('test_name', test_names)
    def test_instantiate(self, test_name):
        try:
            instance = NEI(**tests[test_name])
            self.instances[test_name] = instance
        except Exception as exc:
            raise Exception(f"Problem with test {test_name}") from exc

    @pytest.mark.parametrize('test_name', test_names)
    def test_time_start(self, test_name):
        instance = self.instances[test_name]
        if 'time_start' in tests[test_name].keys():
            assert tests[test_name]['time_start'] == instance.time_start
        elif 'time_input' in tests[test_name].keys():
            assert tests[test_name]['time_input'].min() == instance.time_start
        else:
            assert instance.time_start == 0 * u.s

    @pytest.mark.parametrize('test_name', test_names)
    def test_time_max(self, test_name):
        instance = self.instances[test_name]
        if 'time_max' in tests[test_name].keys():
            assert tests[test_name]['time_max'] == instance.time_max

    @pytest.mark.parametrize('test_name', test_names)
    def test_initial_type(self, test_name):
        instance = self.instances[test_name]
        assert isinstance(instance.initial, IonizationStates)

    @pytest.mark.parametrize('test_name', test_names)
    def test_n_H_input(self, test_name):
        actual = self.instances[test_name].n_H_input
        expected = tests[test_name]['n_H']
        if isinstance(expected, u.Quantity) and not expected.isscalar:
            assert all(expected == actual)
        else:
            assert expected == actual

    @pytest.mark.parametrize('test_name', test_names)
    def test_T_e_input(self, test_name):
        actual = self.instances[test_name].T_e_input
        expected = tests[test_name]['T_e']
        if isinstance(expected, u.Quantity) and not expected.isscalar:
            assert all(expected == actual)
        else:
            assert expected == actual

    @pytest.mark.parametrize(
        'test_name',
        [test_name for test_name in test_names if isinstance(tests[test_name]['inputs'], dict)],
    )
    def test_initial_ionfracs(self, test_name):
        original_inputs = tests[test_name]['inputs']
        original_elements = original_inputs.keys()

        for element in original_elements:
            assert np.allclose(
                original_inputs[element],
                self.instances[test_name].initial.ionic_fractions[particle_symbol(element)]
            )

    @pytest.mark.parametrize('test_name', test_names)
    def test_simulate(self, test_name):
        instance = self.instances[test_name]
        try:
            instance.simulate()
        except Exception as exc:
            raise ValueError("Unable to simulate.") from exc

    # Test that ionization fractions that were calculated to be in
    # equilibrium remain in equilibrium after (1) a single long time
    # step, and (2) a bunch of smaller time steps.


class TestResults:

    @classmethod
    def setup_class(cls):
        cls.instances = {}

    def test_instantiation(self):
        ...