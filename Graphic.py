#!/usr/bin/env python3

import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

arq = open('log.txt')

time_list = []

for line in arq.readlines():
	time_list.append(float(line.replace('\n', '')))

print(time_list)

# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

# Note that using plt.subplots below is equivalent to using
# fig = plt.figure() and then ax = fig.add_subplot(111)
fig, ax = plt.subplots()
ax.plot(t, time_list)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()
