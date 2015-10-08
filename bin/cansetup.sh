#!/bin/bash
sudo slcand -o -s5 -t hw  /dev/ttyUSB1
sudo ip link set up slcan1
