# Adapted from https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

from filterdesign import emqf
from filterdesign import filterplot

zpk = emqf.analog_lowpass(order=7, stopband_attenuation=50, f3db=True)

fig = plt.figure(constrained_layout=True, figsize=(11, 4))

gs = fig.add_gridspec(1, 3)
ax1 = fig.add_subplot(gs[0, :-1])
ax2 = fig.add_subplot(gs[0, -1:])

filterplot.plot_analog_filter_zpk(zpk, ax=ax1)
filterplot.pole_zero_plot(zpk, unitcircle=True, ax=ax2)
ax2.set_title("Pole/Zero plot (analog)")
fig.tight_layout()

# ax2.scatter(0, 1)

fig.savefig("./examples/img/emqf_freq_zpk.png", dpi=200)
plt.show()
