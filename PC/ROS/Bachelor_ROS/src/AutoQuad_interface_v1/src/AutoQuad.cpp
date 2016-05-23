#include "AutoQuad.h"

AutoQuad::AutoQuad(int argc, char** argv){
	ros::init(argc, argv, "wait_for_reset");
	ros::NodeHandle n;
	pub_recv = n.advertise<msgs::can>("/fmSignal/can_to_device", 5);
	sub_trans = n.subscribe("/fmSignal/can_from_device",1, &AutoQuad::can_callback, this);
	// Run at 20 hz
	timer = n.createTimer(ros::Duration(0.05), &AutoQuad::onTimer, this);
}

void AutoQuad::can_callback(const msgs::can::ConstPtr& can_msg){
	unsigned int id = can_msg->id;
//	ROS_DEBUG("Recv: Can message");


	switch(id & CAN_FID_MASK){
	case CAN_FID_GRANT_ADDR:
		recv_ok_addr_msg(id);
		break;

	case CAN_FID_RESET_BUS:
		recv_reset_msg();
		break;
	case CAN_FID_CMD:
	{

		switch((id & CAN_DOC_MASK) >> (19-3)){
		case CAN_CMD_TELEM_RATE:
			recv_telem_rate_msg(id);
			break;

		case CAN_CMD_TELEM_VALUE:
			recv_telem_value_msg(id);
			break;

		default:
//			ROS_WARN("Recv: Unknown function id command: %X", (id & CAN_DOC_MASK) >> (19 - 3));
		break;
		}

	}
	break;

	default:
//		ROS_WARN("Received unhandled message");
//		ROS_WARN("\t fid: %X", id & CAN_FID_MASK);
		break;
	}
}

