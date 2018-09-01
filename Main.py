#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ev3dev.ev3 import ColorSensor, LargeMotor, Button, GyroSensor, Sound, UltrasonicSensor, MediumMotor
from PID import PID
from os import system
from time import sleep
from json import dump, load
import threading
import time
import math

# Alterando fonte do brick
system('setfont Lat15-TerminusBold14')

# Instanciando sensores
cl_left = ColorSensor('in1')
cl_right = ColorSensor('in4')
gyro = GyroSensor('in2')
sonic = UltrasonicSensor('in3')

# Instanciando motores
m_right = LargeMotor('outD')
m_left = LargeMotor('outA')
m_garra = LargeMotor('outC')

try:
	# Verificando se os sensores/motores estão conectados
	assert cl_left.connected
	assert cl_right.connected
	assert gyro.connected
	assert sonic.connected
	assert m_left.connected
	assert m_right.connected
except:
	print("ALGUM SENSOR/MOTOR NAO ESTA CONECTADO")
	sleep(2)
	system("clear")
	exit()

# Definindo modo reflectância
cl_left.mode = 'COL-REFLECT'
cl_right.mode = 'COL-REFLECT'

gyro.mode = 'GYRO-ANG'

VERDE = 3
PRETO = 1

DIREITA = 1
ESQUERDA = 0

kp, ki, kd, tp = 6, 0.5, 0.3, -200

def menu():

	botao = Button()

	print("Seta esquerda para calibrar <- | Seta direita para rodar ->")
	
	while True:
		if botao.left:
			system("clear")
			calibrar(botao)
			break
		elif botao.right:
			system("clear")
			dados = lerDados()

			run(kp, ki, kd, tp, dados)
			break
	menu()

def calibrar(botao):

	sensores = {'esquerdo': {'silverTape': {}}, 'direito': {'silverTape': {}}, 'piso_3': {}}

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
	system("clear")
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

	system("clear")
	sleep(1)

	#--------Verde--------

	print("Verde:")
	print("----ESQUERDO----")
	print("Pressione o botao do meio quando estiver pronto.")

	while True:
		if botao.enter:
			sensorEsquerdo = cl_left.value()
			sensores['esquerdo']['verde'] = sensorEsquerdo
			break

	sleep(1)

	print("----DIREITO----")
	print("Pressione o botao do meio quando estiver pronto.")

	while True:
		if botao.enter:
			sensorDireito = cl_right.value()
			sensores['direito']['verde'] = sensorDireito
			break

	system("clear")
	sleep(1)

	#--------SilverTape---------

	print("SilverTape:")
	print("Pressione o botao do meio quando estiver pronto.")

	while True:
		if botao.enter:
			sensorEsquerdo = cl_left.value()
			sensorDireito = cl_right.value()

			sensores['esquerdo']['silverTape']['refl'] = sensorEsquerdo
			sensores['direito']['silverTape']['refl'] = sensorDireito

			cl_left.mode = 'RGB-RAW'
			cl_right.mode = 'RGB-RAW'

			sensorEsquerdo = cl_left.value()
			sensorDireito = cl_right.value()

			sensores['esquerdo']['silverTape']['rgb'] = sensorEsquerdo
			sensores['direito']['silverTape']['rgb'] = sensorDireito

			cl_left.mode = 'COL-REFLECT'
			cl_right.mode = 'COL-REFLECT'
			break

	system("clear")
	sleep(1)

	while True:
		#--------Piso 3---------
		print("PISO 3:")
		print("--DISTANCIA FRONTAL--")
		print("Pressione o botao quando estiver pronto.")
		print(sonic.value() / 10)
		system("clear")
		if botao.enter:
			ultraSonic = sonic.value()
			sensores['piso_3']['frontal'] = ultraSonic
			break

	sleep(1)

	while True:
		print("--DISTANCIA LADO--")
		print("Pressione o botao quando estiver pronto.")
		print(sonic.value() / 10)
		system("clear")
		if botao.enter:
			ultraSonic = sonic.value()
			sensores['piso_3']['lado'] = ultraSonic
			break

	system("clear")
	sleep(1)

	sensores['piso_3']['angulo'] = math.degrees(math.atan(sensores['piso_3']['frontal'] / sensores['piso_3']['lado']))
	sensores['piso_3']['meio'] = math.sqrt((sensores['piso_3']['frontal'] ** 2) + (sensores['piso_3']['lado'] ** 2)) / 2

	print(sensores)

	print("Sensores calibrados.")
	
	sleep(0.5)

	arq = open("sensores.json", "w")

	dump(sensores, arq)

	arq.close()

	print("Valores salvos.")

	sleep(0.5)
	system("clear")

