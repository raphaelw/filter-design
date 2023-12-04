import unittest

# import numpy.testing as npt

import numpy as np
import emqf


def _complex_sort_keyfunc(complex_num):
    """Sort by real part then by imag part"""
    c = complex(complex_num)
    return c.real, c.imag


class TestSelectivityFactor(unittest.TestCase):
    TEST_SET = [
        {"kwargs": {"N": 2, "As": 25}, "verified_result": 8.90548901417296},
        {"kwargs": {"N": 3, "As": 10}, "verified_result": 1.13665205003484},
        {"kwargs": {"N": 4, "As": 20}, "verified_result": 1.34389234722479},
        {"kwargs": {"N": 5, "As": 50}, "verified_result": 3.37476179496728},
        {"kwargs": {"N": 7, "As": 55.55}, "verified_result": 2.02763195794622},
    ]

    def test_input_output(self):
        for t in __class__.TEST_SET:
            kwargs = t["kwargs"]
            verified_result = t["verified_result"]
            xi = emqf.emqf_selectivity_factor(**kwargs)
            self.assertAlmostEqual(xi, verified_result, places=5)


class TestAnalogLowpass(unittest.TestCase):
    # TODO: add even order test data
    # TODO: add data for gain (=k)
    TEST_SET = [
        {
            "kwargs": dict(N=7, xi=2.20227264783, f3db=True),
            "verified_result": {
                "poles": [
                    -1.0,
                    (-0.7970176443524649 + 0.6039560204111288j),
                    (-0.7970176443524649 - 0.6039560204111288j),
                    (-0.43442506987734747 + 0.9007079763508602j),
                    (-0.43442506987734747 - 0.9007079763508602j),
                    (-0.13151338056090509 + 0.9913143955039907j),
                    (-0.13151338056090509 - 0.9913143955039907j),
                ],
                "zeros": [
                    # infinity
                    3.266758038863892j,
                    -3.266758038863892j,
                    1.8573266057528255j,
                    -1.8573266057528255j,
                    1.5180044036329923j,
                    -1.5180044036329923j,
                ],
            },
        },
        {
            "kwargs": dict(N=3, xi=1.13665205003484, f3db=True),
            "verified_result": {
                "poles": [
                    -1.0,
                    (-0.11853445445639667 + 0.992949939879511j),
                    (-0.11853445445639667 - 0.992949939879511j),
                ],
                "zeros": [
                    # infinity
                    1.144873078567662j,
                    -1.144873078567662j,
                ],
            },
        },
        {
            "kwargs": dict(N=3, xi=1.13665205003484, f3db=False),
            "verified_result": {
                "poles": [
                    -1.066138851198492,
                    (-0.12637418710158269 + 1.0586225082007534j),
                    (-0.12637418710158269 - 1.0586225082007534j),
                ],
                "zeros": [
                    # infinity
                    1.2205936687522079j,
                    -1.2205936687522079j,
                ],
            },
        },
    ]

    def test_output_types_and_shapes(self):
        for t in __class__.TEST_SET:
            kwargs = t["kwargs"]
            verified_result = t["verified_result"]
            z = verified_result["zeros"]
            p = verified_result["poles"]
            z_, p_, k_ = emqf.emqf_analog_lowpass(**kwargs)

            # types
            self.assertIsInstance(z_, np.ndarray)
            self.assertIsInstance(p_, np.ndarray)
            self.assertIsInstance(k_, float)

            # shapes
            self.assertTupleEqual(z_.shape, (len(z),))
            self.assertTupleEqual(p_.shape, (len(p),))

    def _almost_equal_complex_unsorted_lists(self, list_a, list_b, places=5):
        list_a = list( map(complex, list_a) )
        list_b = list( map(complex, list_b) )
        
        list_a = sorted(list_a, key=_complex_sort_keyfunc)
        list_b = sorted(list_b, key=_complex_sort_keyfunc)

        self.assertEqual(len(list_a), len(list_b))

        for a,b in zip(list_a, list_b):
            self.assertAlmostEqual(a,b,places=places)

    def test_input_output(self):
        for t in __class__.TEST_SET:
            kwargs = t["kwargs"]
            verified_result = t["verified_result"]
            z = verified_result["zeros"]
            p = verified_result["poles"]

            z_, p_, k_ = emqf.emqf_analog_lowpass(**kwargs)

            self._almost_equal_complex_unsorted_lists(z, z_, places=8)
            self._almost_equal_complex_unsorted_lists(p, p_, places=8)

            # TODO: test for gain (=k)



if __name__ == "__main__":
    unittest.main()
