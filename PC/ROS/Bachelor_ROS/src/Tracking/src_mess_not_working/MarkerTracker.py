# -*- coding: utf-8 -*-
"""
Marker tracker for locating n-fold edges in images using convolution.

@author: Henrik Skov Midtiby
"""
import cv2.cv as cv
import cv2
import numpy as np
import math
from time import sleep

from skimage.measure import structural_similarity as ssim

class MarkerTracker:
    '''
    Purpose: Locate a certain marker in an image.
    '''
    def __init__(self, order, kernelSize, scaleFactor):
        self.kernelSize = kernelSize

        (kernelReal, kernelImag) = self.generateSymmetryDetectorKernel(order, kernelSize)
        self.order = order
	self.order_match = False
        self.matReal = cv.CreateMat(kernelSize, kernelSize, cv.CV_32FC1)
        self.matImag = cv.CreateMat(kernelSize, kernelSize, cv.CV_32FC1)
        for i in range(kernelSize):
            for j in range(kernelSize):
                self.matReal[i, j] = kernelReal[i][j] / scaleFactor
                self.matImag[i, j] = kernelImag[i][j] / scaleFactor
        self.lastMarkerLocation = (None, None)
        self.orientation = None

        (kernelRealThirdHarmonics, kernelImagThirdHarmonics) = self.generateSymmetryDetectorKernel(3*order, kernelSize)
        self.matRealThirdHarmonics = cv.CreateMat(kernelSize, kernelSize, cv.CV_32FC1)
        self.matImagThirdHarmonics = cv.CreateMat(kernelSize, kernelSize, cv.CV_32FC1)
        for i in range(kernelSize):
            for j in range(kernelSize):
                self.matRealThirdHarmonics[i, j] = kernelRealThirdHarmonics[i][j] / scaleFactor
                self.matImagThirdHarmonics[i, j] = kernelImagThirdHarmonics[i][j] / scaleFactor

	# Create kernel used to remove arm in quality-measure
	(kernelRemoveArmReal, kernelRemoveArmImag) = self.generateSymmetryDetectorKernel(1, kernelSize)
	self.kernelComplex = np.array(kernelReal + 1j*kernelImag, dtype=complex)
	self.KernelRemoveArmComplex = np.array(kernelRemoveArmReal + 1j*kernelRemoveArmImag, dtype=complex)

	# Values used in quality-measure
	absolute = np.absolute(self.kernelComplex)
	self.threshold = 0.4*absolute.max()

        self.quality = 0
	self.y1 = int(math.floor(float(self.kernelSize)/2))
	self.y2 = int(math.ceil(float(self.kernelSize)/2))

	self.x1 = int(math.floor(float(self.kernelSize)/2))
	self.x2 = int(math.ceil(float(self.kernelSize)/2))

                  
    def generateSymmetryDetectorKernel(self, order, kernelsize):
        valueRange = np.linspace(-1, 1, kernelsize);
        temp1 = np.meshgrid(valueRange, valueRange)
        kernel = temp1[0] + 1j*temp1[1];
            
        magni = abs(kernel);
        kernel = kernel**order;
        kernel = kernel*np.exp(-8*magni**2);
         
        return (np.real(kernel), np.imag(kernel))

    def allocateSpaceGivenFirstFrame(self, frame):
        self.newFrameImage32F = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_32F, 3)
        self.frameReal = cv.CreateImage ((frame.width, frame.height), cv.IPL_DEPTH_32F, 1)
        self.frameImag = cv.CreateImage ((frame.width, frame.height), cv.IPL_DEPTH_32F, 1)
        self.frameRealThirdHarmonics = cv.CreateImage ((frame.width, frame.height), cv.IPL_DEPTH_32F, 1)
        self.frameImagThirdHarmonics = cv.CreateImage ((frame.width, frame.height), cv.IPL_DEPTH_32F, 1)
        self.frameRealSq = cv.CreateImage ((frame.width, frame.height), cv.IPL_DEPTH_32F, 1)
        self.frameImagSq = cv.CreateImage ((frame.width, frame.height), cv.IPL_DEPTH_32F, 1)
        self.frameSumSq = cv.CreateImage ((frame.width, frame.height), cv.IPL_DEPTH_32F, 1)


	self.quality_match = cv.CreateImage((1,1), cv.IPL_DEPTH_32F, 1)
    
    def locateMarker(self, frame):
        self.frameReal = cv.CloneImage(frame)
        self.frameImag = cv.CloneImage(frame)
        self.frameRealThirdHarmonics = cv.CloneImage(frame)
        self.frameImagThirdHarmonics = cv.CloneImage(frame)

        # Calculate convolution and determine response strength.
        cv.Filter2D(self.frameReal, self.frameReal, self.matReal) # src, dst, kernel
        cv.Filter2D(self.frameImag, self.frameImag, self.matImag) # src, dst, kernel

        cv.Mul(self.frameReal, self.frameReal, self.frameRealSq) # src, src, dst
        cv.Mul(self.frameImag, self.frameImag, self.frameImagSq) # src, src, dst
        cv.Add(self.frameRealSq, self.frameImagSq, self.frameSumSq)

        # Calculate convolution of third harmonics for quality estimation.
        cv.Filter2D(self.frameRealThirdHarmonics, self.frameRealThirdHarmonics, self.matRealThirdHarmonics)
        cv.Filter2D(self.frameImagThirdHarmonics, self.frameImagThirdHarmonics, self.matImagThirdHarmonics)
        
        min_val, max_val, min_loc, max_loc = cv.MinMaxLoc(self.frameSumSq)
        self.lastMarkerLocation = max_loc
        (xm, ym) = max_loc
        self.determineMarkerOrientation(frame)
	self.determineMarkerQuality(frame)

        return max_loc

    def determineMarkerOrder(self, img_small):

        (xm, ym) = self.lastMarkerLocation
	searchDist = self.kernelSize / 2

	# Order is defined as 1+number of black arms
	detectedOrder = 1

	for order in xrange(self.order):
		angle1 = self.orientation + order*2*math.pi/self.order
		angle1 = self.limitAngleToRange(angle1)


		w,h = cv.GetSize(img_small)

		xm2 = int(xm + searchDist*math.cos(angle1))
		ym2 = int(ym + searchDist*math.sin(angle1))

		if ym2 < 0 or xm2 < 0:
			print "less than zero, line 127"
			
		if ym2 > h or xm2 > w:
			if ym2 > h:
				ym2 = h-1

			if xm2 > w:
				xm2 = w-1
		try:
			intensity = img_small[ym2, xm2]

			if intensity < 100:
				detectedOrder +=1
		except:
			pass
