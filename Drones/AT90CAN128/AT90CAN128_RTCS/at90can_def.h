/*
 * at90can_def.h
 *
 *  Created on: Apr 14, 2016
 *      Author: exchizz
 */
#include <avr/io.h>

#ifndef AT90CAN_DEF_H_
#define AT90CAN_DEF_H_


#define INT0_CNT_TOP	249 /* corresponds on an interrupt0 each 1ms */

#define BV(bit) (1<<bit) /* return bit value for a bit */

/* ATmega port defines (output) */
#define PB_OUT( ddr, bit)		ddr |= BV(bit) /* set port bit as output */
#define PB_HIGH( port, bit)		port |= BV(bit) /* set port bit high */
#define PB_LOW( port, bit)		port &= ~BV(bit) /* set port bit low */
#define PB_FLIP( port, bit)		port ^= BV(bit) /* flip port bit */

/* LED defines */
#define INT_LED_INIT			PB_OUT (DDRE,DDE6) /* set LED bit as output */
#define INT_LED_ON				PB_LOW (PORTE,PE6) /* turn LED on */
#define INT_LED_OFF				PB_HIGH (PORTE,PE6) /* turn LED off */


#endif /* AT90CAN_DEF_H_ */
