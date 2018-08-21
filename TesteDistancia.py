#!/usr/bin/env python3

from ev3dev.ev3 import UltrasonicSensor
from os import system

system('setfont Lat15-TerminusBold14')

sonic = UltrasonicSensor('in3')

while True:
	print(sonic.value())
	system("clear")