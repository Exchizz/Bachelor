# -*- coding: utf-8 -*-
"""
Created on Tue May 13 19:38:43 2014

@author: henrik
"""

class MarkerPose:
    def __init__(self, x, y, theta, quality, order = None, order_match = -1):
        self.x = x
        self.y = y
        self.theta = theta
        self.quality = quality
        self.order = order
	self.order_match = order_match
