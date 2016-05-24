#!/usr/bin/python

# import utmconv class
from transverse_mercator_py.utm import utmconv
from math import pi, cos, hypot
from std_msgs.msg import Char
import rospy

from Communication.msg import GPS
from markerLocator.msg import DronePose
from time import time, sleep


Robolab_ll = (55.366856, 10.431562) # latitude, longitude

class DecisionMaker:
	def __init__(self):
		rospy.init_node('talker', anonymous=True)

		pub_droneout = rospy.get_param('~drone_out', '/communication/drone')
		self.pub = rospy.Publisher(pub_droneout, GPS, queue_size=10) ## change msg type

		sub_dronein = rospy.get_param('~pose_in', '/positions/drone')
		rospy.Subscriber(sub_dronein, DronePose, self.pose_callback)

		hmi_in = rospy.get_param('~hmi_in', '/fmHMI/keyboard')
		rospy.Subscriber(hmi_in, Char, self.hmi_callback)

		self.rate = rospy.Rate(5) #5 1hz
		self.uc = utmconv()

		# Robolab in UTM
#		(hemisphere, zone, letter, easting, northing) = uc.geodetic_to_utm (Robolab_ll)
		self.utm_offset = self.uc.geodetic_to_utm (Robolab_ll[0], Robolab_ll[1])
		(self.offset_hemisphere, self.offset_zone, self.offset_letter, self.offset_easting, self.offset_northing) = self.utm_offset
		print '\nConverted from geodetic to UTM [m]'
		print '  %d %c %.5fe %.5fn' % (self.offset_zone, self.offset_letter, self.offset_easting, self.offset_northing)

		self.last_msg_time = 0
		self.img_hz = 25

		self.utm_pose_in = (0,0)


		self.height = 20
	def hmi_callback(self, data):
		if data.data == 65:
			self.height+=1
		elif data.data == 66:
			self.height-=1

		rospy.loginfo("Height: %d" % self.height)

	def pose_callback(self, msg):
		order_match = msg.order_match
		if order_match:
			quality = msg.quality

			x = msg.x/100.0 # cm -> m
			y = msg.y/100.0 # cm -> m

#			x = 0.10
#			y = 0.10
#			print "Local pos: ", x, y
			self.utm_pose_in = (float(self.offset_easting) + x), (float(self.offset_northing) + y) #easting, northing

			self.last_msg_time = time()

#    def utm_to_geodetic (self, hemisphere, zone, easting, northing):
#	def utm_to_ll(self, utm):
#		hemisphere = 
#		return self.uc.utm_to_geodetic (self.utm_offset[3], self.utm_offset[1], utm[0], utm[1])


	def spin(self):
		while not rospy.is_shutdown():

			now = time()
			if(now - self.last_msg_time) < 1.0/self.img_hz:
				rospy.loginfo("%s: Drone locked" % rospy.get_name())

				# Manipulate drones position
				utm_pose_out = self.utm_pose_in


				ll_pose_out = self.uc.utm_to_geodetic(self.offset_hemisphere, self.offset_zone, utm_pose_out[0], utm_pose_out[1])

				print "Dist from offset: ", hypot(utm_pose_out[0] - self.offset_easting, utm_pose_out[1] - self.offset_northing)

				print "drone position: ", ll_pose_out

				gps = GPS()
				gps.lat = ll_pose_out[0]
				gps.lon = ll_pose_out[1]
				gps.height = self.height
#				gps.DOP = 2

				self.pub.publish(gps)
			else:
				rospy.logwarn("%s:No drone position" % rospy.get_name())

			self.rate.sleep()
if __name__ == '__main__':
	decisionMaker = DecisionMaker()
	decisionMaker.spin()
