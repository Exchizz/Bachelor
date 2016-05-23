#!/usr/bin/python

'''
Written by Mathias Neerup
manee12@student.sdu.dk
'''

from CanInterface import CanInterface
from CanMessage import CanMessage
from struct import pack
import numpy as np

class AutoQuadNode(CanInterface):
    def __init__(self, iface, type):
        # Call base constructor
        CanInterface.__init__(self, iface, type)

        x = np.linspace(0, 2*np.pi, 20)
        self.sinus = np.sin(x)
        self.phase = 0

    def WaitForReset(self, timeout=0):
        #Wait for AQ to send it's ready msg(my own debug msg)
        self.recv(timeout)

    def SendCMD(self):
        pass

    def RegisterNode(self, type, canId):
        # ...1c... = register node, can.h
        # Little endian, mhmh
        self.send(0x01c00000, ['\xEF','\xCD','\xAB','\x89',type, canId,'\x23','\x01'])

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

    def AnswerRequestTelemValue(self, msg):
        # Receives [0008] (4 hex, two bytes)
        index = int(msg.get_data_hex()[0:2],16)
        print "index: ", index

        value = int(msg.get_data_hex()[2:4],16)
        print "value: ", value

        doc = msg.get_data_object()
        print "doc: ", doc

        seq = msg.get_sequence_id()
        self.SendACK(seq)

    def AnswerRequestTelemRate(self, msg):
        # Receives [0008] (4 hex, two bytes)
        data = int(msg.get_data_hex()[0:2],16)
        print "data: ", data, " hz"

        doc = msg.get_data_object()
        print "doc: ", doc

        seq = msg.get_sequence_id()
        self.SendACK(seq)

    def SendACK(self, seq):
        # CAN_FID_ACK0x00 40 00 00, little endian
        self.send(0x00400000 | seq , ['\xEF','\xCD','\xAB','\x89',0, 0,'\x23','\x01'])


    def ReqistrerTelem(self, type, canId):
        # ...1c... = register telem, can.h
        # Little endian, mhmh #0x02c000
        sensor_value = self.sinus[self.phase]

	self.phase+=1
        self.phase = self.phase % 20

        sensor_value_float = pack('>f', sensor_value)

        data_float = [int(ord(elm)) for elm in sensor_value_float]

        data_float.reverse()

	# Send to AQ. id =  CAN_FID_TELEM (02c00000) | Sourceid 1 (00000800) | CAN_SENSORS_PDB_BATA (00004000)
        self.send(0x02C04800, data_float)

