/*
 * led.c
 *
 *  Created on: Apr 14, 2016
 *      Author: exchizz
 */
#include "at90can_def.h"

void led_init(){
#ifdef FMCTRL
	INT_LED_INIT;
	INT_LED_OFF;

#elif WIFI_BOARD
	INT_LED_INIT_GREEN;
	INT_LED_OFF_GREEN;

	INT_LED_INIT_RED;
	INT_LED_OFF_RED;

	INT_LED_INIT_BLUE;
	INT_LED_OFF_BLUE;
#endif
}



