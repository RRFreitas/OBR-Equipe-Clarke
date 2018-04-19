#!/usr/bin/env python3

from ev3dev.ev3 import ColorSensor, INPUT_1, INPUT_2, OUTPUT_A, OUTPUT_B, LargeMotor
from PID import PID

VALUE_ON_WHITE = 100
VALUE_ON_BLACK = 9
VALUE_ON_GREEN = 15

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

offset = -9

def run(kp, ki, kd, TP):
	pid = PID(kp, ki, kd)
	pid.SetPoint=0.0

	arq = open('log.txt', 'w+')
	print("erro,sensor esquerdo,sensor direito")
	while True:
		error = (cl_left.value() - cl_right.value()) - offset

        # u > 0 : Sensor direito encostando na linha
        # u < 0 : Sensor esquerdo encostando na linha
        # u = 0 : Ambos os sensores na linha, ou nenhum na linha

        #u = kp * error  # Ganho proporcional ao erro
	
		pid.update(error)

		u = pid.output

		#arq.write('tp-u=%i  tp+u=%i\n' % (TP-u, TP+u))

		l = saturar(TP + u)
		r = saturar(TP - u)

		print(error, sep=",")

		m_left.run_forever(speed_sp=l)
		m_right.run_forever(speed_sp=r)


def saturar(tp):
	if(tp > 1000):
		return 1000
	elif(tp < -1000):
		return -1000
	else:
		return tp

if __name__ == '__main__':
	run(9.3, 0, 0, -170)
