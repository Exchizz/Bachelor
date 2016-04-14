#!/usr/bin/python
import socket
import rospy

class Wifi:
        def __init__(self, dst_ip, port):
                self.dest = (dst_ip, port)

                # Datagram (udp) socket
                try:
                        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        rospy.loginfo( 'Socket created' )
                except socket.error, msg :
                        rospy.logfatal( 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1] )
                        exit(1)



        def tx_packet(self, data):
                self.s.sendto(data, self.dest)
                rospy.logdebug("WIFI_TX: " + str(data))

