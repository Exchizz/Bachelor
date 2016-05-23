#!/usr/bin/python

# import utmconv class
from transverse_mercator_py.utm import utmconv
from math import pi, cos
import rospy

from Communication.msg import GPS
from markerLocator.msg import DronePose
from time import time, sleep


Robolab_ll = (55.367522, 10.432557) # latitude, longitude

class DecisionMaker:
	def __init__(self):
		rospy.init_node('talker', anonymous=True)

		pub_droneout = rospy.get_param('~drone_out', '/communication/drone')
		self.pub = rospy.Publisher(pub_droneout, GPS, queue_size=10) ## change msg type

		pub_dronein = rospy.get_param('~pose_in', '/positions/drone')
		rospy.Subscriber(pub_dronein, DronePose, self.pose_callback)
		self.rate = rospy.Rate(1) # 1hz
		self.uc = utmconv()

		# Robolab in UTM
#		(hemisphere, zone, letter, easting, northing) = uc.geodetic_to_utm (Robolab_ll)
		self.utm_offset = self.uc.geodetic_to_utm (Robolab_ll[0], Robolab_ll[1])
		(hemisphere, zone, letter, easting, northing) = self.utm_offset
		print '\nConverted from geodetic to UTM [m]'
		print '  %d %c %.5fe %.5fn' % (zone, letter, easting, northing)

		self.last_msg_time = 0
		self.img_hz = 20

		self.utm_pose_in = (0,0)
	def pose_callback(self, msg):
		order_match = msg.order_match
		if order_match:
			quality = msg.quality
			pose_local = (msg.x, msg.y)

			self.utm_pose_in = (self.utm_offset[3] + msg.x, self.utm_offset[4] + msg.y)
			self.last_msg_time = time()

	def utm_to_ll(self, utm):
		return self.uc.utm_to_geodetic (self.utm_offset[0], self.utm_offset[1], utm[0], utm[1])


	def spin(self):
		while not rospy.is_shutdown():

			now = time()
			if(now - self.last_msg_time) < 1.0/self.img_hz:
				rospy.loginfo("%s: Drone locked" % rospy.get_name())


				# Manipulate drones position
				utm_pose_out = self.utm_pose_in


				ll_pose_out = self.utm_to_ll(utm_pose_out)
				gps = GPS()
				gps.lat = ll_pose_out[0]
				gps.lon = ll_pose_out[1]
				gps.height = 30
				gps.DOP = 2
	
				self.pub.publish(gps)
			else:
				rospy.logwarn("%s:No drone position" % rospy.get_name())

			self.rate.sleep()
if __name__ == '__main__':
	decisionMaker = DecisionMaker()
	decisionMaker.spin()
