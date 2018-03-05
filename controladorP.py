#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep

MOTOR_MAX_POWER = -150.0
MOTOR_MIN_POWER = 150.0

VALUE_ON_WHITE = 70
VALUE_ON_BLACK = 5
VALUE_ON_GREEN = 15

ROT = 100

cl_left = ColorSensor(address=INPUT_1)
cl_right = ColorSensor(address=INPUT_2)

m_left = LargeMotor(address=OUTPUT_A)
m_right = LargeMotor(address=OUTPUT_B)

assert cl_left.connected
assert cl_right.connected
assert m_left.connected
assert m_right.connected

cl_left.mode='COL-REFLECT'
cl_right.mode='COL-REFLECT'

offset = 0
kp = 0.2

def run():
	while True:
		error = (cl_left.value() - cl_right.value()) - offset
		
		u = kp * error

		print("error = %i u = %i" % (error, u))		

		if u <= 5 and u >= -5 :
			m_left.run_forever(speed_sp=MOTOR_MAX_POWER)
			m_right.run_forever(speed_sp=MOTOR_MAX_POWER)
		elif u < -5: #Direita no preto
			m_left.run_forever(speed_sp=MOTOR_MAX_POWER + u)
			m_right.run_forever(speed_sp=-(MOTOR_MAX_POWER + u))
		elif u > 5: #Esquerda no preto
			m_left.run_forever(speed_sp=-(MOTOR_MAX_POWER + u))
			m_right.run_forever(speed_sp=MOTOR_MAX_POWER + u)

run()
