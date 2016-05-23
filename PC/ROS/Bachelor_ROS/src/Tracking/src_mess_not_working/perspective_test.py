#!/usr/bin/python
from PerspectiveTransform import PerspectiveCorrecter
from math import hypot

pointLocationsInImage = [[952, 533], [946, 3], [1668, 3], [1667, 527]]
realCoordinates = [[0, 0], [0, 109], [150.1, 109], [150.1, 0]]
perspectiveConverter = PerspectiveCorrecter(pointLocationsInImage, realCoordinates)



# not image 14 in /home/exchizz/
px_pkt = (208,377)
meter_pktl = perspectiveConverter.convert(px_pkt)

px_pkt = (95,319)
meter_pktr = perspectiveConverter.convert(px_pkt)


distance = hypot(meter_pktl[0] - meter_pktr[0],meter_pktl[1] - meter_pktr[1])

print "Test 1 distance is: ", distance,  " error: ", 50-distance

exit()
# Image 15
px_pkt = (925,689)
meter_pktl = perspectiveConverter.convert(px_pkt)

px_pkt = (1246,839)
meter_pktr = perspectiveConverter.convert(px_pkt)


distance = hypot(meter_pktl[0] - meter_pktr[0],meter_pktl[1] - meter_pktr[1])

print "pkt1: ", meter_pktl, " : ", meter_pktr, "Test 2 distance is: ", distance,  " error: ", 75-distance
