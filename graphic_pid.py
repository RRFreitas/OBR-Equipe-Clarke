#!/usr/bin/env python3

import PID
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

arq = open('log.txt')

feedback_list = []

for line in arq.readlines():
	feedback_list.append(float(line.replace('\n', '')))

def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100, feed_list=[]):
	pid = PID.PID(P, I, D)

	pid.SetPoint=0.0
	pid.setSampleTime(0.01)

	END = L
	feedback = 0

	time_list = []

	for i in range(1, END):
		pid.update(feedback)
		output = pid.output
		time.sleep(0.02)

       # feedback_list.append(feedback)
		time_list.append(i)

	time_sm = np.array(time_list)
	time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)

	plt.plot(time_smooth, feed_list)
	plt.xlim((0, len(feed_list)))
	plt.ylim((min(feed_list)-0.5, max(feed_list)+0.5))
	plt.xlabel('time (s)')
	plt.ylabel('PID (PV)')
	plt.title('TEST PID')

	plt.ylim((1-0.5, 1+0.5))

	plt.grid(True)
	plt.show()

if __name__ == "__main__":
	test_pid(9, 0, 0, 263, feedback_list)
