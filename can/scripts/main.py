#!/usr/bin/python


'''
Test code to communicate with AutQuad using CAN

Requirements to run:
sudo pip install python-can

You will need to change the name of the CAN-interface to make it work.
If you can't find the name of the interface in 'ifconfig', you might be missing loading one or more kernel-modules (pcan, vcan ect. It depends on our CAN hardware)
'''
from struct import unpack
from CanInterface import CanInterface


class AutoQuadNode(CanInterface):
    def __init__(self, iface, type):
        # Call base constructor
        CanInterface.__init__(self, iface, type)

    def RegisterNode(self):
        # ...1c... = register node, can.h
        self.send(0x01c00000, unpack('<BBBBBBBB','\x01\x23\x45\x67\x89\xAB\xCD\xEF'))

        # Get ACK msg (if any)
        msg = self.recv()

        #Throws exception if msg is None = we haven't received an msg
        assert(msg != None)

        return msg


if __name__ == "__main__":
        autoquadNode = AutoQuadNode('can0', 'socketcan')

    try:
        print "Registering node"
        rsp = autoquadNode.RegisterNode()
        print "Registration complete"
        print rsp
    except AssertionError:
        exit("Unable to register node")