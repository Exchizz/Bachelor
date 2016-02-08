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
	//source_id = ((id & CAN_SID_MASK) >> (14-3));
	source_id = ((id & CAN_TID_MASK) >> (9-3)); //We are target_id with respect to the drone, but source when we are sending.. I assume
	//ttype = (id & CAN_TT_MASK >> (29-3));
	//llc = (id & CAN_LCC_MASK >> (30-3));

	return sequence_id;
}
