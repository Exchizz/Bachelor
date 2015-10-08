#!/usr/bin/python

import can
import time
import can
import time


class CAN:
	def __init__(self):
		self.bus = can.interface.Bus('slcan1', bustype='socketcan')


	def send(self,data):
		msg = can.Message(arbitration_id=0x000000, data=data, extended_id=False)
		return (self.bus.send(msg) < 0)


	def recv(self):
		return self.bus.recv()

if __name__ == "__main__":
	canz = CAN()
	while True:
		print (canz.recv())


