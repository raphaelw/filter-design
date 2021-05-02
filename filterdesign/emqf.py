from __future__ import division
from __future__ import with_statement

import math

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

    L = pow(10, a_s/10) - 1
    t = 0.5 * ((1 - pow( 1-(1/(L**2)), 1/4)) / (1 + pow( 1-(1/(L**2)) ,1/4)))
    q = t + 2*pow(t,5) + 15*pow(t,9) + 150*pow(t,13)
    g = math.exp(math.log(q)/N) # natural logarithm
    q_0 = (g + pow(g,9) + pow(g,25) + pow(g,49) + pow(g,81) + pow(g,121) + pow(g,169)) / (1 + 2 * (pow(g,4) + pow(g,16) + pow(g,36) + pow(g,64) + pow(g,100) + pow(g,144)))

    xi = 1 / math.sqrt(1 - pow((1-2*q_0)/(1+2*q_0),4))
    return xi

if __name__ == '__main__':
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