#			img_small[ym2-1, xm2-1] = 128
#			img_small[ym2, xm2] = 128
#			img_small[ym2+1, xm2+1] = 128

	return detectedOrder
	#cv.SaveImage("output/detect_order.png", img_small)

    def determineMarkerQuality(self, frame):

	phase = np.exp((self.limitAngleToRange(-self.orientation))*1j)
	angleThreshold = 3.14/(2*self.order)

	t1 = (self.kernelComplex*np.power(phase, self.order)).real > self.threshold
	t2 = (self.kernelComplex*np.power(phase, self.order)).real < -self.threshold

	img_t1_t2_diff = t1.astype(np.int8)-t2.astype(np.int8)

	t3 = np.angle(self.KernelRemoveArmComplex * phase) < angleThreshold
	t4 = np.angle(self.KernelRemoveArmComplex * phase) > -angleThreshold

	mask = 1-2*(t3 & t4)
	temp = img_t1_t2_diff * mask

	template = 127+(1-temp*127)

	(xm, ym) = self.lastMarkerLocation
	try:
		y1 = ym-self.y1 if ym-self.y1 > 0 else 0

		y2 = ym+self.y2

		x1 = xm-self.x1 if xm-self.x1 > 0 else 0
		x2 = xm+self.x2

			
		frame_tmp = np.array(frame[y1:y2, x1:x2])
	except(TypeError):
		print ym-self.y1, ym+self.y2, xm-self.x1, xm+self.x2
		print "error"
		self.quality = 0.0
		exit(1)

	img_small = cv.fromarray( frame_tmp.astype( np.uint8 )  )


	frame_w, frame_h = cv.GetSize(img_small)
	template = template[0:frame_h, 0:frame_w].copy()
	img_template = cv.fromarray( template.astype( np.uint8 ) )

	if True:
#		cv.ShowImage("temp_kernel", img_template)
#		cv.ShowImage("small_image", img_small)

		matches = 0.0
		px_count = 0

		w,h = cv.GetSize(img_small)
		for x in xrange(w):
			for y in xrange(h):
				if img_template[y, x] != 128: # Don't pay attention to the gray area
					px_count+=1
					if math.fabs(img_small[y, x] - img_template[y, x]) < 70:
						matches+=1

		self.quality = matches/(px_count)
##		self.quality = 1

		if self.quality > 0.3:
			determinedOrder = self.determineMarkerOrder(frame)
			#print determinedOrder
			if self.order != determinedOrder:
				print "Wrong order ", self.order, determinedOrder
				self.quality = 0.0
			else:
				self.order_match = True
		else:
			print "\t quality: ", self.quality

    def determineMarkerOrientation(self, frame):
        (xm, ym) = self.lastMarkerLocation
        realval = cv.Get2D(self.frameReal, ym, xm)[0]
        imagval = cv.Get2D(self.frameImag, ym, xm)[0]
        self.orientation = (math.atan2(-realval, imagval) - math.pi / 2) / self.order

        maxValue = 0
        maxOrient = 0
        searchDist = self.kernelSize / 3
        for k in range(self.order):
            orient = self.orientation + 2 * k * math.pi / self.order
            xm2 = int(xm + searchDist*math.cos(orient))
            ym2 = int(ym + searchDist*math.sin(orient))
            if(xm2 > 0 and ym2 > 0 and xm2 < frame.width and ym2 < frame.height):
                try:
                    intensity = cv.Get2D(frame, ym2, xm2)
                    if(intensity[0] > maxValue):
                        maxValue = intensity[0]
                        maxOrient = orient
                except:
                    print("determineMarkerOrientation: error: %d %d %d %d" % (ym2, xm2, frame.width, frame.height))
                    pass

        self.orientation = self.limitAngleToRange(maxOrient)

    def limitAngleToRange(self, angle):
        while(angle < math.pi):
            angle += 2*math.pi
        while(angle > math.pi):
            angle -= 2*math.pi
        return angle
