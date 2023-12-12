import unittest
import helpers

import numpy as np
from filterdesign import filterutils


class Test_Filterutils_Cascade_Zpk(unittest.TestCase):
    TEST_SET = [
        {
            "args": [np.array([1j]), np.array([1j, 2 + 3j]), 12],
            "expected_result": True,
        },
        {
            "args": [np.array([1j]), np.array([1j, 2 + 3j]), 12j],
            "expected_result": True,
        },
        {"args": [], "expected_result": False},
        {
            "args": [1j, 2j, 12],
            "expected_result": False,
        },
        {
            "args": [np.array([1j])],
            "expected_result": False,
        },
        {
            "args": [np.array([1j]), np.array([1j, 2 + 3j])],
            "expected_result": False,
        },
        {
            "args": [1j, np.array([1j, 2 + 3j]), 12],
            "expected_result": False,
        },
        {
            "args": [np.array([1j, 2 + 3j]), 1j, 12],
            "expected_result": False,
        },
        {
            "args": [np.array([1j]), 2j, np.array([12])],
            "expected_result": False,
        },
        {
            "args": [1j, np.array([1j, 2 + 3j]), np.array([12])],
            "expected_result": False,
        },
        {
            "args": [np.array([1j]), np.array([1j, 2 + 3j]), np.array([12])],
            "expected_result": False,
        },
    ]

    def test_is_zpk_format(self):
        # helpers.list_1d_almost_equal(self, np.linspace(1, 10), np.linspace(1, 11))

        for test_data in __class__.TEST_SET:
            result = filterutils._is_zpk_format(test_data["args"])
            self.assertEqual(test_data["expected_result"], result)


class Test_Filterutils_Cascade_Sos(unittest.TestCase):
    TEST_SET = [
        {
            "args": np.ones((1, 6)),
            "expected_result": True,
        },
        {
            "args": np.ones((5, 6)),
            "expected_result": True,
        },
        {
            "args": np.ones((1, 6), dtype=np.cfloat),
            "expected_result": True,
        },
        {
            "args": np.ones((5, 6), dtype=np.cfloat),
            "expected_result": True,
        },
        {
            "args": np.ones((1, 7)),
            "expected_result": False,
        },
        {
            "args": np.ones((1, 5)),
            "expected_result": False,
        },
        {
            "args": np.ones((6, 1)),
            "expected_result": False,
        },
        {
            "args": 1.0,
            "expected_result": False,
        },
        {
            "args": [],
            "expected_result": False,
        },
        {
            "args": np.ones((6,)),
            "expected_result": False,
        },
    ]

    def test_is_so_format(self):
        for test_data in __class__.TEST_SET:
            result = filterutils._is_sos_format(test_data["args"])
            self.assertEqual(test_data["expected_result"], result)


class Test_Filterutils_Cascade_Main(unittest.TestCase):
    def cascade_zpk(self, cascade_func):
        zpk_a = [np.array([1 + 1j, 2 + 2j]), np.array([11 + 11j, 22 + 22j]), 1.0]
        zpk_b = [np.array([3 + 3j]), np.array([33 + 33j, 44 + 44j]), 0.5]
        zpk_expected = [
            np.array([1 + 1j, 2 + 2j, 3 + 3j]),
            np.array([11 + 11j, 22 + 22j, 33 + 33j, 44 + 44j]),
            0.5,
        ]

        zpk_actual = cascade_func(zpk_a, zpk_b)
        helpers.list_1d_almost_equal(self, zpk_actual[0], zpk_expected[0])
        helpers.list_1d_almost_equal(self, zpk_actual[1], zpk_expected[1])
        self.assertAlmostEqual(zpk_expected[2], zpk_actual[2])

    def test_cascade_zpk(self):
        self.cascade_zpk(cascade_func=filterutils._cascade_zpk_pair)

    def test_cascade_zpk_public(self):
        self.cascade_zpk(cascade_func=filterutils.cascade)

    def cascade_sos(self, cascade_func):
        sos_a = np.array([[1.0] * 6, [2.0] * 6])
        sos_b = np.array([[3.0] * 6, [4.0] * 6, [5.0] * 6])
        sos_expected = np.array([[1.0] * 6, [2.0] * 6, [3.0] * 6, [4.0] * 6, [5.0] * 6])

        sos = cascade_func(sos_a, sos_b)
        self.assertEqual(sos_expected.shape, sos.shape)
        helpers.list_1d_almost_equal(self, sos_expected.flatten(), sos.flatten())

    def test_cascade_sos(self):
        self.cascade_sos(cascade_func=filterutils._cascade_sos_pair)

    def test_cascade_sos_public(self):
        self.cascade_sos(cascade_func=filterutils.cascade)


if __name__ == "__main__":
    unittest.main()
