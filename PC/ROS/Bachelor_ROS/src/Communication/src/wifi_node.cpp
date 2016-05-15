//#include <stdio.h>
#include <stdint.h>
//#include <stdlib.h>
//#include <unistd.h>
//#include <string.h>
//#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/in_systm.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>

#include "ros/ros.h"
#include "Communication/GPS.h"
#include "crc/crc.h"

class WIFI {
	private:
		int s;
		int ret;
		struct sockaddr_in addr;
		crc_t crc;
	public:
		WIFI(int argc, char **argv){

			int port = 8888;

			addr.sin_family = AF_INET;
			addr.sin_port = htons(port);
			ret = inet_aton("192.168.0.15", &addr.sin_addr);
			if (ret == 0) { perror("inet_aton"); }

			s = socket(PF_INET, SOCK_DGRAM, 0);
			if (s == -1) { perror("socket"); exit(1); }


		}

		void GPSCallback(const Communication::GPS::ConstPtr& msg){
			ROS_WARN("I heard a %f %f", msg->lat, msg->lon);
/*
			double lat = msg->lat;
			double lon = msg->lon;
			double height = msg->height;
			double dop = msg->DOP;

			unsigned char data_all[34];
			int i = 0;

			unsigned char data[8];


			memcpy(data, &lat, 8);
			for(; i < 8; i++){
				data_all[i] = data[(i)];
			}


			memcpy(data, &lon, 8);

			for(; i < 16; i++){
				data_all[i] = data[(i-8)];
			}

			memcpy(data, &height, 8);
			for(; i < 24; i++){
				data_all[i] = data[(i-16)];
			}

			memcpy(data, &dop, 8);
			for(; i < 32; i++){
				data_all[i] = data[(i-24)];
			}

*/
//			unsigned char data[] = "1abdefghijklmnopqrstuvxyz123456700";
			crc = crc_init();
			crc = crc_update(crc, data,32);
			crc = crc_finalize(crc);


			data[32] = (crc>>8) & 0x00ff;
			data[33] = crc & 0x00ff;

			ret = sendto(s, data, 34, 0, (struct sockaddr *)&addr, sizeof(addr));
			if (ret == -1) {
				perror("sendto");
			}

		}

		void spin(){
			ros::spin();
		}



};

/**
 * This tutorial demonstrates simple receipt of messages over the ROS system.
 */

int main(int argc, char **argv){
	WIFI wifi(argc, argv);


	ros::init(argc, argv, "listener");
	ros::NodeHandle n;
	ros::Subscriber sub = n.subscribe("data_in", 10, &WIFI::GPSCallback, &wifi);
	ROS_WARN("Node started");
	wifi.spin();
	return 0;
}

