/*
 I will write something important here at some point..
 MMN - Mathias Mikkel Neerup manee12@student.sdu.dk
 */

#include <sstream>
#include <iostream>

#include "AutoQuad.h"
#include "Session.h"

#include "msgs/nmea.h"

#define ST_IDLE            0
#define ST_RESET_RECV      1
#define ST_REQ_ADDR        2
#define ST_GOT_UNIQ_ADDR   3
#define ST_STREAM    4


#define LOOP_RATE 5


#define LATITUDE_DOC  0x01
#define LONGITUDE_DOC 0x02
#define ALTITUDE_DOC  0x03


class RegisterNode_node : public AutoQuad {

private:
	int state;
	MessageCreator messageCreator;
	int txcount = LOOP_RATE; //Loop runs with 20 hz, only run with 1 hz(qgroundstation plots slowly)

	//Make a nice plot :>
	float phase = 0;
	float value_long = 0;
	float value_lat = 0;
	std::string topic_nmea_from_gps_sub;

	ros::Subscriber nmea_sub;
	msgs::nmea last_gps_msg;
public:
	void nmea_callback(const msgs::nmea::ConstPtr& nmea_msg){
		// Latitude
		double latitude = atof(nmea_msg->data[1].c_str());
		double longitude = atof(nmea_msg->data[3].c_str());

		std::cout << "Received from GPS, lat: " << latitude << " longitude: " << longitude << std::endl;

		canMSG canMessage = messageCreator.Create_Stream(latitude, LATITUDE_DOC);
		pub_recv.publish(canMessage);

		// Longitude
		canMessage = messageCreator.Create_Stream(longitude, LONGITUDE_DOC);
		pub_recv.publish(canMessage);

		int altitude = 30;
		canMessage = messageCreator.Create_Stream(altitude, LATITUDE_DOC);
		pub_recv.publish(canMessage);
	}
	void recv_reset_msg() {
		ROS_WARN("Reset msg received");
		state = ST_REQ_ADDR;
	}

	void recv_ok_addr_msg(int id) {
		messageCreator.mySession.updateSession(id);

		std::cout << "Tid: " << messageCreator.mySession.target_id << std::endl;
		std::cout << "Ttype: " << messageCreator.mySession.ttype << std::endl;
		std::cout << "Logic communication channel: " << messageCreator.mySession.llc << std::endl;
		std::cout << "Source id: " << messageCreator.mySession.source_id << std::endl;
		state = ST_GOT_UNIQ_ADDR;
	}

	//void recv_

	RegisterNode_node(int argc, char** argv): AutoQuad(argc, argv){
		state = ST_IDLE;
		ros::NodeHandle n("~ ");
		n.param<std::string> ("nmea_from_device_sub", topic_nmea_from_gps_sub, "/fmData/nmea_from_gps");
		nmea_sub = n.subscribe(topic_nmea_from_gps_sub, 1000, &RegisterNode_node::nmea_callback, this);
	}

	void onTimer(const ros::TimerEvent& event){
		switch(state){
		case ST_IDLE:
			break;
		case ST_REQ_ADDR:
		{
			ROS_WARN("Tx: Request addr");
			canMSG canMessage = messageCreator.Create_ReqAddr(CAN_TYPE_SENSOR, CAN_SENSORS_GPS_LAT);
			pub_recv.publish(canMessage);
			state = ST_IDLE;
		}
		break;
		case ST_GOT_UNIQ_ADDR:
			state = ST_STREAM;
			break;

		case ST_STREAM:
			if( (txcount++) != LOOP_RATE ){
				break;
			}


			break;
		}
	}
	void spin(){
		ros::spin();
	}

	void recv_telem_rate_msg(int id){
		// Update the current session
		messageCreator.mySession.updateSession(id);

		ROS_WARN("TELEM_RATE");
		canMSG canMessage = messageCreator.Create_SendACK();
		pub_recv.publish(canMessage);
		state = ST_STREAM;
	}

	void recv_telem_value_msg(int id){
		// Update the current session
		messageCreator.mySession.updateSession(id);

		ROS_WARN("TELEM_VALUE");
		canMSG canMessage = messageCreator.Create_SendACK();
		pub_recv.publish(canMessage);
	}
};


int main(int argc, char **argv){
	AutoQuad* autoquad = new RegisterNode_node(argc, argv);

	autoquad->spin();
	return 0;
}
