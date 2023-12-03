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
    q_0 = (
          (g + np.power(g,9) + np.power(g,25) + np.power(g,49) + np.power(g,81) + np.power(g,121) + np.power(g,169))
        / (1 + 2 * (np.power(g,4) + np.power(g,16) + np.power(g,36) + np.power(g,64) + np.power(g,100) + np.power(g,144)))
    )

    xi = 1 / np.sqrt(1 - np.power((1-2*q_0)/(1+2*q_0),4))
    return xi

def emqf_analog_lowpass(N, xi, f3db=False):
    """
    Compute analog EMQF filter prototype in z,p,k format.

    Parameters
    ----------
    N : int
        The order of the filter.
    xi : float
        Selectivity factor xi. See also `emqf_selectivity_factor()`
    f3db : bool
        The filter is normalized such that the gain magnitude is -3 dB at angular frequency 1.

    Returns
    -------
    z, p, k : ndarray, ndarray, float
        Zeros, poles, and system gain of the IIR filter transfer
        function.

    Notes
    -----
    Filter design steps according to
    M. D. Lutovac's Book "Filter Design for Signal Processing" (2000)
    9.7.2 Elliptic Minimal Q-Factor Transfer Functions, Design of
        Half-Band IIR Filters for Given Passband or Stopband Attenuation
    """
    raise NotImplementedError

if __name__ == '__main__':
    #__test_emqf_selectivity_factor()
    pass
    N = 5
    xi = emqf_selectivity_factor(N=N,As=50)
    r = getEMQFAnalogFilterBySelectivityFactor(n=N, xi=xi)
    print(r)
