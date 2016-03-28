import cv2
import numpy as np

#c = cv2.VideoCapture('test.avi')
#_,f = c.read()
cam=cv2.VideoCapture(0)
_,f=cam.read()

avg1 = np.float32(f)

# loop over images and estimate background 
while True:
    _,f = cam.read()

    cv2.accumulateWeighted(f, avg1, 0.1)

    res1 = cv2.convertScaleAbs(avg1)

    cv2.imshow('img',f)
    cv2.imshow('avg1',res1)

    if(cv2.waitKey(27)!=-1):
	cam.release()
	cv2.destroyAllWindows()

