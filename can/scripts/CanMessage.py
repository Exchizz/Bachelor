__author__ = 'exchizz'


class CanMessage:
    def __init__(self, msg):
        self.msg = msg

    def get_data_binary(self):
        # Returns msg's data as binary string
        data_string = ''.join(["%.2x" % byte for byte in self.msg.data])
        data_binary = "{:*>64b}".format(int(data_string, 16))
        return data_binary

    def get_id_binary(self):
        # Returns msg's id as binary string
        id_string = "%.8x" % self.msg.arbitration_id
        id_binary = "{:0>29b}".format(int(id_string, 16))
        return id_binary

    def get_function_id(self):
        # Returns msg's fid
        rxId = self.get_id_binary()
        fid = int(rxId[3:7],2) # Function ID [25:22] (Left to right) (Right to Left: 29 - 22  = 7, 29-25-1(first not included in python) = 3, from 3 to 7)
        return fid

    def get_target_type(self):
        rxId = self.get_id_binary()
        ttype = int(rxId[2:3],2) # Function ID [25:22] (Left to right) (Right to Left: 29 - 22  = 7, 29-25-1(first not included in python) = 3, from 3 to 7)
        return ttype

    def get_logical_communications_channel(self):
        rxId = self.get_id_binary()
        llc = int(rxId[2],2) # Get two first bits [28:27]
        return llc

    def get_target_id(self):
        rxId = self.get_id_binary()
        tid = int(rxId[18:23],2) # Get two first bits [28:27]
        return tid

    def get_sequence_id(self):
        rxId = self.get_id_binary()
        seqid = int(rxId[-6:],2) # Get two first bits [28:27]
        return seqid
