#!/usr/bin/python


'''
Test code to communicate with AutQuad using CAN

Requirements to run:
sudo pip install python-can

You will need to change the name of the CAN-interface to make it work.
If you can't find the name of the interface in 'ifconfig', you might be missing loading one or more kernel-modules (pcan, vcan ect. It depends on our CAN hardware)
'''

from AutoQuadNode import AutoQuadNode
from CanInterface import CanInterface

CAN_FID_GRANT_ADDR = 0x8


if __name__ == "__main__":
    autoquadNode = AutoQuadNode('can0', 'socketcan')

    try:
        print "Registering node"
        msg = autoquadNode.RegisterNode()
        print "Registration complete"

        print "Binary ID:   ", msg.get_data_binary()
        print "Binary data: ", msg.get_id_binary()
        print "Function ID: ", msg.get_fid()

    except AssertionError:
        exit("Unable to register node")