def lerDados():
	"""
		Carrega de um arquivo os valores de branco, preto e verde de cada sensor.
	"""

	arq = open("sensores.json", "r")
	sensores = load(arq)
	return sensores

def getSensorDireito(dados):
	# Retorna o valor do sensor direito calibrado, na escala 0-100

	cl_right.mode = 'COL-REFLECT'

	valor = (
		(dados["direito"]["branco"] - cl_right.value()) /
		(dados["direito"]["branco"] - dados["direito"]["preto"])
	) * -100 + 100
	
	return valor

def getSensorEsquerdo(dados):
	# Retorna o valor do sensor direito calibrado, na escala 0-100

	cl_left.mode = 'COL-REFLECT'

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

def verificarVerde(sensor):
	sensor.mode = 'COL-COLOR'

	cor = sensor.value()

	sensor.mode = 'COL-REFLECT'

	return cor == VERDE

def verificarPreto(sensor):
	sensor.mode = 'COL-COLOR'
	
	cor = sensor.value()
	
	sensor.mode = 'COL-REFLECT'

	return cor == PRETO

def resetarGyro():
	gyro.mode = 'GYRO-RATE'
	gyro.mode = 'GYRO-ANG'

def virar(dir):
	m_left.stop()
	m_right.stop()

	pos0 = gyro.value()

	Sound.beep()

	if(dir == ESQUERDA):
		m_left.run_to_rel_pos(position_sp=-55, speed_sp=900, stop_action="hold")
		m_right.run_to_rel_pos(position_sp=-55, speed_sp=900, stop_action="hold")
		sleep(0.1)

		while gyro.value() > pos0 - 67:
			m_left.run_forever(speed_sp=250)
			m_right.run_forever(speed_sp=-500)

		m_left.stop()
		m_right.stop()
	elif(dir == DIREITA):
		m_left.run_to_rel_pos(position_sp=-55, speed_sp=900, stop_action="hold")
		m_right.run_to_rel_pos(position_sp=-55, speed_sp=900, stop_action="hold")
		sleep(0.1)

		while gyro.value() < pos0 + 67:
			m_left.run_forever(speed_sp=-500)
			m_right.run_forever(speed_sp=250)
		m_left.stop()
		m_right.stop()
	andarEmCm(2)
	sleep(0.5)

def girar(graus):

	pos0 = gyro.value()
	if(graus > 0):
		while gyro.value() < pos0 + graus:
			m_left.run_forever(speed_sp=-250)
			m_right.run_forever(speed_sp=250)
	else:
		while gyro.value() > pos0 + graus:
			m_left.run_forever(speed_sp=250)
			m_right.run_forever(speed_sp=-250)

	m_left.stop()
	m_right.stop()

def andarEmGraus(graus):
	m_left.run_to_rel_pos(position_sp=graus, speed_sp=500, stop_action="hold")
	m_right.run_to_rel_pos(position_sp=graus, speed_sp=500, stop_action="hold")

def andarEmCm(cm):
	andarEmGraus(-28.5 * cm)

def desviar(dados, pid, offset):
	pid.Kp = 10

	sensorEsquerdo = getSensorEsquerdo(dados)
	sensorDireito = getSensorDireito(dados)

	erro = (sensorDireito - sensorEsquerdo) - offset

	print(erro)
	while abs(erro) > 0.5: # 1 segundo
		print(erro)
		sensorEsquerdo = getSensorEsquerdo(dados)
		sensorDireito = getSensorDireito(dados)

		erro = (sensorDireito - sensorEsquerdo) - offset

		pid.update(erro)

		u = pid.output

		m_left.run_forever(speed_sp=saturar(-u))
		m_right.run_forever(speed_sp=saturar(u))

	global kp
	pid.Kp = kp


	Sound.beep()

	pos0 = gyro.value()

	girar(-85)
	sleep(0.1)
	andarEmGraus(-680)
	sleep(2)

	girar(85)
	sleep(0.1)
	andarEmGraus(-1080)
	sleep(3)

	girar(85)
	sleep(0.1)

	andarEmGraus(-250)
	sleep(1.1)

	while cl_left.value() > 25 and cl_right.value() > 25:
		m_left.run_forever(speed_sp=-300)
		m_right.run_forever(speed_sp=-300)
	m_left.stop()
	m_right.stop()

	andarEmCm(2.5)
	sleep(0.4)
	girar(-90)
	sleep(0.6)

	m_left.run_to_rel_pos(position_sp=185, speed_sp=200, stop_action="hold")
	m_right.run_to_rel_pos(position_sp=185, speed_sp=200, stop_action="hold")
	sleep(0.4)


