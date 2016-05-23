#!/usr/bin/python
# license removed for brevity
import rospy
from time import sleep
from Communication.msg import GPS

if __name__ == '__main__':
    pub = rospy.Publisher('/drone_id', GPS, queue_size=10)
    rospy.init_node('talker', anonymous=True)
#    rate = rospy.Rate(10) # 10hz
    hz = 20.0
    while not rospy.is_shutdown():
	raw_input("Enter to send 200 msg")
	msg = GPS()
	msg.DOP = 10
	msg.height = 10.43
	msg.lat = 10.123
	msg.lon = 10.321

	for i in range(200):
		status = float(i)/200.0*100
	        rospy.loginfo("msg out %d" % status)
	        pub.publish(msg)
		sleep(1/hz)
