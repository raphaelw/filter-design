import numpy as np
from functools import reduce


def _is_zpk_format(zpk):
    if not len(zpk) == 3:
        return False

    zeros, poles, k = zpk
    if not isinstance(zeros, np.ndarray):
        return False
    if not isinstance(poles, np.ndarray):
        return False
    if not isinstance(k, (float, complex, int)):  # include int?
        return False

    return True


def _is_sos_format(sos):
    # "second-order filter coefficients, must have shape (n_sections, 6)"
    #   -> according to https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfilt.html#scipy.signal.sosfilt
    if not isinstance(sos, np.ndarray):
        return False

    shape = sos.shape
    if not len(shape) == 2:
        return False
    if not shape[1] == 6:
        return False

    return True


def _cascade_zpk_pair(zpk_a, zpk_b):
    if not (_is_zpk_format(zpk_a) or _is_zpk_format(zpk_b)):
        raise TypeError("One of the inputs is not zpk structured data.")

    z = np.concatenate([zpk_a[0], zpk_b[0]], axis=None)
    p = np.concatenate([zpk_a[1], zpk_b[1]], axis=None)
    k = zpk_a[2] * zpk_b[2]
    return z, p, k


def _cascade_sos_pair(sos_a, sos_b):
    if not (_is_sos_format(sos_a) or _is_sos_format(sos_b)):
        raise TypeError("One of the inputs is not sos structured data.")

    return np.concatenate([sos_a, sos_b], axis=0)


def cascade(*args):
    """
    *args
        Two or more zpk or sos sections that should be cascaded.
        Note that zpk and sos cannot be mixed.
    """
    valid_zpk_cascade = all(map(_is_zpk_format, args))
    if valid_zpk_cascade:
        return reduce(_cascade_zpk_pair, args)

    valid_sos_cascade = all(map(_is_sos_format, args))
    if valid_sos_cascade:
        return reduce(_cascade_sos_pair, args)

    raise TypeError(
        "Input is neither a consistent zpk cascade nor a consistent sos cascade."
    )
