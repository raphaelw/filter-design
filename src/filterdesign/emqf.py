from __future__ import division
from __future__ import with_statement

import numpy as np
from scipy.special import ellipk, ellipj
from scipy.signal import freqs_zpk


def selectivity_factor(N: int, stopband_attenuation: float):
    """
    Compute the selectivity factor (xi) for the EMQF filter of order N
    and stopband attenuation As.

    Parameters
    ----------
    N : int
        The order of the filter.
    stopband_attenuation : float
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
    a_s = float(stopband_attenuation)

    L = np.power(10.0, a_s / 10) - 1
    t = 0.5 * (
        (1 - np.power(1 - (1 / np.power(L, 2)), 1 / 4))
        / (1 + np.power(1 - (1 / np.power(L, 2)), 1 / 4))
    )
    q = t + 2 * np.power(t, 5) + 15 * np.power(t, 9) + 150 * np.power(t, 13)
    g = np.exp(np.log(q) / N)  # natural logarithm

    # fmt: off
    q_0 = (
          (g + np.power(g,9) + np.power(g,25) + np.power(g,49) + np.power(g,81) + np.power(g,121) + np.power(g,169))
        / (1 + 2 * (np.power(g,4) + np.power(g,16) + np.power(g,36) + np.power(g,64) + np.power(g,100) + np.power(g,144)))
    )
    # fmt: off

    xi = 1 / np.sqrt(1 - np.power((1-2*q_0)/(1+2*q_0),4))
    return xi


def _X(N, xi, i):
    """i'th zero of elliptic rational function"""
    N = int(N)
    xi = float(xi)
    i = int(i)

    order_is_odd = (N % 2) == 1

    if order_is_odd and i == (N + 1) // 2:
        return 0.0

    k = 1 / xi
    m = k**2  # modulus m = k^2
    u = ((2.0 * float(i) - 1.0) / float(N)) * ellipk(m)

    # according to https://en.wikipedia.org/wiki/Jacobi_elliptic_functions#Minor_functions
    # the following relationship can be used cd() = cn()/dn()
    sn, cn, dn, ph = ellipj(u, m)
    cd = cn / dn
    return -cd


def emqf_analog_prototype_from_selectivity_factor(
    N: int, xi: float, f3db: bool = False
):
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
    6.3.4 Zeros, Poles and Q-Factors
    6.3.5 Discrimination Factor, Elliptic Rational Function, and Characteristic Function
    6.3.6 Normalized Lowpadd Elliptic Transfer Function
    12.11 Elliptic Filters With Minimal Q-Factors
    """
    N = int(N)
    xi = float(xi)
    f3db = bool(f3db)

    assert N > 0
    order_is_odd = (N % 2) == 1

    zeros, poles = list(), list()

    up_to_including = N // 2
    for i in range(1, up_to_including + 1):
        X = _X(N=N, xi=xi, i=i)

        nominator_re = -np.sqrt(1.0 - np.power(X, 2)) * np.sqrt(
            np.power(xi, 2) - np.power(X, 2)
        )
        nominator_im = X * (xi + 1.0)
        nominator = complex(nominator_re, nominator_im)

        denominator = xi + np.power(X, 2)

        S_minQ = np.sqrt(xi) * (nominator / denominator)

        H_pole = S_minQ
        H_zero = complex(0, 1) * xi / X  # transfer function zero (Eq 12.373)
        if f3db:
            H_pole /= np.sqrt(xi)
            H_zero /= np.sqrt(xi)

        poles.append(H_pole)
        poles.append(H_pole.conjugate())
        zeros.append(H_zero)
        zeros.append(H_zero.conjugate())

    if order_is_odd:
        # add first order section. note that it has a zero at infinity
        H_pole = -1.0 if f3db else -np.sqrt(xi)
        poles.append(H_pole)

    z = np.array(zeros, dtype=complex)
    p = np.array(poles, dtype=complex)
    k = 1.0  # preliminary

    # compte gain factor
    f3db_location = 1.0 if f3db else np.sqrt(xi)
    w, h = freqs_zpk(z, p, k, [f3db_location])
    k *= 1.0 / abs(h[0]) * (1.0 / np.sqrt(2))

    return z, p, k


def emqfap(N: int, stopband_attenuation: float = 60, f3db: bool = False):
    """
    Return (z,p,k) for an analog prototype EMQF filter of Nth-order.

    Parameters
    ----------
    N : int
        The order of the filter.
    stopband_attenuation : float
        Stopband attenuation given in dB as a positive number.
    f3db : bool
        The filter is normalized such that the gain magnitude is -3 dB at angular frequency 1.
        Otherwise, the filter is normalized to the passband edge frequency.

    Returns
    -------
    z, p, k : ndarray, ndarray, float
        Zeros, poles, and system gain of the IIR filter transfer
        function.
    """
    xi = selectivity_factor(N=N, stopband_attenuation=stopband_attenuation)
    return emqf_analog_prototype_from_selectivity_factor(N=N, xi=xi, f3db=f3db)
