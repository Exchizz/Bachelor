#!/usr/bin/python


'''
Test code to communicate with AutQuad using CAN

Requirements to run:
sudo pip install python-can

You will need to change the name of the CAN-interface to make it work.
If you can't find the name of the interface in 'ifconfig', you might be missing loading one or more kernel-modules (pcan, vcan ect. It depends on your CAN hardware)
'''

from AutoQuadNode import AutoQuadNode
from CanMessage import CanMessage
from time import sleep


class Me:
    pass

CAN_TYPE_SENSOR = '\x03'

if __name__ == "__main__":
    me = Me()
    autoquadNode = AutoQuadNode('can1', 'socketcan')

    #Wait for AQ to send reset-msg
    autoquadNode.WaitForReset(timeout=1000);
    print "Recevied readymsg"

    msg = autoquadNode.RegisterNode(CAN_TYPE_SENSOR,1) # (type,canId)

    #Wait for telemetryTryValue
    msg = autoquadNode.recv()
    msg = CanMessage(msg)
    print msg
    autoquadNode.AnswerRequestTelemValue(msg)

    msg = autoquadNode.recv()
    msg = CanMessage(msg)
    autoquadNode.AnswerRequestTelemRate(msg)

    #Wait for telemetryTryRate
    #msg = autoquadNode.recv()
    #print "request rate: ", msg
    #msg = autoquadNode.AnswerRequestTelemValue()

    #print "Registration complete"
    #print msg
    #sleep(0.5)
    #me.source_id = msg.get_target_id()
    #msg = autoquadNode.ReqistrerTelem(CAN_TYPE_SENSOR, 1) # (type, canId)
    #print msg