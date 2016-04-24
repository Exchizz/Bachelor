/*****************************************************************************
* University of Southern Denmark
* Embedded Programming (EMP)
*
* MODULENAME.: uart.h
*
* PROJECT....: EMP
*
* DESCRIPTION: Test.
*
* Change Log:
******************************************************************************
* Date    Id    Change
* YYMMDD
* --------------------
* 150228  MoH   Module created.
*
*****************************************************************************/

#ifndef _UART_H
  #define _UART_H

/***************************** Include files *******************************/
#include <avr/io.h>
#include <avr/interrupt.h>
#include "tmodel.h"
/*****************************    Defines    *******************************/
/***************************************************************************/
/* parameters for serial communication */

#define FOSC 		8000000	/* oscillator frequency [Hz] */
#define BAUD 		9600		/* baud rate */
//#define USART_0					/* serial port */
/* #define DOUBLE_SPEED_MODE */

/***************************************************************************/
/* defines */
#define USART_0 1
#define USART_1 2

/*****************************   Constants   *******************************/
/*****************************   Functions   *******************************/
BOOLEAN uart_put_q( INT8U );
BOOLEAN uart_get_q( INT8U* );

void uart_tx_task(INT8U my_id, INT8U my_state, INT8U event, INT8U data);
void uart_rx_task(INT8U my_id, INT8U my_state, INT8U event, INT8U data);


extern void uart_init(int uart);
/*****************************************************************************
*   Input    : -
*   Output   : -
*   Function : Initialize uart 0
******************************************************************************/


/****************************** End Of Module *******************************/
#endif

