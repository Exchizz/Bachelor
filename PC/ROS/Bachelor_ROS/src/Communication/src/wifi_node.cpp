//#include <stdio.h>
#include <stdint.h>
//#include <stdlib.h>
//#include <unistd.h>
#include <string.h>
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

/*
		uint8_t hDOP = 1.5;
		uint8_t vDOP = 1.5*hDOP*10;
		uint8_t tDOP = 1.5*hDOP*10;
		uint8_t nDOP = 0.7*hDOP*10;
		uint8_t eDOP = 0.7*hDOP*10;
*/

//		uint8_t hDOP = 11;
		uint8_t vDOP = 35;
		uint8_t tDOP = 27;
		uint8_t nDOP = 27;
		uint8_t eDOP = 27;

	public:
		WIFI(std::string ip, int port){
			addr.sin_family = AF_INET;
			addr.sin_port = htons(port);
			ret = inet_aton(ip.c_str(), &addr.sin_addr);
			if (ret == 0) { perror("inet_aton"); }

			s = socket(PF_INET, SOCK_DGRAM, 0);
			if (s == -1) { perror("socket"); exit(1); }

			ROS_WARN("Communication to %s:%d started", ip.c_str(), port);
		}

		void GPSCallback(const Communication::GPS::ConstPtr& msg){
			ROS_WARN("I heard a %f %f", msg->lat, msg->lon);

			double lat = msg->lat;
			double lon = msg->lon;
			double height = msg->height;
			double dop = msg->DOP;

			unsigned char data[34];
			int i = 0;
			char temp[8];

			memcpy(temp, &lat, 8);
			for(; i < 8; i++){
				data[i] = temp[(i)];
			}

			memcpy(temp, &lon, 8);
			for(; i < 16; i++){
				data[i] = temp[(i-8)];
			}

			memcpy(temp, &height, 8);
			for(; i < 24; i++){
				data[i] = temp[(i-16)];
			}

//			memcpy(temp, &dop, 8);
//			for(; i < 32; i++){
//				data[i] = temp[(i-24)];
//			}

			data[i++] = vDOP;
			data[i++] = tDOP;
			data[i++] = nDOP;
			data[i++] = eDOP;

			data[i++] = 0;
			data[i++] = 0;
			data[i++] = 0;
			data[i++] = 0;

			crc = crc_init();
			crc = crc_update(crc, data, 32);
			crc = crc_finalize(crc);

			data[i++] = (crc>>8) & 0x00ff;
			data[i++] = crc & 0x00ff;

			ret = sendto(s, data, 34, 0, (struct sockaddr *)&addr, sizeof(addr));
			if (ret == -1) {
				perror("sendto");
			}
		}

		void spin(){
			ros::spin();
		}
};

int main(int argc, char **argv){


	ros::init(argc, argv, "listener");
	ros::NodeHandle n("~");
	std::string param_ip, param_topic;
	int param_port;

	n.param<std::string>("ip", param_ip, "127.0.0.1");
	n.param<int>("port", param_port, 8888);
	n.param<std::string>("topic_sub", param_topic, "/data_in");

	WIFI wifi(param_ip, param_port);
	ros::Subscriber sub = n.subscribe(param_topic.c_str(), 10, &WIFI::GPSCallback, &wifi);
	wifi.spin();
	return 0;
}

