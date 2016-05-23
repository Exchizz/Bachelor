/*
 * MessageCreator.cpp
 *
 *  Created on: Feb 4, 2016
 *      Author: exchizz
 */

#include "MessageCreator.h"

MessageCreator::MessageCreator() {
	// TODO Auto-generated constructor stub

}

canMSG MessageCreator::Create_ReqAddr(int type, int canId){
	canMSG msg_out;

	msg_out.id = CAN_FID_REQ_ADDR | CAN_EFF;

	// EF, CD, AB, 89 is uuid in AutoQuad
	std::vector<int> v {'\x01','\xEF','\xCD','\xAC',type, canId,'\x23','\x01'}; // '\x23','\x01'

	for(int i = 0; i < v.size(); ++i){
		msg_out.data[i] = v[i];
	}
	msg_out.length = v.size();

	return msg_out;
}

canMSG MessageCreator::Create_Stream(double value, unsigned int doc) {

	canMSG msg_out;
	msg_out.id = CAN_FID_TELEM | CAN_EFF | (mySession.source_id << (14-3)) | (doc << (19-3));

	const unsigned char * value_double = reinterpret_cast<const unsigned char*>(&value);

	for(int i = 0; i < sizeof(double); ++i){
		msg_out.data[i] = value_double[i];
	}
	msg_out.length = sizeof(double);

	return msg_out;
}

canMSG MessageCreator::Create_SendACK(){
	canMSG msg_out;

	msg_out.id = CAN_FID_ACK | CAN_EFF | mySession.sequence_id;
	msg_out.length = 0;

	return msg_out;
}

