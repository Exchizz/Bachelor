/*
 * scheduler.h
 *
 *  Created on: Apr 14, 2016
 *      Author: exchizz
 */
#include <avr/interrupt.h>
#include "at90can_def.h"
#include "emp_type.h"

#ifndef SYSTICK_H_
	#define SYSTICK_H_

	volatile INT16S ticks;
	void init_systick();
#endif /* SYSTICK_H_ */
