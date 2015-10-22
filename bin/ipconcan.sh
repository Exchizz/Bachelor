#!/bin/bash
# s8 = 1mbit
sudo slcand -s8 -S 921600  /dev/ttyUSB0
sudo ip link set up slcan0
