/*
 * at90can_def.h
 *
 *  Created on: Apr 14, 2016
 *      Author: exchizz
 */
#include <avr/io.h>

#ifndef AT90CAN_DEF_H_
#define AT90CAN_DEF_H_


#define WIFI_BOARD 1

#define INT0_CNT_TOP	249 /* corresponds on an interrupt0 each 1ms */

#define BV(bit) (1<<bit) /* return bit value for a bit */

#define PB_OUT( ddr, bit)		ddr |= BV(bit) /* set port bit as output */
#define PB_IN( ddr, bit) ddr &= ~BV(bit) /* set port bit as input */
#define PB_HIGH( port, bit)		port |= BV(bit) /* set port bit high */
#define PB_LOW( port, bit)		port &= ~BV(bit) /* set port bit low */
#define PB_FLIP( port, bit)		port ^= BV(bit) /* flip port bit */

#ifdef FMCTRL
/* ATmega port defines (output) */
	/* LED defines */
	#define INT_LED_INIT			PB_OUT (DDRE,DDE6) /* set LED bit as output */
	#define INT_LED_ON				PB_LOW (PORTE,PE6) /* turn LED on */
	#define INT_LED_OFF				PB_HIGH (PORTE,PE6) /* turn LED off */

#elif WIFI_BOARD

	/* LED defines */
	#define INT_LED_INIT_RED		PB_OUT (DDRB,DDE6) /* set LED bit as output */
	#define INT_LED_ON_RED			PB_LOW (PORTB,PE6) /* turn LED on */
	#define INT_LED_OFF_RED			PB_HIGH (PORTB,PE6) /* turn LED off */

	#define INT_LED_INIT_GREEN		PB_OUT (DDRB,DDE5) /* set LED bit as output */
	#define INT_LED_ON_GREEN		PB_LOW (PORTB,PE5) /* turn LED on */
	#define INT_LED_OFF_GREEN		PB_HIGH (PORTB,PE5) /* turn LED off */

	#define INT_LED_INIT_BLUE		PB_OUT (DDRB,DDE4) /* set LED bit as output */
	#define INT_LED_ON_BLUE			PB_LOW (PORTB,PE4) /* turn LED on */
	#define INT_LED_OFF_BLUE		PB_HIGH (PORTB,PE4) /* turn LED off */

#endif
#endif /* AT90CAN_DEF_H_ */
