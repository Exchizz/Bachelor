# Send UDP broadcast packets

MYPORT = 8888

import sys
from time import sleep
from socket import *
import struct

#from crc16 import crc16
#s = socket(AF_INET, SOCK_DGRAM)
#s.bind(('', 0))
#s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

try:
    s = socket(AF_INET, SOCK_DGRAM)
except error:
    print 'Failed to create socket'
    sys.exit()

s.settimeout(1)

#data = repr(time.time()) + '\n'
crc = crc16()
for i in range(100):
	counter = i % 10

	lat=10.0
	lon=10.0
	height=10.0
	dop=10.1

	asbytes = struct.pack('ddff', lat,lon,height,dop)
	msg = asbytes;


#	msg = str(counter) + "bcdefghijklmnopqrstu123"

	result = crc.calc(msg)
	crc_out = chr(result >> 8) + chr(result & 0x00ff)

	out = msg + crc_out
	print type(out)
	s.sendto(out, ("Drone1.local", 8888))
	print "out: ", out

#	try:
#		d = s.recvfrom(2)
#		print "answer: ", d[0]
#	except:
#		pass

	sleep(0.05) #20 hz
#	sleep(0.001) #100 hz

#	counter+=1
