#!/usr/bin/python
from crc16 import crc16
import socket
import rospy
import struct
class Wifi:
        def __init__(self, dst_ip, port):
                self.dest = (dst_ip, port)
		self.crc = crc16()

                # Datagram (udp) socket
                try:
                        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        rospy.loginfo( 'Socket created' )
                except socket.error, msg :
                        rospy.logfatal( 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1] )
                        exit(1)



        def tx_packet(self, msg):

		result = self.crc.calc(msg)
		crc_out = chr(result >> 8) + chr(result & 0x00ff)

		out = msg + crc_out
		print out
                self.s.sendto(out, self.dest)
#		self.s.sendto(out, ("Drone1.local", 8888))
