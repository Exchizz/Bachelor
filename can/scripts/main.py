#!/usr/bin/python


'''
Test code to communicate with AutQuad using CAN

Requirements to run:
sudo pip install python-can

You will need to change the name of the CAN-interface to make it work.
If you can't find the name of the interface in 'ifconfig', you might be missing loading one or more kernel-modules (pcan, vcan ect. It depends on our CAN hardware)
'''

from AutoQuadNode import AutoQuadNode

if __name__ == "__main__":
    autoquadNode = AutoQuadNode('can0', 'socketcan')

    try:
        print "Registering node"
        msg = autoquadNode.RegisterNode()
        print "Registration complete"

        print "Binary ID:       ", msg.get_id_binary()
        print "Binary data:     ", msg.get_data_binary()
        print "Function ID:     ", msg.get_function_id()
        print "Target type:     ", msg.get_target_type()
        print "Logical Com. Ch: ", msg.get_logical_communications_channel()
        print "Target ID:       ", msg.get_target_id()
        print "Sequence ID:     ", msg.get_sequence_id()
        print "UUID data (HEX): ", msg.get_uuid_data()

    except AssertionError:
        exit("Unable to register node")