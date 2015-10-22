__author__ = 'exchizz'

from CanInterface import CanInterface
from CanMessage import CanMessage


class AutoQuadNode(CanInterface):
    def __init__(self, iface, type):
        # Call base constructor
        CanInterface.__init__(self, iface, type)

    def RegisterNode(self):
        # ...1c... = register node, can.h
        # Little endian, mhmh
        self.send(0x01c00000, ['\x67','\x45','\x23','\x03'])

        # Get ACK msg (if any)
        msg = self.recv()

        #Throws exception if msg is None = we haven't received an msg
        assert(msg != None)

        print "Rx MSG: ", msg

        #rxData = self.get_data_binary()
        #rxDataInt = int(rxData.replace('*',''), 2)
        obj = CanMessage(msg)
        return obj