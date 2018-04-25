#!/usr/bin/env python3

from ev3dev.ev3 import ColorSensor, INPUT_1, INPUT_2, OUTPUT_A, OUTPUT_B, LargeMotor, Button
from PID import PID
from os import system
from time import sleep
import json

cl_left = ColorSensor(address=INPUT_1)
cl_right = ColorSensor(address=INPUT_2)

m_left = LargeMotor(address=OUTPUT_A)
m_right = LargeMotor(address=OUTPUT_B)

assert cl_left.connected
assert cl_right.connected
assert m_left.connected
assert m_right.connected

cl_left.mode = 'COL-REFLECT'
cl_right.mode = 'COL-REFLECT'

system('setfont Lat15-TerminusBold14')

offset = 0

def menu():
	
	button = Button()
	print("Seta esquerda para calibrar <- | Seta direita para rodar ->")
	
	while True:
		if button.left:
			calibrar()
			break
		elif button.right:
			dados = lerDados()
			run(11, 0, 0, -170, dados)
			break
	menu()

def calibrar():

	button = Button()

	
	sensores = {'esquerdo': {}, 'direito': {}}

	#-------Branco--------

	print("Branco:")
	print("Pressione o botao do meio quando estiver pronto.")
	
	while True:
		if button.enter:
			sensorEsquerdo = cl_left.value()
			sensorDireito = cl_right.value()
			sensores['esquerdo']['branco'] = sensorEsquerdo
			sensores['direito']['branco'] = sensorDireito
			break
	
	sleep(1.5)
	
	#--------Preto--------

	print("Preto:")
	print("Pressione o botao do meio quando estiver pronto.")

	while True:
		if button.enter:
			sensorEsquerdo = cl_left.value()
			sensorDireito = cl_right.value()
			sensores['esquerdo']['preto'] = sensorEsquerdo
			sensores['direito']['preto'] = sensorDireito
			break

	print("Sensores calibrados.")
	
	sleep(2)

	arq = open("sensores.json", "w")

	json.dump(sensores, arq)

	arq.close()

	print("Valores salvos.")

def lerDados():
	arq = open("sensores.json", "r")
	sensores = json.load(arq)
	return sensores

def getSensorDireito(dados):
	# Retorna o valor do sensor direito calibrado, na escala 0-100

	valor = (
		(dados["direito"]["branco"] - cl_right.value()) /
		(dados["direito"]["branco"] - dados["direito"]["preto"])
	) * -100 + 100
	
	return valor

def getSensorEsquerdo(dados):
	# Retorna o valor do sensor direito calibrado, na escala 0-100

	valor = (
		(dados["esquerdo"]["branco"] - cl_left.value()) /
		(dados["esquerdo"]["branco"] - dados["esquerdo"]["preto"])
	) * -100 + 100

	return valor

def saturar(tp):
	if(tp > 1000):
		return 1000
	elif(tp < -1000):
		return -1000
	else:
		return tp

def run(kp, ki, kd, TP, dados):
	pid = PID(kp, ki, kd)
	pid.SetPoint=0.0

	while True:
		sensorEsquerdo = getSensorEsquerdo(dados)
		sensorDireito = getSensorDireito(dados)

		print("esquerdo = %i direito = %i" % (sensorEsquerdo, sensorDireito))

		erro = (sensorEsquerdo - sensorDireito) - offset

        # erro > 0 : Sensor direito encostando na linha
        # erro < 0 : Sensor esquerdo encostando na linha
        # erro = 0 : Ambos os sensores na linha, ou nenhum na linha
	
		pid.update(erro)

		u = pid.output

		print(erro)

		l = saturar(TP + u)
		r = saturar(TP - u)

		m_left.run_forever(speed_sp=l)
		m_right.run_forever(speed_sp=r)

if __name__ == '__main__':
	menu()