"""
	Anda três centímetros para trás e retorna se alguns dos sentores vê preto.
"""
def verdePosPreto():
	m_right.stop()
	m_left.stop()

	andarEmCm(-1.4)
	sleep(0.5)

	posPreto = verificarPreto(cl_left) or verificarPreto(cl_right)

	andarEmCm(1.4)
	sleep(0.5)

	return posPreto

def virarGiro(pos):
	if pos == "h":
		g_motor.run_to_rel_pos(position_sp=-90, speed_sp=100, stop_action="hold")
		m_left.stop()
		m_right.stop()
		sleep(1)
		gyro.mode = 'GYRO-RATE'
		gyro.mode = 'GYRO-ANG'
		sleep(1)
	elif pos == "v":
		g_motor.run_to_rel_pos(position_sp=90, speed_sp=100, stop_action="hold")
		m_left.stop()
		m_right.stop()
		sleep(1)
		gyro.mode = 'GYRO-RATE'
		gyro.mode = 'GYRO-ANG'
		sleep(1)


def verificarInclinacao():
	if gyro.value() > 15:
		print("Inclinado")
		return True
	else:
		print("Plano")
		return False

def verificarSilverTap(dados):
	if (dados['esquerdo']['silverTape']['refl'] - 10 < cl_left.value() < dados['esquerdo']['silverTape']['refl'] + 10 and 
			dados['direito']['silverTape']['refl'] - 10 < cl_right.value() < dados['direito']['silverTape']['refl'] + 10):

		print("possivel silver tape")
		cl_left.mode = 'RGB-RAW'
		cl_right.mode = 'RGB-RAW'

		if(dados['esquerdo']['silverTape']['rgb'] - 20 < cl_left.value() < dados['esquerdo']['silverTape']['rgb'] + 20 and 
				dados['direito']['silverTape']['rgb'] - 20 < cl_right.value() < dados['direito']['silverTape']['rgb'] + 20):
			cl_left.mode = 'COL-REFLECT'
			cl_right.mode = 'COL-REFLECT'
			Sound.beep()
			rotina3Piso(dados)

def resetarGyro():
	gyro.mode = 'GYRO-RATE'
	gyro.mode = 'GYRO-ANG'

def mapearArea():
	resetarGyro()

	sonar = {}

	while gyro.value() < 360:
		m_left.run_forever(speed_sp=-150)
		m_right.run_forever(speed_sp=150)
		
		sonar[gyro.value()] = sonic.value()

	m_left.stop()
	m_right.stop()


	print(sonar)

	angulos = list(sonar.keys())

	angulos.sort(key=lambda a: sonar[a])
	print(angulos)

	angAtual = gyro.value()

	print("Angulo Atual: %d  Angulo do objeto: %d" % (angAtual, angulos[0]))

	girar(angulos[0])

	distanciaBolinha = sonar[angulos[0]]

	return distanciaBolinha, angulos[0]


def rotina3Piso(dados):

	resetarGyro()

	while sonic.value() > dados['piso_3']['frontal']:
		m_left.run_forever(speed_sp=-100)
		m_right.run_forever(speed_sp=-100)
		print("To na posicao: ", sonic.value())

	girar(-gyro.value())


	#andarEmCm(10)
	#sleep(3)

	girar(-90 + dados['piso_3']['angulo'])
	sleep(2)

	andarEmCm(dados['piso_3']['meio'] / 10)
	sleep(5)

	'''
	if sonic.value() > 800:
		lado = -1 # esquerda
	else:
		girar(60)
		sleep(1)
		lado = 1 # direita
	'''
	#sonar, angulosOrdenados = mapear(-30)
	anguloPlataforma, cantos = localizarPlataforma()
	distanciaBolinha, anguloBolinha = mapearArea()

	distanciaPlataforma = cantos[anguloPlataforma]['distancia']

	distancia = distanciaBolinha / 10 - 7.5 #7.5 é a distancia que o robo tem que ficar da bola pra garrar pegar

	distanciaP = distanciaPlataforma / 10 #3.5 é a distancia que o robo tem que ficar da plataforma para jogar a bola

	irAteBolinha(distancia)
	sleep(3)

	girar(180)
	sleep(2)

	baixarGarra()
	sleep(2)

	girar(-180)
	sleep(2)

	irAteBolinha(-distancia)
	sleep(3)

	girar(-anguloBolinha)
	sleep(3)

	girar(anguloPlataforma)	
	sleep(3)

	irAtePlataforma(distanciaP)
	sleep(3)

	jogarBola()
	sleep(2)

	irAtePlataforma(-distanciaP)
	sleep(3)

	girar(-anguloPlataforma)
	sleep(3)

