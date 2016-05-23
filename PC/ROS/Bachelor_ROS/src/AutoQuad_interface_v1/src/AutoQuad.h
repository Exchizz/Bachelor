#include "ros/ros.h"
#include "msgs/can.h"
#include "MessageCreator.h"

#ifndef AUTOQUAD_H_
#define AUTOQUAD_H_

// Abstract class because of virtual
class AutoQuad {
private:
	//Methods
	virtual void recv_reset_msg() = 0; // Pure virtual
	virtual void recv_ok_addr_msg(int id){};

protected:
	// Variables
	ros::Publisher  pub_recv; // receve with respect to PC
	ros::Subscriber sub_trans; // transmit with respect to PC

	// Timer
	ros::Timer timer;
public:

	//Methods
	virtual void spin() = 0; // Pure virtual
	virtual void onTimer(const ros::TimerEvent& event){}
	void can_callback(const msgs::can::ConstPtr& can_msg);
	virtual void recv_telem_value_msg(int){};
	virtual void recv_telem_rate_msg(int){};


	AutoQuad(){}
	AutoQuad(int argc, char** argv);

	// Destructor
	virtual ~AutoQuad(){}
};
#endif /* AUTOQUAD_H_ */
