#!/usr/bin/env python3

from ev3dev.ev3 import ColorSensor, INPUT_1, INPUT_2, OUTPUT_A, OUTPUT_B, LargeMotor, Button, Screen
from PID import PID
from os import system
from time import sleep
import json

# Instanciando sensores
cl_left = ColorSensor(address=INPUT_1)
cl_right = ColorSensor(address=INPUT_2)

# Instanciando motores
m_left = LargeMotor(address=OUTPUT_A)
m_right = LargeMotor(address=OUTPUT_B)

# Verificando se os sensores/motores estão conectados
assert cl_left.connected
assert cl_right.connected
assert m_left.connected
assert m_right.connected

# Definindo modo reflectância
cl_left.mode = 'COL-REFLECT'
cl_right.mode = 'COL-REFLECT'

# Alterando fonte do brick
system('setfont Lat15-TerminusBold14')

offset = 0

def menu():

	tela = Screen()
	botao = Button()

	tela.clear()
	print("Seta esquerda para calibrar <- | Seta direita para rodar ->")
	
	while True:
		if botao.left:
			tela.clear()
			calibrar(tela, botao)
			break
		elif botao.right:
			tela.clear()
			dados = lerDados()
			run(11, 0, 0, -170, dados)
			break
	menu()

def calibrar(tela, botao):

	sensores = {'esquerdo': {}, 'direito': {}}

	#-------Branco--------

	print("Branco:")
	print("Pressione o botao do meio quando estiver pronto.")
	
	while True:
		if botao.enter:
			sensorEsquerdo = cl_left.value()
			sensorDireito = cl_right.value()
			sensores['esquerdo']['branco'] = sensorEsquerdo
			sensores['direito']['branco'] = sensorDireito
			break
	
	# Limpa tela e espera 1 segundo para soltar o botão
	tela.clear()
	sleep(1)
	
	#--------Preto--------

	print("Preto:")
	print("Pressione o botao do meio quando estiver pronto.")

	while True:
		if botao.enter:
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

	sleep(0.5)

def lerDados():
	"""
		Carrega de um arquivo os valores de branco e preto de cada sensor.
	"""

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

def saturar(valor):
	"""
		Satura para 1000 ou -1000 caso ultrapasse o valor máximo/mínimo
	"""

	if(valor > 1000):
		return 1000
	elif(valor < -1000):
		return -1000
	else:
		return valor

def run(kp, ki, kd, TP, dados):
	"""
		Roda o seguidor de linha.

		Parâmetros:
			kp: Constante do controlador P
			ki: Constante do controlador I
			kd: Constante do controlador D
			TP: Potência base dos motores
			dados: Dicionário com os valores de branco e preto de cada sensor.
	"""

	pid = PID(kp, ki, kd)
	pid.SetPoint=0.0

	while True:
		sensorEsquerdo = getSensorEsquerdo(dados)
		sensorDireito = getSensorDireito(dados)

		erro = (sensorEsquerdo - sensorDireito) - offset

        # erro > 0 : Sensor direito encostando na linha
        # erro < 0 : Sensor esquerdo encostando na linha
        # erro = 0 : Ambos os sensores na linha, ou nenhum na linha
	
		pid.update(erro)

		u = pid.output

		l = saturar(TP + u)
		r = saturar(TP - u)

		m_left.run_forever(speed_sp=l)
		m_right.run_forever(speed_sp=r)

if __name__ == '__main__':
	menu()
