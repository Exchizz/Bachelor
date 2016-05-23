/*
 * SessionHandler.cpp
 *
 *  Created on: Feb 5, 2016
 *      Author: exchizz
 */

#include "Session.h"

Session::Session() {
	// TODO Auto-generated constructor stub

}

int Session::createSession(int id){
	return 0;
}


int Session::updateSession(int id){
	sequence_id = (id & CAN_SEQ_MASK);
	source_id = ((id & CAN_TID_MASK) >> (9-3)); //We are target_id with respect to the drone, but source when we are sending.. I assume
	std::cout << "Received source_id: " << source_id << std::endl;
//	target_id = ((id & CAN_TID_MASK) >> (9-3));
	//ttype = (id & CAN_TT_MASK);
	//llc = (id & CAN_LCC_MASK);

	return sequence_id;
}
