# Adapted from https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

from filterdesign import emqf

N = 5
As = 50
z, p, k = emqf.analog_lowpass(N=N, As=As, f3db=True)

b, a = signal.zpk2tf(z, p, k)
w, h = signal.freqs(b, a, 2000)
plt.semilogx(w, 20 * np.log10(abs(h)))
plt.title("Filter frequency response")
plt.xlabel("Frequency [radians / second]")
plt.ylabel("Amplitude [dB]")
plt.margins(0, 0.1)
plt.grid(which="both", axis="both")
# plt.axvline(100, color='green') # cutoff frequency
plt.show()
