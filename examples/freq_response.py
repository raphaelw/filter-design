# Adapted from https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

from filterdesign import emqf
from filterdesign import filterplot

z, p, k = emqf.analog_lowpass(order=7, stopband_attenuation=50, f3db=True)

fig_ = plt.figure(constrained_layout=True, figsize=(11, 4))

gs = fig_.add_gridspec(1, 3)
ax1 = fig_.add_subplot(gs[0, :-1])
ax2 = fig_.add_subplot(gs[0, -1:])

filterplot.plot_analog_filter_zpk((z, p, k), ax=ax1)
filterplot.pole_zero_plot((z, p, k), unitcircle=True, ax=ax2)
ax2.set_title("Pole/Zero plot (analog)")
fig_.tight_layout()


fig, ax = plt.subplots(1, 2)
filterplot.plot_analog_filter_zpk((z, p, k), ax=ax[0])
filterplot.pole_zero_plot((z, p, k), unitcircle=True, ax=ax[1])
# ax2.scatter(0, 1)

fig_.savefig("./examples/img/emqf_freq_zpk.png", dpi=200)
plt.show()
