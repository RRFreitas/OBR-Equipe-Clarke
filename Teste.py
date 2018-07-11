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
m_right = LargeMotor('outC')
m_left = LargeMotor('outA')

def saturar(valor):
	"""
		Satura para 1000 ou -1000 caso ultrapasse o valor máximo/mínimo
	"""

	if(valor > 500):
		return 500
	elif(valor < 0):
		return -500
	else:
		return valor

def desviar():
	while sideSonic.value() > 100:
		m_right.run_forever(speed_sp=500)
		m_left.run_forever(speed_sp=-500)

	pid = PID(1.5, 0.1, 0.1)
	pid.SetPoint = 60

	while 1:
		pid.update(sideSonic.value())

		u = pid.output

		if(abs(u) > 1000):
			u = -u
			u = u/2
		print(u)

		l = saturar(-200 + u)
		r = saturar(-200 - u)

		m_right.run_forever(speed_sp=r)
		m_left.run_forever(speed_sp=l)

while 1:
	if(sonic.value() < 60):
		desviar()

	m_right.run_forever(speed_sp=-200)
	m_left.run_forever(speed_sp=-200)