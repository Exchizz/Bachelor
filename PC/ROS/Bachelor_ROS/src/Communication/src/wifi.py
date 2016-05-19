#!/usr/bin/python
#from crc16 import crc16
import crc16
import socket
import rospy
import struct
from crc_algorithms import Crc
class Wifi:
        def __init__(self, dst_ip, port):
                self.dest = (dst_ip, port)
	#	self.crc = crc16()

		self.crc = Crc(width = 16, poly = 0x8005, reflect_in = True, xor_in = 0x0000, reflect_out = True, xor_out = 0x0000)
                # Datagram (udp) socket
                try:
                        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        rospy.loginfo( 'Socket created' )
                except socket.error, msg :
                        rospy.logfatal( 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1] )
                        exit(1)



        def tx_packet(self, msg):

#		result = self.crc.calc(msg)
#		crc_out = chr(result >> 8) + chr(result & 0x00ff)

#		msg="abcdefgijklmnopqrstuvxyz12345678"
		result = self.crc.table_driven(msg)
#		print("{0:#x}".format(msg))

		crc_out = chr(result >> 8) + chr(result & 0x00ff)

		out = msg + crc_out
		print out
                self.s.sendto(out, self.dest)
#		self.s.sendto(out, ("Drone1.local", 8888))
