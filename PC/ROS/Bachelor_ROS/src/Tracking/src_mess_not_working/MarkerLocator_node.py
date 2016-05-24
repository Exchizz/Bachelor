#!/usr/bin/env python
from time import time, strftime
import sys
import os

import numbers
import cv
import cv2
import math
import numpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from ImageAnalyzer import ImageAnalyzer
from TrackerInWindowMode import TrackerInWindowMode
from PerspectiveTransform import PerspectiveCorrecter
from MarkerPose import MarkerPose
from markerLocator.msg import DronePose

import signal



'''
2012-10-10
Script developed by Henrik Skov Midtiby (henrikmidtiby@gmail.com).
Provided for free but use at your own risk.

2013-02-13
Structural changes allows simultaneous tracking of several markers.
Frederik Hagelskjaer added code to publish marker locations to ROS.
'''

PublishToROS = True

if PublishToROS:
    import rospy
    from geometry_msgs.msg import Point

class CameraDriver:
    '''
    Purpose: capture images from a camera and delegate procesing of the
    images to a different class.
    '''
    def __init__(self, markerOrder = 4, defaultKernelSize = 21, scalingParameter = 2500):
        # Initialize camera driver.
        # Open output window.
#        cv.NamedWindow('filterdemo', cv.CV_WINDOW_NORMAL)
#	cv.NamedWindow('temp_kernel', cv.CV_WINDOW_NORMAL)
#	cv.NamedWindow('small_image', cv.CV_WINDOW_NORMAL)

#        self.setResolution()


        # Storage for image processing.
        self.currentFrame = None
        self.processedFrame = None
        self.running = True
        # Storage for trackers.
        self.trackers = []
        self.windowedTrackers = []
        self.oldLocations = []
        # Initialize trackers.
#        for markerOrder in markerOrders:
        temp = ImageAnalyzer(downscaleFactor=1)
        temp.addMarkerToTrack(markerOrder, defaultKernelSize, scalingParameter)
        self.trackers.append(temp)
        self.windowedTrackers.append(TrackerInWindowMode(markerOrder, defaultKernelSize))
        self.oldLocations.append(MarkerPose(None, None, None, None))
        self.cnt = 0
        self.defaultOrientation = 0

    def setFocus(self):
        # Disable autofocus
        os.system('v4l2-ctl -d '+str(self.cameraDevice)+' -c focus_auto=0')
        
        # Set focus to a specific value. High values for nearby objects and
        # low values for distant objects.
        os.system('v4l2-ctl -d ' + str(self.cameraDevice) + ' -c focus_absolute=0')

        # sharpness (int)    : min=0 max=255 step=1 default=128 value=128
        os.system('v4l2-ctl -d ' + str(self.cameraDevice) + ' -c sharpness=200') # default 200

    
    def setResolution(self):
#        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
#        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
        #cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_WIDTH, 2304)
        #cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_HEIGHT, 1536)

    def getImage(self):
        # Get image from camera.
       	self.currentFrame = cv.QueryFrame(self.camera)

    def processFrame(self, currentFrame):
        # Locate all markers in image.
	self.currentFrame = currentFrame

	for k in range(len(self.trackers)):
#            if(self.oldLocations[k].x is None or self.oldLocations[k].quality < 0.4 and self.oldLocations[k].quality != 0 ):
            if self.oldLocations[k].x is None  or self.oldLocations[k].quality < 0.3:
                # Previous marker location is unknown, search in the entire image.
