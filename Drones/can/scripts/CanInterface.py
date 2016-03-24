#!/usr/bin/python
import can
__author__ = 'Mathias Neerup'


class CanInterface:
        def __init__(self, iface, type):
                self.bus = can.interface.Bus(iface, bustype=type)

        def send(self,extended_id, payload):
                msg = can.Message(arbitration_id=extended_id, data=payload, extended_id=True)
                print "Tx MSG: ", msg
                if self.bus.send(msg) < 0:
                        exit("Unable to send, stopping")
                #else:
                #        print("Message sent")

        def recv(self, timeout = 5):
                return self.bus.recv(timeout = timeout)

