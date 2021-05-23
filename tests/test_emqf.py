import unittest
#import numpy.testing as npt

from emqf.emqf import emqf_selectivity_factor

class TestSimple(unittest.TestCase):

    def test_emqf_selectivity_factor(self):
        test_set = [
            {'kwargs' : {'N':2, 'As':25}, 'verified_result':8.90548901417296},
            {'kwargs' : {'N':3, 'As':10}, 'verified_result':1.13665205003484},
            {'kwargs' : {'N':4, 'As':20}, 'verified_result':1.34389234722479},
            {'kwargs' : {'N':5, 'As':50}, 'verified_result':3.37476179496728},
            {'kwargs' : {'N':7, 'As':55.55}, 'verified_result':2.02763195794622}
        ]
        for t in test_set:
            kwargs = t['kwargs']
            verified_result = t['verified_result']
            xi = emqf_selectivity_factor(**kwargs)
            self.assertAlmostEqual(xi, verified_result, 5)


if __name__ == '__main__':
    unittest.main()
