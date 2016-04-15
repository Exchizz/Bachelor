/*
 * led.c
 *
 *  Created on: Apr 14, 2016
 *      Author: exchizz
 */
#include "at90can_def.h"

void led_init(){
	INT_LED_INIT;
	INT_LED_OFF;
}



