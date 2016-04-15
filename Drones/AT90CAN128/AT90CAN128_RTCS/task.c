/*
 * task.c
 *
 *  Created on: Apr 15, 2016
 *      Author: exchizz
 */


#include "task.h"

extern void counter_task(INT8U my_id, INT8U my_state, INT8U event, INT8U data){
	static INT8U counter = 0;
	char string[] = "number: \n\r";
	string[7] = counter++ + '0';
	for(int i = 0; i < 10; i++){
		put_queue( Q_UART_TX, string[i], WAIT_FOREVER );
	}
	wait(500);
}
