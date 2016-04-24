/*
 * ESP8266.h
 *
 *  Created on: Apr 22, 2016
 *      Author: exchizz
 */

#ifndef ESP8266_H_
#define ESP8266_H_

#include "at90can_def.h"
#define ESP_NORMAL_MODE       1
#define ESP_FLASH_MODE    2

#define INIT_CH_PD		PB_OUT (DDRA,DDA4) /* set LED bit as output */
#define INT_CH_PD_HIGH	PB_HIGH (PORTA,PA4) /* turn LED on */
#define INT_CH_PD_LOW	PB_LOW (PORTA,PA4) /* turn LED on */

#define INIT_GPIO0		PB_OUT (DDRE,DDE4) /* set LED bit as output */
#define INT_GPIO0_HIGH	PB_HIGH (PORTE,PE4) /* turn LED on */
#define INT_GPIO0_LOW	PB_LOW (PORTE,PE4) /* turn LED on */

#define INIT_RESET		PB_OUT (DDRA,DDA3) /* set LED bit as output */
#define INT_RESET_HIGH	PB_HIGH (PORTA,PA3) /* turn LED on */
#define INT_RESET_LOW	PB_LOW (PORTA,PA3) /* turn LED on */


#define INIT_RX1_IN	PB_IN (DDRD,DDD2) /* set LED bit as output */
#define INIT_TX1_IN	PB_IN (DDRD,DDD3) /* set LED bit as output */

#define INT_RX1_TRI_STATE	PB_HIGH (PORTD,PD2) /* turn LED on */
#define INT_TX1_TRI_STATE	PB_HIGH (PORTD,PD3) /* turn LED on */




void esp_init(int mode);
void esp_powerup();
void esp_at_mode();
void esp_flash_mode();

#endif /* ESP8266_H_ */
