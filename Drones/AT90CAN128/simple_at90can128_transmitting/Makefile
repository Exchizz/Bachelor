#############################################################################
# Frobit FroboMind Controller firmware
# Copyright (c) 2012-2014, Kjeld Jensen <kjeld@frobomind.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#############################################################################
# File: Makefile
# Project: Frobit FroboMind Controller firmware
# Platform: RoboCard v1.11 http://www.robocard.org
# Microcontroller: ATmega328p
# Author: Kjeld Jensen <kjeld@frobomind.org>
# Created:  2012-08-14
# Modified: 2013-02-12 Kjeld Jensen, added wheel.c, pid_ctrl.c and migrated to the BSD license
# Modified: 2014-04-17 Kjeld Jensen, updated serial driver to avr_serial.c
#                                    pid_ctrl.c is now pid_ctrl_int.c
# Modified: 2014-08-16 Kjeld Jensen, ported to the FroboMind Controller
#############################################################################

PROJECT=main
SOURCES=can_test1.c
MMCU=at90can128
CC=avr-gcc
AVRDUDE=avrdude -p c128 -c usbasp

CFLAGS= -mmcu=$(MMCU) -Wall -Os -pedantic -Wall

default:
	@echo ""
	@echo "make clean......delete object & hex files"
	@echo "make hex........build the $(PROJECT).hex file"
	@echo "make flash......copy $(PROJECT).hex to RoboCard flash"
	@echo "make fuse.......set external crystal fuse"
	@echo ""

hex: $(PROJECT).elf
	avr-objcopy -R .eeprom -O ihex $(PROJECT).elf  $(PROJECT).hex

$(PROJECT).elf: $(SOURCES)
	$(CC) $(CFLAGS) -I./ -o $(PROJECT).elf $(SOURCES)

flash: $(PROJECT).hex
	 $(AVRDUDE) -U flash:w:$(PROJECT).hex

#fuse:
#	$(AVRDUDE) $(M328FUSEOPT)

clean:
	rm -f $(PROJECT).elf $(PROJECT).hex

#############################################################################

