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

#define FOSC 		16000000	/* oscillator frequency [Hz] */
#define BAUD 		57600		/* baud rate */
#define USART_1					/* serial port */
/* #define DOUBLE_SPEED_MODE */

/***************************************************************************/
/* defines */

#ifdef USART
	#define UCSRA_REG 	UCSR0A
	#define UCSRB_REG 	UCSR0B
	#define UCSRC_REG 	UCSR0C
	#define UBRRL_REG 	UBRR0L
	#define UBRRH_REG 	UBRR0H
	#define UDR_REG		UDR0
	#define RXEN_BIT	RXEN0
	#define TXEN_BIT	TXEN0
	#define RXCIE_BIT	RXCIE0
	#define TXCIE_BIT	TXCIE0
	#define RXC_BIT		RXC0
	#define TXC_BIT		TXC0
	#define U2X_BIT		U2X0
	#define UCSZ0_BIT	UCSZ00
	#define UCSZ1_BIT	UCSZ01
	#define UDRE_BIT	UDRE0
#endif

#ifdef USART_0
	#define UCSRA_REG 	UCSR0A
	#define UCSRB_REG 	UCSR0B
	#define UCSRC_REG 	UCSR0C
	#define UBRRL_REG 	UBRR0L
	#define UBRRH_REG 	UBRR0H
	#define UDR_REG		UDR0
	#define RXEN_BIT	RXEN0
	#define TXEN_BIT	TXEN0
	#define RXCIE_BIT	RXCIE0
	#define TXCIE_BIT	TXCIE0
	#define RXC_BIT		RXC0
	#define TXC_BIT		TXC0
	#define U2X_BIT		U2X0
	#define UCSZ0_BIT	UCSZ00
	#define UCSZ1_BIT	UCSZ01
	#define UDRE_BIT	UDRE0
#endif

#ifdef USART_1
	#define UCSRA_REG 	UCSR1A
	#define UCSRB_REG 	UCSR1B
	#define UCSRC_REG 	UCSR1C
	#define UBRRL_REG 	UBRR1L
	#define UBRRH_REG 	UBRR1H
	#define UDR_REG		UDR1
	#define RXEN_BIT	RXEN1
	#define TXEN_BIT	TXEN1
	#define RXCIE_BIT	RXCIE1
	#define TXCIE_BIT	TXCIE1
	#define RXC_BIT		RXC1
	#define TXC_BIT		TXC1
	#define U2X_BIT		U2X1
	#define UCSZ0_BIT	UCSZ10
	#define UCSZ1_BIT	UCSZ11
	#define UDRE_BIT	UDRE1
#endif

#ifdef DOUBLE_SPEED_MODE
	#define UBRR (FOSC/BAUD/8 - 1)
#else
	#define UBRR (FOSC/BAUD/16 - 1)
#endif

/*****************************   Constants   *******************************/

/*****************************   Functions   *******************************/
BOOLEAN uart_put_q( INT8U );
BOOLEAN uart_get_q( INT8U* );

void uart_tx_task(INT8U my_id, INT8U my_state, INT8U event, INT8U data);
void uart_rx_task(INT8U my_id, INT8U my_state, INT8U event, INT8U data);


extern void uart1_init( INT32U baud_rate);
/*****************************************************************************
*   Input    : -
*   Output   : -
*   Function : Initialize uart 0
******************************************************************************/


/****************************** End Of Module *******************************/
#endif

