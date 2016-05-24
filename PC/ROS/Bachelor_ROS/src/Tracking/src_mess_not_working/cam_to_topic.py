#!/usr/bin/env python
import cv2
import cv
import signal
import sys
import os

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from time import sleep

def signal_handler(signal, frame):
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
	rospy.init_node('image_converter', anonymous=True)

	device = rospy.get_param( '~device' , 1)
#	cap = cv2.VideoCapture('/home/exchizz/SDU/Skole/Bachelor/PC/ROS/Bachelor_ROS/src/Tracking/src/my_video-10.mkv')
        # Disable autofocus
        os.system('v4l2-ctl -d 1 -c focus_auto=0')

        # Set focus to a specific value. High values for nearby objects and
        # low values for distant objects.
        os.system('v4l2-ctl -d 1 -c focus_absolute=0')

        # sharpness (int)    : min=0 max=255 step=1 default=128 value=128
        os.system('v4l2-ctl -d 1 -c sharpness=200')

	cap = cv2.VideoCapture(device)

	# width, 3 = width
	cap.set(3,1920);
	# height, 4 = height
	cap.set(4,1080);

	topic_camera = rospy.get_param( '~camera_out' , "/camera/stream")
	image_pub = rospy.Publisher(topic_camera, Image, queue_size=1)
	bridge = CvBridge()

#	raw_input("Press Enter to start playing...")

	while cap.isOpened():
		ret,frame = cap.read()
		if not ret:
			print "No frame..."
			exit(1)
		image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
