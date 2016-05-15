#!/usr/bin/python
import rospy
import struct
from wifi import Wifi
#from std_msgs.msg import String
from Communication.msg import GPS

class ROS:
        def __init__(self):
                # Create node
                rospy.init_node( 'Wifi', anonymous=True )

                # Get topic-name from param-server
                topic_in = rospy.get_param( 'topic_in', '/data_in' )

                # Get drone settings from param-server
                param_drone_ip = rospy.get_param( 'drone_ip', 'Drone1.local' )
                param_drone_port = rospy.get_param( 'drone_port', 8888 )

                # Subscribe to popic
                rospy.Subscriber( topic_in, GPS, self.topic_callback )

                # Create instance of wifi-class
                self.wifi_out = Wifi( param_drone_ip, param_drone_port )

        def spin(self):
                # spin() simply keeps python from exiting until this node is stopped
                rospy.spin()

        def topic_callback(self, msg):
		lat = msg.lat
		lon = msg.lon
		height = msg.height
		dop = msg.DOP

#		print lat, lon, height, dop
#		lat = 10
#		lon = 12.12345
#		height = 10.1
#		dop = 10.5
#		print lat, lon, height, dop

		asstring = struct.pack('dddd', lat,lon,height,dop)
#		print struct.unpack('ddff',asstring)
                self.wifi_out.tx_packet(asstring)


