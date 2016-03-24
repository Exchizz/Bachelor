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
from defines import *


class Me:
    pass


telemetry = 0

if __name__ == "__main__":
        me = Me()
        autoquadNode = AutoQuadNode('can0', 'socketcan')

        #Wait for AQ to send reset-msg
        autoquadNode.WaitForReset(timeout=1000);
        print "Recevied reset_msg"

        msg = autoquadNode.RegisterNode(CAN_TYPE_OSD, 1) # (type,canId)

        seq = msg.get_sequence_id()
        sourceid = msg.get_target_id()
        print msg
        #autoquadNode.SendCMD(cmd = CAN_CMD_TELEM_VALUE, doc = CAN_CMD_TELEM_VALUE, seqid = seq, sourceid = sourceid)


        #print msg
        exit()

        #Wait for telemetryTryValue
        msg = autoquadNode.recv()
        msg = CanMessage(msg)
        print msg
        autoquadNode.AnswerRequestTelemValue(msg)

        msg = autoquadNode.recv()
        msg = CanMessage(msg)
        print msg
        autoquadNode.AnswerRequestTelemRate(msg)
        print "Registering as TELEM"
        autoquadNode.SendCMD(CAN_CMD_TELEM_VALUE)

        #while True:
        #    autoquadNode.ReqistrerTelem(CAN_TYPE_SENSOR, 0) # (type, canId())CAN_SENSORS_PDB_BATA = 0
        #    sleep(0.1)
            #print "tx msg"