def jogarBola():
	m_garra.run_to_rel_pos(position_sp=115, speed_sp=300, stop_action="hold")

def baixarGarra():
	m_garra.run_to_rel_pos(position_sp=-225, speed_sp=200, stop_action="hold")

def irAteBolinha(distancia):
	andarEmCm(distancia)

def irAtePlataforma(distancia):
	andarEmCm(distancia)

def localizarPlataforma():
	resetarGyro()
	cantos = {}
	cantos[gyro.value()] = {'distancia': sonic.value()}
	girar(gyro.value() - 90)
	sleep(2)
	cantos[gyro.value()] = {'distancia': sonic.value()}
	girar(gyro.value() + 270)
	sleep(6)
	cantos[gyro.value()] = {'distancia': sonic.value()}
	print(cantos)
	girar(-90)
	sleep(4)

	angulos = list(cantos.keys())

	angulos.sort(key=lambda a: cantos[a]['distancia'])
	
	return angulos[0], cantos  #retorna a lista dos angulos dos cantos em ordem crescente (angulos[0] = area de resgate)


def run(kp, ki, kd, TP, dados):
	"""
		Roda o seguidor de linha.

		Parâmetros:
			kp: Constante do controlador P
			ki: Constante do controlador I
			kd: Constante do controlador D
			TP: Potência base dos motores
			dados: Dicionário com os valores de branco, preto e verde de cada sensor.
	"""

	pid = PID(kp, ki, kd)

	pid.SetPoint=0.0

	offset = dados["direito"]["branco"] - dados["esquerdo"]["branco"]

	#entrouRampa = False

	#vendoVerde = False

	while True:
		if(dados["direito"]["verde"] - 2 < cl_right.value() < dados["direito"]["verde"] + 2 or
			dados["esquerdo"]["verde"] - 2 < cl_left.value() < dados["esquerdo"]["verde"] + 2):

			direitoVendoVerde = verificarVerde(cl_right)
			esquerdoVendoVerde = verificarVerde(cl_left)

			m_right.stop()
			m_left.stop()
			if(direitoVendoVerde and esquerdoVendoVerde):
				#vendoVerde = True
				#virarGiro("h")
				girar(150)
				andarEmCm(3)
				sleep(0.5)
				#virarGiro("v")
				#vendoVerde = False
			elif(direitoVendoVerde):
				#vendoVerde = True
				
				if(verdePosPreto()):
					andarEmCm(2)
					sleep(1)
				else:
					#virarGiro("h")
					virar(DIREITA)
					#virarGiro("v")
				#vendoVerde = False
			elif(esquerdoVendoVerde):
				#vendoVerde = True
				if(verdePosPreto()):
					andarEmCm(2)
					sleep(1)
				else:
					#virarGiro("h")
					virar(ESQUERDA)
					#virarGiro("v")
				#vendoVerde = False

		verificarSilverTap(dados)

		sensorEsquerdo = getSensorEsquerdo(dados)
		sensorDireito = getSensorDireito(dados)

		if(sonic.value() < 80):
			desviar(dados, pid, offset)

		erro = (sensorDireito - sensorEsquerdo) - offset

	    # erro > 0 : Sensor direito encostando na linha
	    # erro < 0 : Sensor esquerdo encostando na linha
	    # erro = 0 : Ambos os sensores na linha, ou nenhum na linha
		

		pid.update(erro)

		u = pid.output

		l = saturar(TP - u)
		r = saturar(TP + u)

		sensorCEsq = cl_left.value()
		sensorCDir = cl_right.value()

		m_left.run_forever(speed_sp=l)
		m_right.run_forever(speed_sp=r)

if __name__ == '__main__':
	menu()
