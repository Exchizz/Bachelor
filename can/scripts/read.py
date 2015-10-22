#!/usr/bin/python

import can
import time

class CAN:
	def __init__(self):
		self.bus = can.interface.Bus('slcan0', bustype='socketcan')

	def send(self,data):
		msg = can.Message(arbitration_id=0x1e000000, data=data, extended_id=False)
		if self.bus.send(msg) < 0:
			print("Message NOT sent")
		else:
			print("Message sent")


	def recv(self):
		return self.bus.recv()

if __name__ == "__main__":
		canz = CAN()
#	while True:
#		print (canz.recv())
		canz.send('AAAAAAAA')
		time.sleep(0.5)
