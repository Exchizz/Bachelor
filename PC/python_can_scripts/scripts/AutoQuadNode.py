__author__ = 'exchizz'

from CanInterface import CanInterface
from CanMessage import CanMessage
from struct import pack
from defines import *
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

    def SendCMD(self, cmd = '', doc = '0', seqid = '0', sourceid = 0):
        # DOC = Data object code
        # data = [0,1,2,3,4,5,6,7,8]
        self.send(0x00000000 | CAN_FID_CMD | seqid | cmd | sourceid << 11, ['\x00','\xCD','\xAB','\x89','\x78', '\x45','\x23','\x01'])



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
        self.phase +=1

        self.phase = self.phase % 20
        sensor_value_float = pack('>f', sensor_value)
        #print sensor_value
        data_float = [int(ord(elm)) for elm in sensor_value_float]

        #list2 = [elm.replace('0x',r'x') for elm in data_float]
        data_float.reverse()
        data_float.extend([type, canId,'\x00','\x00'])
        #print "data: ", data_float
        #self.send(0x02C00800, ['\x00','\x00','\x00','\x01',type, canId,'\x00','\x00']) # Hardcoded sid to 1
        self.send(0x02C00800, data_float)

        # Get ACK msg (if any)
        #msg = self.recv()

        #Throws exception if msg is None = we haven't received an msg
        #try:
        #    assert(msg != None)

        #    print "Rx MSG: ", msg
        #    obj = CanMessage(msg)
        #    return obj

        #except AssertionError:
        #    exit("Got no response")