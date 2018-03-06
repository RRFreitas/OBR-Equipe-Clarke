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
		
		# u < 0 : Sensor direito encostando na linha
		# u > 0 : Sensor esquerdo encostando na linha
		# u = 0 : Ambos os sensores na linha, ou nenhum na linha

		u = kp * error # Ganho proporcional ao erro

		print("error = %i u = %i" % (error, u))		

		if u <= 5 and u >= -5 : #Margem para seguir reto
			m_left.run_forever(speed_sp=MOTOR_MAX_POWER)
			m_right.run_forever(speed_sp=MOTOR_MAX_POWER)
		if u < -5: #Direita no preto, aumentar força no motor esquerdo e inverter no direito
			m_left.run_forever(speed_sp=MOTOR_MAX_POWER)
			m_right.run_forever(speed_sp=MOTOR_MIN_POWER)
		if u > 5: #Esquerda no preto, aumentar força no motor direito e inverter no esquerdo
			m_left.run_forever(speed_sp=MOTOR_MIN_POWER)
			m_right.run_forever(speed_sp=MOTOR_MAX_POWER)

run()
