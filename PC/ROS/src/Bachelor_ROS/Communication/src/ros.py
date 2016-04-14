#!/usr/bin/python
import rospy
from wifi import Wifi
from std_msgs.msg import String

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


