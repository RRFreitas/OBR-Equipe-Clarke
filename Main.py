#!/usr/bin/env python3

from ev3dev.ev3 import ColorSensor, INPUT_1, INPUT_4, OUTPUT_A, OUTPUT_C, LargeMotor, Button, Sound, UltrasonicSensor
from PID import PID
from os import system
from time import sleep
from json import dump, load

# Alterando fonte do brick
system('setfont Lat15-TerminusBold14')

# Instanciando sensores
cl_left = ColorSensor(address=INPUT_1)
cl_right = ColorSensor(address=INPUT_4)
sideSonic = UltrasonicSensor('in2')
sonic = UltrasonicSensor('in3')

# Instanciando motores
m_right = LargeMotor(address=OUTPUT_A)
m_left = LargeMotor(address=OUTPUT_C)

try:
	# Verificando se os sensores/motores estão conectados
	assert cl_left.connected
	assert cl_right.connected
	assert sideSonic.connected
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

offset = 0

VERDE = 3
PRETO = 1

DIREITA = 1
ESQUERDA = 0

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
			run(10, 0.5, 0.3, -260, dados)
			break
	menu()

def calibrar(botao):

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

def girar90(dir):
	m_left.stop()
	m_right.stop()

	if(dir == ESQUERDA):
		m_right.run_to_rel_pos(position_sp=42
		0, speed_sp=500, stop_action="hold")
		m_left.run_to_rel_pos(position_sp=-420, speed_sp=500, stop_action="hold")
		sleep(1)
	elif(dir == DIREITA):
		m_right.run_to_rel_pos(position_sp=-420, speed_sp=500, stop_action="hold")
		m_left.run_to_rel_pos(position_sp=420, speed_sp=500, stop_action="hold")
		sleep(1)

def virar(dir):
	m_left.stop()
	m_right.stop()

	Sound.beep()

	if(dir == ESQUERDA):
		m_left.run_to_rel_pos(position_sp=-120, speed_sp=500, stop_action="hold")
		m_right.run_to_rel_pos(position_sp=-120, speed_sp=500, stop_action="hold")
		sleep(0.5)

		m_right.run_to_rel_pos(position_sp=360, speed_sp=500, stop_action="hold")
		m_left.run_to_rel_pos(position_sp=-360, speed_sp=500, stop_action="hold")
		sleep(1)

		m_left.run_to_rel_pos(position_sp=-90, speed_sp=500, stop_action="hold")
		m_right.run_to_rel_pos(position_sp=-90, speed_sp=500, stop_action="hold")
		sleep(0.5)
	elif(dir == DIREITA):
		m_left.run_to_rel_pos(position_sp=-120, speed_sp=500, stop_action="hold")
		m_right.run_to_rel_pos(position_sp=-120, speed_sp=500, stop_action="hold")
		sleep(0.5)

		m_right.run_to_rel_pos(position_sp=-360, speed_sp=500, stop_action="hold")
		m_left.run_to_rel_pos(position_sp=360, speed_sp=500, stop_action="hold")
		sleep(1)

		m_left.run_to_rel_pos(position_sp=-90, speed_sp=500, stop_action="hold")
		m_right.run_to_rel_pos(position_sp=-90, speed_sp=500, stop_action="hold")
		sleep(0.5)

"""
def girar(graus):
	pos0 = gyro.value()
	if(graus > 0):
		while gyro.value() < pos0 + graus:
			m_left.run_forever(speed_sp=250)
			m_right.run_forever(speed_sp=-500)
	else:
		while gyro.value() > pos0 + graus:
			m_left.run_forever(speed_sp=-500)
			m_right.run_forever(speed_sp=250)

	m_left.stop()
	m_right.stop()
"""

def andarEmGraus(graus):
	m_left.run_to_rel_pos(position_sp=graus, speed_sp=900, stop_action="hold")
	m_right.run_to_rel_pos(position_sp=graus, speed_sp=900, stop_action="hold")

"""def desviar(dados):

	Sound.beep()

	pos0 = gyro.value()

	girar(82)
	sleep(0.1)
	andarEmGraus(-500)
	sleep(1)

	girar(-82)
	sleep(0.1)
	andarEmGraus(-750)
	sleep(1.5)

	girar(-82)
	sleep(0.1)

	andarEmGraus(-200)
	sleep(1.1)

	reflectancia = abs(cl_left.value()) + abs(cl_left.value())

	while reflectancia > 25:
		reflectancia = abs(cl_left.value()) + abs(cl_left.value())
		m_left.run_forever(speed_sp=-300)
		m_right.run_forever(speed_sp=-300)
	m_left.stop()
	m_right.stop()

	girar(85)
	sleep(0.1)

	m_left.run_to_rel_pos(position_sp=125, speed_sp=400, stop_action="hold")
	m_right.run_to_rel_pos(position_sp=125, speed_sp=400, stop_action="hold")
	sleep(0.3)"""

def desviar():
	girar90(DIREITA)

	distancia = sideSonic.value()

	while distancia < 100:
		distancia = sideSonic.value()
		m_left.run_forever(speed_sp=-300)
		m_right.run_forever(speed_sp=-300)
	
	m_left.run_forever(speed_sp=-300)
	m_right.run_forever(speed_sp=-300)
	sleep(1)
	girar90(ESQUERDA)

	m_left.run_forever(speed_sp=-300)
	m_right.run_forever(speed_sp=-300)
	sleep(2)

	distancia = sideSonic.value()
	while distancia < 150:
		distancia = sideSonic.value()
		m_left.run_forever(speed_sp=-300)
		m_right.run_forever(speed_sp=-300)
		print(distancia)
	
	m_left.run_forever(speed_sp=-300)
	m_right.run_forever(speed_sp=-300)
	sleep(1)
	girar90(ESQUERDA)
	
	reflectancia = abs(cl_left.value()) + abs(cl_left.value())

	while reflectancia > 25:
		reflectancia = abs(cl_left.value()) + abs(cl_left.value())
		m_left.run_forever(speed_sp=-300)
		m_right.run_forever(speed_sp=-300)
	m_left.stop()
	m_right.stop()
	girar90(DIREITA)

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

	global offset

	print("potencia esquerda,potencia direita")

	while True:
		if(dados["direito"]["verde"] - 1 < cl_right.value() < dados["direito"]["verde"] + 1 or
			dados["esquerdo"]["verde"] - 1 < cl_left.value() < dados["esquerdo"]["verde"] + 1):

			direitoVendoVerde = verificarVerde(cl_right)
			esquerdoVendoVerde = verificarVerde(cl_left)

			if(direitoVendoVerde):
				virar(DIREITA)
			elif(esquerdoVendoVerde):
				virar(ESQUERDA)

		if(sonic.value() < 60):
			print("uhu")
			desviar()
			#desviar(dados)

		sensorEsquerdo = getSensorEsquerdo(dados)
		sensorDireito = getSensorDireito(dados)

		erro = (sensorDireito - sensorEsquerdo) - offset

		offset = 0
	    # erro > 0 : Sensor direito encostando na linha
	    # erro < 0 : Sensor esquerdo encostando na linha
	    # erro = 0 : Ambos os sensores na linha, ou nenhum na linha
		
		pid.update(erro)

		u = pid.output

		l = saturar(TP + u)
		r = saturar(TP - u)

		sensorCEsq = cl_left.value()
		sensorCDir = cl_right.value()

		m_left.run_forever(speed_sp=l)
		m_right.run_forever(speed_sp=r)

if __name__ == '__main__':
	menu()