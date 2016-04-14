#!/usr/bin/python

import rospy
from std_msgs.msg import String
import socket

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


class ROS:
	def __init__(self):
		# Create node
		rospy.init_node( 'Wifi', anonymous=True )

		# Get topic-name from param-server
		topic_in = rospy.get_param( 'topic_in', '/communication/to_drone' )

		# Get drone settings from param-server
		param_drone_ip = rospy.get_param( 'drone_ip', '172.16.0.34' )
		param_drone_port = rospy.get_param( 'drone_port', 1337 )

		# Subscribe to popic
		rospy.Subscriber( topic_in, String, self.topic_callback )

		# Create instance of wifi-class
		self.wifi_out = Wifi( param_drone_ip, param_drone_port )

	def spin(self):
		# spin() simply keeps python from exiting until this node is stopped
		rospy.spin()

	def topic_callback(self, msg):
		rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg.data)
		self.wifi_out.tx_packet(msg.data)		

if __name__ == '__main__':
	ros = ROS()
	ros.spin()
