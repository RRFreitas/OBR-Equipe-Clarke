#!/usr/bin/env python3

from time import sleep
from ev3dev.ev3 import LargeMotor, GyroSensor, UltrasonicSensor, ColorSensor, Sound
from os import system

system('setfont Lat15-TerminusBold14')

cl_left = ColorSensor('in1')
cl_right = ColorSensor('in4')
l = LargeMotor('outA')
r = LargeMotor('outC')
gyro = GyroSensor('in2')
sonic = UltrasonicSensor('in3')


gradient = []
count = 0

while 1:
	l.run_forever(speed_sp=-300)
	r.run_forever(speed_sp=-300)

	count += 1

	if(count % 25 == 0):
		count = 1

		gradient.append((cl_left.value(), cl_right.value()))

		if(len(gradient) > 10):
			gradient.pop(0)

		print(gradient)