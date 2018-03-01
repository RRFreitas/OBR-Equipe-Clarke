#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time   import sleep

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

MODE = 'linha'

def run():
	while True:
		r1 = cl_left.value()
		r2 = cl_right.value()

		print("Sensor direito: ", r1)
		print("Sensor esquerdo: ", r2)
		
		if((r1 >= VALUE_ON_WHITE and r2 >= VALUE_ON_WHITE) or (r1 <= VALUE_ON_BLACK and r2 <= VALUE_ON_BLACK)):
			m_left.run_forever(speed_sp=MOTOR_MAX_POWER)
			m_right.run_forever(speed_sp=MOTOR_MAX_POWER)
		elif(r1 < VALUE_ON_WHITE and r2 >= VALUE_ON_WHITE):
			while(r1 < VALUE_ON_WHITE or r2 < VALUE_ON_WHITE + 25):
				r1 = cl_left.value()
				r2 = cl_right.value()
				m_left.run_forever(speed_sp=ROT)
				m_right.run_forever(speed_sp=-ROT)
				#m_right.wait_while('running')
		elif(r1 >= VALUE_ON_WHITE and r2 < VALUE_ON_WHITE):
			while(r2 < VALUE_ON_WHITE or r1 < VALUE_ON_WHITE + 25):
				r1 = cl_left.value()
				r2 = cl_right.value()
				m_right.run_forever(speed_sp=ROT)
				m_left.run_forever(speed_sp=-ROT)
				#m_left.wait_while('running') 
def rotateLeft():
	pass

def rotateRight():
	pass

run()
