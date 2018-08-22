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

def girar(graus):
	pos0 = int(gyro.value())
	if(graus > 0):
		while gyro.value() < pos0 + graus:
			l.run_forever(speed_sp=-250)
			r.run_forever(speed_sp=250)
	else:
		while gyro.value() > pos0 + graus:
			l.run_forever(speed_sp=250)
			r.run_forever(speed_sp=-250)

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
	if sonic.value() > 1000:
		andarEmCm(65) #65cm
		sleep(4)
	else:
		girar(80)
		sleep(1)
		andarEmCm(65) #65cm
		sleep(4)

	mapearArea()


def mapearArea():
	gyro.mode = 'GYRO-RATE'
	gyro.mode = 'GYRO-ANG'


	sonar = {}

	while gyro.value() < 360:
		l.run_forever(speed_sp=-150)
		r.run_forever(speed_sp=150)
		
		sonar[gyro.value()] = sonic.value()

	l.stop()
	r.stop()


	print(sonar)

	angulos = list(sonar.keys())

	angulos.sort(key=lambda a: sonar[a])
	print(angulos)

	angAtual = gyro.value()

	print("Angulo Atual: %d  Angulo do objeto: %d" % (angAtual, angulos[0]))

	girar(angulos[0])
	Sound.beep()

	while sonic.value() > 150:
		r.run_forever(speed_sp=-250)
		l.run_forever(speed_sp=-250)


def mostrarDistancia():
	while 1:
		print(sonic.value())

#mostrarDistancia()
rotina3Piso()


"""
3ª sala: 107.5cm x 107.5cm
Entrada: 17cm

Quando terminar rampa:
	rotina3Piso()
"""

