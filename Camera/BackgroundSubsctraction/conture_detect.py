# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
#import argparse
import datetime
#import imutils
import time
import cv2
import numpy as np

camera = cv2.VideoCapture("floor_sun_waving_food.mkv")
#camera = cv2.VideoCapture(0)

# initialize the first frame in the video stream
firstFrame = None

(grabbed, frame) = camera.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#gray = cv2.GaussianBlur(gray, (21, 21), 0)
avg = np.float32(gray)

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	(grabbed, frame) = camera.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	cv2.accumulateWeighted(gray, avg, 0.5)
	res = cv2.convertScaleAbs(avg)

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(res, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)

	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 50:
			continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


	# show the frame and record if the user presses a key
	cv2.imshow("Frame", frame)
	cv2.imshow("Frame Delta", frameDelta)
	cv2.imshow("Thresh", gray)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
