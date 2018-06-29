#!/usr/bin/env python3

from time import sleep
from ev3dev.ev3 import LargeMotor, GyroSensor, UltrasonicSensor, ColorSensor
from os import system
from PID import PID

system('setfont Lat15-TerminusBold14')

# Instanciando sensores
cl_left = ColorSensor('in1')
cl_right = ColorSensor('in4')
sideSonic = UltrasonicSensor('in2')
sonic = UltrasonicSensor('in3')

# Instanciando motores
m_right = LargeMotor('outD')
m_left = LargeMotor('outA')

def saturar(valor):
	"""
		Satura para 1000 ou -1000 caso ultrapasse o valor máximo/mínimo
	"""

	if(valor > 1000):
		return 1000
	elif(valor < 0):
		return -1000
	else:
		return valor

def desviar():
	while sideSonic.value() > 100:
		m_right.run_forever(speed_sp=200)
		m_left.run_forever(speed_sp=-200)

	pid = PID(0.5, 0, 0)
	pid.SetPoint = 300

	while 1:
		pid.update(sideSonic.value())

		u = pid.output

		print(u)

		l = saturar(-200 + u)
		r = saturar(-200 - u)

		if(abs(l) + abs(r) > 1900):
			l, r = r, l

		m_right.run_forever(speed_sp=r)
		m_left.run_forever(speed_sp=l)

while 1:
	if(sonic.value() < 60):
		desviar()

	m_right.run_forever(speed_sp=-200)
	m_left.run_forever(speed_sp=-200)