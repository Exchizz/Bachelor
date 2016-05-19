#!/bin/sh
#
# Script for setting up can0 and can1.
# If real devices are available they are used - if not fake ones are created.
#

setup_canX() {
	# Try to down the interface - if it fails the interface does not exist.
	sudo ifconfig can$1 down > /dev/null 2>&1
	if [ $? -ne 0 ]; then
#		echo "Unable to bring can0 down.."
#		sudo ip link add name can$1 type vcan
		exit 1
	fi

	# Setup flags - fake devices do not support these
	sudo ip link set can$1 type can restart-ms 100 > /dev/null 2>&1
#	sudo ip link set can$1 up type can bitrate 250000 > /dev/null 2>&1 # changed from 1 mbit
	sudo ip link set can$1 up type can bitrate 1000000 > /dev/null 2>&1 
	if [ $? -eq 0 ]; then
		echo "can$1 setup as a real device."
	else
		echo "can$1 setup as a fake device."
	fi
	sudo ifconfig can$1 up
	if [ $? -ne 0 ]; then
		echo "Failed bringing up can$1."
	fi

}


# Load vcan driver
sudo modprobe vcan
sudo ip link add type vcan

setup_canX 0
