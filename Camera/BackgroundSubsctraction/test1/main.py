import cv2
import numpy as np
from time import time, strftime

#cam=cv2.VideoCapture('floor_sun_waveing_foot.mkv')
cam=cv2.VideoCapture('recording_flight_with_5_marker_afternoon.mkv')
#fgbg = cv2.BackgroundSubtractorMOG(history=10,nmixtures=3,backgroundRatio=0.9)
fgbg = cv2.BackgroundSubtractorMOG()

f,img=cam.read()
avg = np.float32(img)

while(cam.isOpened):
	f,img = cam.read()
#	cv2.accumulateWeighted(img, avg, 0.3)
#	res1 = cv2.convertScaleAbs(avg)

#	cv2.imshow('Filter',res1)
	fgmask = fgbg.apply(img)
#	cv2.imshow('Res1',fgmask)

	res = cv2.bitwise_and(img, img, mask = fgmask)
	cv2.imshow('Original',img)
	cv2.imshow('No background',res)
#	if(cv2.waitKey(27)!=-1):
#		 cam.release()
#		 cv2.destroyAllWindows()

# Listen for keyboard events and take relevant actions.
        if cv2.waitKey(20) & 0xFF == 115: # s
            # save image
            print("Saving image")
            filename = strftime("%Y-%m-%d %H-%M-%S")
            cv2.imwrite("bg_fg_%s.png" % filename, img)
            cv2.imwrite("fg_%s.png" % filename, res)

