#!/usr/bin/env python3

from ev3dev.ev3 import ColorSensor, LargeMotor, Button, GyroSensor, Sound, UltrasonicSensor, MediumMotor
from time import sleep

gyro = GyroSensor('in2')
g_motor = MediumMotor('outC')


def virarGiro(pos):
	if pos == "h":
		g_motor.run_to_rel_pos(position_sp=90, speed_sp=100, stop_action="hold")
		sleep(1)
		gyro.mode = 'GYRO-RATE'
		gyro.mode = 'GYRO-ANG'
	elif pos == "v":
		g_motor.run_to_rel_pos(position_sp=-90, speed_sp=100, stop_action="hold")
		sleep(1)
		gyro.mode = 'GYRO-RATE'
		gyro.mode = 'GYRO-ANG'

virarGiro("v")

def verificarInclinacao():
	if gyro.value() < -10:
		print("Inclinado")
		return True
	else:
		print("Plano")
		return False

entrouRampa = False

if not entrouRampa:
	if verificarInclinacao():
		entrouRampa = True
elif entrouRampa:
	if not verificarInclinacao():
		andarEmCm(5)
		rotina3Piso()