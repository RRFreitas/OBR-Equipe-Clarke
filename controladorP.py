#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep

TP = -100.0

VALUE_ON_WHITE = 100
VALUE_ON_BLACK = 9
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
kp = 9

def run():
    while True:
        error = (cl_left.value() - cl_right.value()) - offset
        		
        # u < 0 : Sensor direito encostando na linha
        # u > 0 : Sensor esquerdo encostando na linha
        # u = 0 : Ambos os sensores na linha, ou nenhum na linha

        u = kp * error # Ganho proporcional ao erro

        print("error = %i u = %i" % (error, u))	

        m_left.run_forever(speed_sp=TP + u)
        m_right.run_forever(speed_sp=TP - u)
run()
