/*
 * scheduler.c
 *
 *  Created on: Apr 14, 2016
 *      Author: exchizz
 */
#include "systick.h"

void init_systick(){
	TIMSK0 = BV(OCIE0A);
	TCCR0A = BV(CS00) | BV(CS01) | BV(WGM01); /* clk/64, TOS is defined as OCR0A */
	OCR0A = INT0_CNT_TOP;
}


ISR (TIMER0_COMP_vect){
	ticks++;
}