#		print "Lost track of marker, searching entire image"
                self.processedFrame = self.trackers[k].analyzeImage(self.currentFrame)
                markerX = self.trackers[k].markerLocationsX[0]
                markerY = self.trackers[k].markerLocationsY[0]
                order = self.trackers[k].markerTrackers[0].order
		quality = self.trackers[k].markerTrackers[0].quality
		order_match = self.trackers[k].markerTrackers[0].order_match
                self.oldLocations[k] = MarkerPose(markerX, markerY, self.defaultOrientation, quality, order, order_match)
            else:
                # Search for marker around the old location.
                self.windowedTrackers[k].cropFrame(self.currentFrame, self.oldLocations[k].x, self.oldLocations[k].y)
                self.oldLocations[k] = self.windowedTrackers[k].locateMarker()
                self.windowedTrackers[k].showCroppedImage()


    def publishImageFrame(self, RP):
        im = numpy.asarray(self.currentFrame[:,:])
        RP.publishImage(im)

    def drawDetectedMarkers(self):
        for k in xrange(len(self.trackers)):
            xm = self.oldLocations[k].x
            ym = self.oldLocations[k].y
            orientation = self.oldLocations[k].theta
            cv.Circle(self.processedFrame, (xm, ym), 4, (55, 55, 255), 2)
            xm2 = int(xm + 50*math.cos(orientation))
            ym2 = int(ym + 50*math.sin(orientation))
            cv.Line(self.processedFrame, (xm, ym), (xm2, ym2), (255, 0, 0), 2)

    def showProcessedFrame(self):
        #cv.ShowImage('filterdemo', self.processedFrame)
	pass
    def resetAllLocations(self):
        # Reset all markers locations, forcing a full search on the next iteration.
        for k in range(len(self.trackers)):
            self.oldLocations[k] = MarkerPose(None, None, None, None)

        
    def handleKeyboardEvents(self):
        # Listen for keyboard events and take relevant actions.
        key = cv.WaitKey(20) 
        # Discard higher order bit, http://permalink.gmane.org/gmane.comp.lib.opencv.devel/410
        key = key & 0xff
        if key == 27: # Esc
            self.running = False
        if key == 114: # R
            print("Resetting")
            self.resetAllLocations()
        if key == 115: # S
            # save image
            print("Saving image")
            filename = strftime("%Y-%m-%d %H-%M-%S")
	    print self.currentFrame
            cv.SaveImage("output/%s.png" % filename, self.currentFrame)

    def returnPositions(self):
        # Return list of all marker locations.
        return self.oldLocations

class ROS:
    def __init__(self):
        # Instantiate ros publisher with information about the markers that
        # will be tracked.

        rospy.init_node('FrobitLocator')
	self.toFind = rospy.get_param( '~to_find', 4)
	rospy.logwarn("Looking for drone order: %d" % self.toFind);
        self.pub = None
#        self.markers = self.toFind
        self.bridge = CvBridge()


	pose_out = rospy.get_param( '~pose_out', 'pose')
        self.pub = rospy.Publisher(pose_out, DronePose, queue_size = 10)

        self.imagePub = rospy.Publisher("imagePublisher", Image, queue_size=10)

	topic_camera_in = rospy.get_param( '~camera_in', '/camera/stream')
	self.image_sub = rospy.Subscriber(topic_camera_in,Image,self.callbackFrame)

	self.newFrame = False
	self.frame = None


	self.cd = CameraDriver(self.toFind, defaultKernelSize = 25)
     

#	pointLocationsInImage = [[1328, 340], [874, 346], [856, 756], [1300, 762]]
#	realCoordinates = [[0, 0], [300, 0], [300, 250], [0, 250]]
	pointLocationsInImage = [[952, 533], [946, 3], [1668, 3], [1667, 527]]
#	pointLocationsInImage =  [[1668, 3], [1667, 527], [952, 533], [946, 3]]
	realCoordinates = [[0, 0], [0, 109], [150.1, 109], [150.1, 0]]
	

	self.perspectiveConverter = PerspectiveCorrecter(pointLocationsInImage, realCoordinates)

#    while cd.running:
#	pass
#        cd.getImage()
#	if RP.newFrame:
#		RP.newFrame = False

    def callbackFrame(self, frame):
	try:
		source = self.bridge.imgmsg_to_cv2(frame, "bgr8")

		frame = cv.CreateImageHeader((source.shape[1], source.shape[0]), cv.IPL_DEPTH_8U, 3)
		cv.SetData( frame, source.tostring(), source.dtype.itemsize * 3 * source.shape[1] )

	except CvBridgeError as e:
		print e	

        self.cd.processFrame(frame)
        self.cd.drawDetectedMarkers()
        self.cd.showProcessedFrame()
        self.cd.handleKeyboardEvents()
	y = self.cd.returnPositions() 
	self.publishMarkerLocations(y)
	img = numpy.asarray(self.cd.processedFrame[:,:])
	self.publishImage(img)


    def publishMarkerLocations(self, locations):
#	pkt = self.perspectiveConverter.convert(px_pkt)

#	print "before homography:", locations[0].x, locations[0].y
	x,y = self.perspectiveConverter.convert( (locations[0].x, locations[0].y) )

#	print "after homography:", x, y
#	print x,y
#	print("x: %8.7f y: %8.7f angle: %8.7f quality: %8.7f order: %s lock: %d" % (x, y, locations[0].theta, locations[0].quality, locations[0].order, locations[0].order_match))
        self.pub.publish(  DronePose( x, y, locations[0].theta, locations[0].quality, locations[0].order_match )  )

    def publishImage(self, Image):
        try:
                self.imagePub.publish(self.bridge.cv2_to_imgmsg(Image, 'bgr8'))
        except CvBridgeError, e:
                print e

def signal_handler(signal, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
	rp = ROS()
	rospy.spin()

main()
