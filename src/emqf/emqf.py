from __future__ import division
from __future__ import with_statement

import numpy as np

def emqf_selectivity_factor(N, As):
    """
    Compute the selectivity factor (xi) for the EMQF filter of order N
    and stopband attenuation As.

    Parameters
    ----------
    N : int
        The order of the filter.
    As : float
        Stopband attenuation given in dB as a positive number.

    Returns
    -------
    xi : float
        Selectivity factor.

    Notes
    -----
    Filter design steps according to
    M. D. Lutovac's Book "Filter Design for Signal Processing" (2000)
    9.7.2 Elliptic Minimal Q-Factor Transfer Functions, Design of
        Half-Band IIR Filters for Given Passband or Stopband Attenuation
    """
    N = int(N)
    a_s = float(As)

    L = np.power(10., a_s/10) - 1
    t = 0.5 * ((1 - np.power( 1-(1/(L**2)), 1/4)) / (1 + np.power( 1-(1/(L**2)) ,1/4)))
    q = t + 2*np.power(t,5) + 15*np.power(t,9) + 150*np.power(t,13)
    g = np.exp(np.log(q)/N) # natural logarithm
    q_0 = (g + np.power(g,9) + np.power(g,25) + np.power(g,49) + np.power(g,81) + np.power(g,121) + np.power(g,169)) / (1 + 2 * (np.power(g,4) + np.power(g,16) + np.power(g,36) + np.power(g,64) + np.power(g,100) + np.power(g,144)))

    xi = 1 / np.sqrt(1 - np.power((1-2*q_0)/(1+2*q_0),4))
    return xi

def __test_emqf_selectivity_factor():
    test_set = [
        {'kwargs' : {'N':2, 'As':25}, 'verified_result':8.90548901417296},
        {'kwargs' : {'N':3, 'As':10}, 'verified_result':1.13665205003484},
        {'kwargs' : {'N':4, 'As':20}, 'verified_result':1.34389234722479},
        {'kwargs' : {'N':5, 'As':50}, 'verified_result':3.37476179496728},
        {'kwargs' : {'N':7, 'As':55.55}, 'verified_result':2.02763195794622}
    ]

    print("Test: emqf_selectivity_factor")
    for test in test_set:
        kwargs = test['kwargs']
        verified_result = test['verified_result']
        xi = emqf_selectivity_factor(**kwargs)
        print(kwargs,'=> xi :', xi, '; difference', abs(xi-verified_result))

if __name__ == '__main__':
    __test_emqf_selectivity_factor()