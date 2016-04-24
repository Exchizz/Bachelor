/*
 * ESP8266.c
 *
 *  Created on: Apr 22, 2016
 *      Author: exchizz
 */
#include "ESP8266.h"

void esp_init(int mode){
	esp_powerup();

	switch(mode){
	case ESP_NORMAL_MODE:
		esp_at_mode();
		break;
	case ESP_FLASH_MODE:
		esp_flash_mode();
		break;
	}
}

void esp_powerup(){
	//INIT_RX1_IN;
	//INIT_TX1_IN;
	INIT_CH_PD;
	INIT_RESET;
	INIT_GPIO0;

	INT_CH_PD_HIGH;
	INT_RESET_LOW;

	//INT_RX1_TRI_STATE;
	//INT_TX1_TRI_STATE;


}


void esp_at_mode(){
	INT_GPIO0_HIGH;
	INT_LED_ON_RED;
}

void esp_flash_mode(){
	INT_GPIO0_LOW;
	INT_LED_ON_BLUE;
}
