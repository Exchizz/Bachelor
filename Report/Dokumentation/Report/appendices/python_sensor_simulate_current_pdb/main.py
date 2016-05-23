#!/usr/bin/python

'''
Written by Mathias Neerup
manee12@student.sdu.dk

Test code to communicate with AutQuad using CAN

Requirements to run:
sudo pip install python-can

You will need to change the name of the CAN-interface to make it work.
If you can't find the name of the interface in 'ifconfig', you might be missing loading one or more kernel-modules (pcan, vcan ect. It depends on your CAN hardware)
'''

from AutoQuadNode import AutoQuadNode
from CanMessage import CanMessage
from time import sleep


CAN_TYPE_SENSOR = '\x03'

if __name__ == "__main__":
        autoquadNode = AutoQuadNode('can1', 'socketcan')

        #Wait for AQ to send reset-msg
        autoquadNode.WaitForReset(timeout=1000);
        print "Recevied readymsg"

        msg = autoquadNode.RegisterNode(CAN_TYPE_SENSOR,1) # (type,canId)


        #Wait for telemetryTryValue
        msg = autoquadNode.recv()
        msg = CanMessage(msg)

        autoquadNode.AnswerRequestTelemValue(msg)

        msg = autoquadNode.recv()
        msg = CanMessage(msg)
        autoquadNode.AnswerRequestTelemRate(msg)

        while True:
            autoquadNode.ReqistrerTelem(CAN_TYPE_SENSOR, 0) # (type, canId()) CAN_SENSORS_PDB_BATA = 1
            sleep(0.1)
