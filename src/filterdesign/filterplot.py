import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def pole_zero_plot(zpk, unitcircle=False, ax=None):
    """
    Create pole zero plots as seen in the signal processing field.

    zpk : list
        Nested list containing zeros at zpk[0] and poles at zpk[1].
    unitcircle : bool
        Plot unit circle.
    ax : matplotlib axes object
        Optionally specify an axes object.
    """
    zeros = zpk[0]
    poles = zpk[1]

    if ax == None:
        ax = plt.gca()

    ax.set_aspect(aspect="equal", adjustable="datalim")

    if unitcircle:
        patch = mpl.patches.Circle(
            (0, 0), 1, facecolor="None", edgecolor="0.75", linestyle="dashed"
        )
        ax.add_patch(patch)

    # origin
    origin_lw = 1
    ax.axhline(y=0, color="k", lw=origin_lw)
    ax.axvline(x=0, color="k", lw=origin_lw)

    # plot
    symbol_scale = 40
    zorder = 2.5
    ax.scatter(
        np.real(poles),
        np.imag(poles),
        marker="x",
        s=symbol_scale,
        c="k",
        zorder=zorder,
        label="Poles",
    )
    ax.scatter(
        np.real(zeros),
        np.imag(zeros),
        marker="o",
        s=symbol_scale * 1.15,
        color="None",
        edgecolor="k",
        zorder=zorder,
        label="Zeros",
    )

    ax.set_title("Pole/Zero plot")


def plot_analog_filter_zpk(zpk, ax=None, worN=2000):
    if ax == None:
        ax = plt.gca()
    z, p, k = zpk
    b, a = signal.zpk2tf(z, p, k)
    w_, h = signal.freqs(b, a, worN)
    ax.semilogx(w_, 20 * np.log10(abs(h)))
    ax.set_title("Filter frequency response")
    ax.set_xlabel("Frequency [radians / second]")
    ax.set_ylabel("Amplitude [dB]")
    ax.margins(0, 0.1)
    ax.grid(which="both", axis="both")


if __name__ == "__main__":
    plt.figure()
    pole_zero_plot(
        zpk=[(1 + 1j, 0.5 + 1j, 1j, 4j), (-1 - 0.75j, -0.5 + 0.333j)], unitcircle=True
    )
    plt.show()
