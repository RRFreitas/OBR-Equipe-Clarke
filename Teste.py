#!/usr/bin/env python3

from time import sleep
from ev3dev.ev3 import LargeMotor, GyroSensor, UltrasonicSensor, ColorSensor
from os import system

system('setfont Lat15-TerminusBold14')

# Instanciando sensores
cl_left = ColorSensor('in1')
cl_right = ColorSensor('in4')
gyro = GyroSensor('in2')
sonic = UltrasonicSensor('in3')

# Instanciando motores
m_right = LargeMotor('outA')
m_left = LargeMotor('outD')

m_left.run_to_rel_pos(position_sp=-120, speed_sp=500, stop_action="hold")
m_right.run_to_rel_pos(position_sp=-120, speed_sp=500, stop_action="hold")
sleep(0.5)

m_right.run_to_rel_pos(position_sp=-360, speed_sp=500, stop_action="hold")
m_left.run_to_rel_pos(position_sp=360, speed_sp=500, stop_action="hold")
sleep(1)

m_left.run_to_rel_pos(position_sp=-45, speed_sp=500, stop_action="hold")
m_right.run_to_rel_pos(position_sp=-45, speed_sp=500, stop_action="hold")
sleep(0.5)