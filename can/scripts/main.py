#!/usr/bin/python


'''
Test code to communicate with AutQuad using CAN

Requirements to run:
sudo pip install python-can

You will need to change the name of the CAN-interface to make it work.
If you can't find the name of the interface in 'ifconfig', you might be missing loading one or more kernel-modules (pcan, vcan ect. It depends on our CAN hardware)
'''
import time
import can


class CanInterface:
        def __init__(self):
                self.bus = can.interface.Bus('can0', bustype='socketcan')

        def send(self,extended_id, payload):
                msg = can.Message(arbitration_id=extended_id, data=payload, extended_id=True)
                if self.bus.send(msg) < 0:
                        exit("Unable to send, stopping")
                else:
                        print("Message sent")


        def recv(self):
                return self.bus.recv(timeout = 1)



class AutoQuadNode(CanInterface):
    def __init__(self):
        # Call base constructor
        CanInterface.__init__(self)

    def RegisterNode(self):
        # ...1c... = register node, can.h
        self.send(0x01c00000, 8*'0')

        # Get ACK msg (if any)
        msg = self.recv()
        return 1 if msg else 0


if __name__ == "__main__":
    '''
                # Instantiate CanInterface
                canInterface = CanInterface()

                # Create new threads
                thread1 = CanReceiverThread(canInterface)

                # Start new Threads
                thread1.start()

                # Register as node in AQ
                canInterface.send(0x01c00000, 'A'*8)
                time.sleep(1)
                print "Exiting main()"
    '''
    autoquadNode = AutoQuadNode()
    autoquadNode.RegisterNode()