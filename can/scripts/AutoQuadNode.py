__author__ = 'exchizz'

from CanInterface import CanInterface
from CanMessage import CanMessage


class AutoQuadNode(CanInterface):
    def __init__(self, iface, type):
        # Call base constructor
        CanInterface.__init__(self, iface, type)

    def RegisterNode(self, type, canId):
        # ...1c... = register node, can.h
        # Little endian, mhmh
        self.send(0x01c00000, ['\xEF','\xCD','\xAB','\x89',type,canId,'\x23','\x01'])

        # Get ACK msg (if any)
        msg = self.recv()

        #Throws exception if msg is None = we haven't received an msg
        try:
            assert(msg != None)

            print "Rx MSG: ", msg
            obj = CanMessage(msg)
            return obj

        except AssertionError:
            print ("Unable to register node")

    def ReqistrerTelem(self, type):
        # ...1c... = register telem, can.h
        # Little endian, mhmh
        self.send(0x02c00000, ['\xEF','\xCD','\xAB','\x89',type,'\x45','\x23','\x01'])

        # Get ACK msg (if any)
        msg = self.recv()

        #Throws exception if msg is None = we haven't received an msg
        try:
            assert(msg != None)

            print "Rx MSG: ", msg
            obj = CanMessage(msg)
            return obj

        except AssertionError:
            exit("Unable to TX msg")