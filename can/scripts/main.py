#!/usr/bin/python


'''
Test code to communicate with AutQuad using CAN

Requirements to run:
sudo pip install python-can

You will need to change the name of the CAN-interface to make it work.
If you can't find the name of the interface in 'ifconfig', you might be missing loading one or more kernel-modules (pcan, vcan ect. It depends on our CAN hardware)
'''
from struct import unpack, pack
from CanInterface import CanInterface


class AutoQuadNode(CanInterface):
    def __init__(self, iface, type):
        # Call base constructor
        CanInterface.__init__(self, iface, type)

    def RegisterNode(self):
        # ...1c... = register node, can.h
        # Little endian, mhmh
        self.send(0x01c00000, ['\x67','\x45','\x23','\x01'])

        # Get ACK msg (if any)
        msg = self.recv()

        #Throws exception if msg is None = we haven't received an msg
        assert(msg != None)

        print "Rx MSG: ", msg

        data_string = ''.join(["%.2x" % byte for byte in msg.data])
        data_binary = "{:*>64b}".format(int(data_string, 16))

        id_string = "%.8x" % msg.arbitration_id
        id_binary = "{:*>29b}".format(int(id_string, 16))

        return data_binary, id_binary


if __name__ == "__main__":
    autoquadNode = AutoQuadNode('can0', 'socketcan')

    try:
        print "Registering node"
        rspData, rspId = autoquadNode.RegisterNode()
        print "Registration complete"

        print "Binary ID:   ", rspId
        print "Binary data: ", rspData


        rspInteger = int(rspData.replace('*',''), 2)

        print rspInteger & 0x1
    except AssertionError:
        exit("Unable to register node")