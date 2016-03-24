/*
 * Session.h
 *
 *  Created on: Feb 5, 2016
 *      Author: exchizz
 */

#include "MessageCreator.h"
#ifndef SESSION_H_
#define SESSION_H_

class Session {
public:
	int target_id;
	int ttype;
	int llc;
	int uuid; // not implemented //
	int sequence_id;
	int source_id;
	Session();
	int createSession(int);
	int updateSession(int);
};

#endif /* SESSION_H */
