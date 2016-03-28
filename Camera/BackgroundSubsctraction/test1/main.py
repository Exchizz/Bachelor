import cv2
import numpy as np
cam=cv2.VideoCapture(0)
#cam=cv2.VideoCapture('floor_sun_waving_food.mkv')
fgbg = cv2.BackgroundSubtractorMOG()

f,img=cam.read()
avg = np.float32(img)

while(cam.isOpened):
	f,img = cam.read()
	cv2.accumulateWeighted(img, avg, 0.3)
	res1 = cv2.convertScaleAbs(avg)

#	cv2.imshow('Original',res1)
	fgmask = fgbg.apply(res1)
#	cv2.imshow('Res1',fgmask)

	res = cv2.bitwise_and(img, img, mask = fgmask)
	cv2.imshow('Original',img)
	cv2.imshow('No background',res)
	if(cv2.waitKey(27)!=-1):
		 cam.release()
		 cv2.destroyAllWindows()
