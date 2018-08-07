#!/usr/bin/env python3

from time import sleep
from ev3dev.ev3 import LargeMotor, GyroSensor, UltrasonicSensor, ColorSensor
from os import system
from threading import Timer

system('setfont Lat15-TerminusBold14')

cl_left = ColorSensor('in1')
cl_right = ColorSensor('in4')
l = LargeMotor('outA')
r = LargeMotor('outC')
gyro = GyroSensor('in2')
sonic = UltrasonicSensor('in3')

def girar(graus):
	pos0 = int(gyro.value())
	if(graus > 0):
		while gyro.value() < pos0 + graus:
			l.run_forever(speed_sp=-500)
			r.run_forever(speed_sp=250)
	else:
		while gyro.value() > pos0 + graus:
			l.run_forever(speed_sp=250)
			r.run_forever(speed_sp=-500)

	l.stop()
	r.stop()

def andarEmCm(cm):
	andarEmGraus(-28.5 * cm)

def andarEmGraus(graus):
	l.run_to_rel_pos(position_sp=graus, speed_sp=900, stop_action="hold")
	r.run_to_rel_pos(position_sp=graus, speed_sp=900, stop_action="hold")

def rotina3Piso():
	gyro.mode = 'GYRO-RATE'
	gyro.mode = 'GYRO-ANG'
	andarEmCm(40)
	sleep(2)
	girar(-gyro.value())
	sleep(1)
	girar(-45)
	sleep(2)
	if sonic.value() > 300:
		andarEmCm(55) #65cm
		sleep(2)
	else:
		girar(80)
		andarEmCm(65) #65cm
		sleep(2)


def mapearArea():
	gyro.mode = 'GYRO-RATE'
	gyro.mode = 'GYRO-ANG'


	sonar = {}

	while gyro.value() < 360:
		l.run_forever(speed_sp=-500)
		r.run_forever(speed_sp=500)
		
		sonar[gyro.value()] = sonic.value()

	l.stop()
	r.stop()

	print(sonar)

	angulos = list(sonar.keys())

	angulos.sort(key=lambda a: sonar[a])
	print(angulos)



mapearArea()
#rotina3Piso()
"""
3ª sala: 107.5cm x 107.5cm
Entrada: 17cm

Quando terminar tampa:
	rotina3Piso()
"""

