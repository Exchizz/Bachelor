#!/bin/bash

action=$1


do_start () {

	echo -n -e "Starting DHCP server on wlan_ap : \n\t";
	sudo service isc-dhcp-server start
	echo -n -e "Starting hostapd on wlan_ap : \n\t";
	sudo service hostapd start

}


do_stop (){
	echo -n -e "Stopping DHCP server on wlan_ap : \n\t";
	sudo service isc-dhcp-server stop
	echo -n -e "Stopping hostapd on wlan_ap : \n\t";
	sudo service hostapd stop
}


case $action in
	"start")
		do_start
	;;

	"stop")
		do_stop
	;;
	"restart")
		do_stop
		do_start
	;;


	*)
		echo "Help useage: "
		echo -e "\tsetup.sh start - Starts access_point"
		echo -e "\tsetup_ap.sh stop  - Returns to normal useage";
	;;
esac
