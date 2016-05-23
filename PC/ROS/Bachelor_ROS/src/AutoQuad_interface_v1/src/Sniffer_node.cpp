/*
 I will write something important here at some point..
 MMN - Mathias Mikkel Neerup manee12@student.sdu.dk
 */

#include <sstream>
#include <iostream>

#include "AutoQuad.h"
#include "Session.h"

#define ST_IDLE            0
#define ST_RESET_RECV      1
#define ST_REQ_ADDR        2
#define ST_GOT_UNIQ_ADDR   3
#define ST_STREAM    4


#define LOOP_RATE 10



class RegisterNode_node : public AutoQuad {

private:
	int state;
	MessageCreator messageCreator;
	int txcount = LOOP_RATE; //Loop runs with 20 hz, only run with 1 hz(qgroundstation plots slowly)

	//Make a nice plot :>
	float phase = 0;
	float value_long = 0;
	float value_lat = 0;
public:
	void onTimer(const ros::TimerEvent& event){

	}
	void spin(){
		ros::spin();
	}

	void recv_ok_addr_msg(int id) {
	}

	RegisterNode_node(int argc, char** argv): AutoQuad(argc, argv){

	}
	void recv_reset_msg() {
		ROS_WARN("Reset msg received");
	}
	void recv_telem_rate_msg(int id){
		ROS_WARN("TELEM_RATE");
	}

	void recv_telem_value_msg(int id){
		ROS_WARN("TELEM_VALUE");
	}
};
int main(int argc, char **argv){
	AutoQuad* autoquad = new RegisterNode_node(argc, argv);

	autoquad->spin();
	return 0;
}




