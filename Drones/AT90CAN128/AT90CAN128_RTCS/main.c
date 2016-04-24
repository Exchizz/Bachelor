#include "led.h"
#include "systick.h"
#include "rtcs.h"
#include "tmodel.h"
#include "uart.h"
#include "task.h"
#include "ESP8266.h"
int main(void){

	/*
	open_queue( Q_UART_TX );
	 */
	/*
	start_task( TASK_UART_TX, uart_tx_task );
	start_task( TASK_UART_RX, uart_rx_task );
	start_task( TASK_KEY, key_task );
	start_task( TASK_UI, ui_task );
	start_task( TASK_UI_KEY, ui_key_task );
	start_task( TASK_LCD, lcd_task );
	start_task( TASK_RTC, rtc_task );

	 */

	/*
	 * Set prescaler to 2. External clock = 16 mhz, only run 8 mhz
	 */

	CLKPR = (1 << CLKPCE); // Enable change of CLKPS bits
	CLKPR = (1 << CLKPS0) ; // Set prescaler to 2, and system clock to 8 MHz as said in datasheet to at90can128

	open_queue( Q_UART_TX );
	open_queue( Q_UART_RX );
	led_init();

	uart_init(USART_0);
	//uart_init(USART_1);

	init_rtcs();
	esp_init(ESP_NORMAL_MODE);

	start_task( TASK_UART_TX, uart_tx_task );
	start_task( TASK_UART_RX, uart_rx_task );
	start_task( TASK_COUNTER, counter_task );
	schedule();

	return(0);

}

