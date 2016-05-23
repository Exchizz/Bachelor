/*
 * MessageCreator.h
 *
 *  Created on: Feb 4, 2016
 *      Author: exchizz
 */


#ifndef MESSAGECREATOR_H_
#define MESSAGECREATOR_H_

#include "msgs/can.h"
typedef msgs::can canMSG;

#include "Session.h"

// Function ID (Substract 3 due to ARM's way of prepending status flags)
#define CAN_FID_MASK        (0xf << (25-3 ))

#define CAN_FID_REQ_ADDR    (0x7 << (25-3))
#define CAN_FID_GRANT_ADDR  (0x8 << (25-3))
#define CAN_FID_RESET_BUS   (0x0 << (25-3))
#define CAN_FID_CMD         (0x3 << (25-3))
#define CAN_FID_GET         (0x4 << (25-3))
#define CAN_FID_REPLY       (0x6 << (25-3))
#define CAN_FID_ACK         (0x1 << (25-3))
#define CAN_FID_TELEM       (0xb << (25-3))
#define CAN_FID_SET         (0x5 << (25-3))

#define CAN_TID_MASK        (0x1f<< (9-3))

#define CAN_TT_MASK         (0x1 << (29-3))
#define CAN_TT_GROUP        (0x0 << (29-3))
#define CAN_TT_NODE         (0x1 << (29-3))

#define CAN_LCC_MASK        (0x3 << (30-3))
#define CAN_LCC_EXCEPTION   (0x0 << (30-3))
#define CAN_LCC_HIGH        (0x1 << (30-3))
#define CAN_LCC_NORMAL      (0x2 << (30-3))
#define CAN_LCC_INFO        (0x3 << (30-3))

#define CAN_SEQ_MASK        (0x3f<< (3-3))

// Source ID
#define CAN_SID_MASK        (0x1f<< (14-3))

// commands
enum {
    CAN_CMD_DISARM = 1,
    CAN_CMD_ARM,
    CAN_CMD_START,
    CAN_CMD_STOP,
    CAN_CMD_SETPOINT10,
    CAN_CMD_SETPOINT12,
    CAN_CMD_SETPOINT16,
    CAN_CMD_RPM,
    CAN_CMD_CFG_READ,
    CAN_CMD_CFG_WRITE,
    CAN_CMD_CFG_DEFAULT,
    CAN_CMD_TELEM_RATE,
    CAN_CMD_TELEM_VALUE,
    CAN_CMD_BEEP,
    CAN_CMD_POS,
    CAN_CMD_USER_DEFINED,
    CAN_CMD_RESET,
    CAN_CMD_STREAM,
    CAN_CMD_ON,
    CAN_CMD_OFF
};
// sensor types
enum {
    CAN_SENSORS_PDB_BATV = 0,
    CAN_SENSORS_PDB_BATA,
    CAN_SENSORS_PDB_TEMP,
    CAN_SENSORS_GIMBAL_ACCX,
    CAN_SENSORS_GIMBAL_ACCY,
    CAN_SENSORS_GIMBAL_ACCZ,
    CAN_SENSORS_GIMBAL_GYOX,
    CAN_SENSORS_GIMBAL_GYOY,
    CAN_SENSORS_GIMBAL_GYOZ,
    CAN_SENSORS_GPS_LAT, // Added by Mathias 08.02.15
    CAN_SENSORS_GPS_LON, // Added by Mathias 08.02.15
    CAN_SENSORS_NUM
};
// Custom
#define CAN_EFF             (0x1 << 31) // Set can Extended bit(needed in can_interface my molar)
#define CAN_DOC_MASK        (0x3f<< (19-3))
//Can types
enum {
    CAN_TYPE_ESC = 1,
    CAN_TYPE_SERVO,
    CAN_TYPE_SENSOR,
    CAN_TYPE_SWITCH,
    CAN_TYPE_OSD,
    CAN_TYPE_UART,
    CAN_TYPE_HUB,
    CAN_TYPE_NUM
};
// data types
enum {
    CAN_DATA_GROUP = 1,
    CAN_DATA_TYPE,
    CAN_DATA_ID,
    CAN_DATA_INPUT_MODE,
    CAN_DATA_RUN_MODE,
    CAN_DATA_STATE,
    CAN_DATA_PARAM_ID,
    CAN_DATA_TELEM,
    CAN_DATA_VERSION,
    CAN_DATA_VALUE,
    CAN_DATA_PARAM_NAME1,
    CAN_DATA_PARAM_NAME2
};


class MessageCreator {
public:
	MessageCreator();
	canMSG Create_ReqAddr(int,int);
	canMSG Create_SendACK();
	Session mySession;
	canMSG Create_Stream(double,unsigned int);
};

#endif /* MESSAGECREATOR_H_ */
