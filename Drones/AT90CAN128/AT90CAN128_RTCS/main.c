#include "led.h"
#include "systick.h"
#include "rtcs.h"
#include "tmodel.h"
#include "uart.h"
#include "task.h"
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
	open_queue( Q_UART_TX );
	open_queue( Q_UART_RX );

	led_init();
	uart1_init(57600);
	init_rtcs();
	//start_task( TASK_DISPLAY_RTC, display_rtc_task );
	start_task( TASK_UART_TX, uart_tx_task );
	start_task( TASK_UART_RX, uart_rx_task );
	start_task( TASK_COUNTER, counter_task );
	schedule();

	return(0);

}

