/*****************************************************************************
 * University of Southern Denmark
 * Embedded Programming (EMP)
 *
 * MODULENAME.: emp.c
 *
 * PROJECT....: EMP
 *
 * DESCRIPTION: See module specification file (.h-file).
 *
 * Change Log:
 *****************************************************************************
 * Date    Id    Change
 * YYMMDD
 * --------------------
 * 150228  MoH   Module created.
 *
 *****************************************************************************/

/***************************** Include files *******************************/
#include <stdint.h>
#include "emp_type.h"
#include "uart.h"
#include "led.h"
/*****************************    Defines    *******************************/

/*****************************   Constants   *******************************/

/*****************************   Variables   *******************************/


/*****************************   Functions   *******************************/

BOOLEAN uart_put_q( INT8U ch )
{
	return( put_queue( Q_UART_TX, ch, WAIT_FOREVER ));
}

BOOLEAN uart_get_q( INT8U *pch )
{
	return( get_queue( Q_UART_RX, pch, WAIT_FOREVER ));
}

BOOLEAN uart1_rx_rdy()
/*****************************************************************************
 *   Function : See module specification (.h-file).
 *****************************************************************************/
{
	//return( uart1_FR_R & UART_FR_RXFF );
	return (UCSR1A & (1 << RXC1));
}

INT8U uart1_getc()
/*****************************************************************************
 *   Function : See module specification (.h-file).
 *****************************************************************************/
{
	return ( UDR_REG );
}

BOOLEAN uart1_tx_rdy()
/*****************************************************************************
 *   Function : See module specification (.h-file).
 *****************************************************************************/
{
	//return( uart1_FR_R & UART_FR_TXFE );
	return (UCSRA_REG & (1 << TXC_BIT));
}

void uart1_putc( INT8U ch )
/*****************************************************************************
 *   Function : See module specification (.h-file).
 *****************************************************************************/
{
	UDR_REG = ch;
}

extern void uart_rx_task(INT8U my_id, INT8U my_state, INT8U event, INT8U data)
/*****************************************************************************
 *   Input    :
 *   Output   :
 *   Function :
 ******************************************************************************/
{

	if( uart1_rx_rdy() ){
		put_queue( Q_UART_RX, uart1_getc(), WAIT_FOREVER );

	} else
		wait( 1 );
}

extern void uart_tx_task(INT8U my_id, INT8U my_state, INT8U event, INT8U data)
/*****************************************************************************
 *   Input    :
 *   Output   :
 *   Function :
 ******************************************************************************/
{
	INT8U ch;

	if( get_queue( Q_UART_TX, &ch, WAIT_FOREVER ))
		uart1_putc(ch);
}


extern void uart1_init( INT32U baud_rate)
/*****************************************************************************
 *   Function : See module specification (.h-file).
 *****************************************************************************/
{
	/* enable tx and rx */
	UCSRB_REG = (1<<TXEN_BIT)|(1<<RXEN_BIT);

	/* set baud rate */
	UBRRH_REG = (unsigned char) ((UBRR)>>8);
	UBRRL_REG = (unsigned char) (UBRR); /* remember the ()! */

	/* asynchronous 8N1 */
	UCSRC_REG = (1<<UCSZ0_BIT)|(1<<UCSZ1_BIT);

	/* enable double speed mode if #DOUBLE_SPEED_MODE is set */
#ifdef DOUBLE_SPEED_MODE
	UCSRA_REG |= U2X_BIT;
#endif

	/* init rx  */
	//UCSRB_REG |= (1 << RXCIE_BIT);
}
/****************************** End Of Module *******************************/












