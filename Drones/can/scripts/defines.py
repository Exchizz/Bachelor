CAN_TYPE_SENSOR = '\x03'
CAN_TYPE_OSD    = '\x05'
CAN_CMD_TELEM_VALUE = 13 << 16

CAN_FID_CMD = 0x3<<22 # move 25 to left due to can.h but only 22 because CAN data registers is moved 3 to the left