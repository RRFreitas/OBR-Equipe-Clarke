#!/usr/bin/env python3

from ev3dev.ev3 import ColorSensor, LargeMotor, Button, GyroSensor, Sound, UltrasonicSensor, ServoMotor
from PID import PID
from os import system
from time import sleep
from json import dump, load

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
			run(11, 0.5, 0.3, -260, dados)
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
	andarEmCm(2.7)
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
	m_left.run_to_rel_pos(position_sp=graus, speed_sp=900, stop_action="hold")
	m_right.run_to_rel_pos(position_sp=graus, speed_sp=900, stop_action="hold")

def andarEmCm(cm):
	andarEmGraus(-28.5 * cm)

def desviar(dados):

	Sound.beep()

	pos0 = gyro.value()

	girar(-85)
	sleep(0.1)
	andarEmGraus(-700)
	sleep(1)

	girar(75)
	sleep(0.1)
	andarEmGraus(-1000)
	sleep(1.8)

	girar(85)
	sleep(0.1)

	andarEmGraus(-250)
	sleep(1.1)

	reflectancia = abs(cl_left.value()) + abs(cl_left.value())

	while reflectancia > 25:
		reflectancia = abs(cl_left.value()) + abs(cl_left.value())
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

	andarEmCm(-2)
	sleep(0.5)

	posPreto = verificarPreto(cl_left) or verificarPreto(cl_right)

	andarEmCm(2)
	sleep(0.5)

	return posPreto

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

	while True:
		if(dados["direito"]["verde"] - 2 < cl_right.value() < dados["direito"]["verde"] + 2 or
			dados["esquerdo"]["verde"] - 2 < cl_left.value() < dados["esquerdo"]["verde"] + 2):

			direitoVendoVerde = verificarVerde(cl_right)
			esquerdoVendoVerde = verificarVerde(cl_left)

			#m_right.stop()
			#m_left.stop()
			if(direitoVendoVerde and esquerdoVendoVerde):
				girar(150)
				andarEmCm(3)
				sleep(0.5)
			elif(direitoVendoVerde):
				virar(DIREITA)
				"""if(verdePosPreto()):
					andarEmCm(2)
					sleep(0.5)
				else:
					virar(DIREITA)"""
			elif(esquerdoVendoVerde):
				virar(ESQUERDA)
				"""if(verdePosPreto):
					andarEmCm(0.5)
					sleep(1)
				else:
					virar(ESQUERDA)"""

		if(sonic.value() < 80):
			desviar(dados)

		sensorEsquerdo = getSensorEsquerdo(dados)
		sensorDireito = getSensorDireito(dados)

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
