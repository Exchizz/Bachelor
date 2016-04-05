import numpy as np
import cv2

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape)[:2]/2)
  rot_mat = cv2.getRotationMatrix2D( image_center, angle, scale=1)
  result = cv2.warpAffine(image, rot_mat, tuple(np.array(image.shape)[:2]),flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))
  return result


image = cv2.imread("marker.png")


for i in range(180):
	image_rotated = rotateImage(image,i)
	cv2.imwrite("marker_rotated" + str(i) + ".png", image_rotated)
