#define F_CPU 16000000UL


#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

#define true 1
#define false 0

char data, canpage_bkp;

struct Frame {
	int id;
};


void init_led(){
    DDRE |= (1<<6);                    /* Set all the pins of PortE, pin 6 as output () */
}


void LED_DEBUG(int state){
	if(state == true){
		PORTE &= ~(1<<6);
	} else {
		PORTE |= (1<<6);
	}
}

void can_tx_msg(struct Frame * frame){

	CANPAGE = (1<<MOBNB0);  /* select MOb 1 */
	/* CANIDT is identifier tag */
	CANIDT2 = (char)(frame->id <<5); /* 3 left bits, shift 5 , id = 4 */
	CANIDT1 = (char)(frame->id >> 3); /* 3 bits in byte above, move 3 left, still id=4 */

	/* cant send long frame */
	CANIDT3 = 0x00 ;
	CANIDT4 = 0x00 ;

	CANMSG = 0x01;
	CANMSG = 0x02;
	CANMSG = 0x03;
	CANMSG = 0x04;
	CANMSG = 0x05;
	CANMSG = 0x06;
	CANMSG = 0x07;
	CANMSG = 0x08;

	CANSTMOB = 0x00; /* clear all status flags */

	/* set data length & enable transmission in MOb ctrl & DLC register */
	CANCDMOB = 8|(0<<CONMOB1)|(1<<CONMOB0);
}

	int i = 0;
int main(void)
{

	int num_mob, num_data;
	struct Frame *frame = {0}; /* Initialize struct */
	init_led();

	CANGCON = (1<<SWRES); /* Reset CAN controller */

	while((CANGSTA & (1<<ENFG)) != 0); /*wait for CAN controller to be enabled */

	/* 250 kbits pr. sek */
	CANBT1  = 0x06;
	CANBT2  = 0x0C;
	CANBT3  = 0x37;

	/* MOb 0 is used for Rx */
	CANPAGE = (0<<MOBNB0);
	CANCDMOB = 8|(1<<CONMOB1); /* enable rx, max data length */
   	CANSTMOB = 0; /* Can Mob status */
   	CANIDT1  = 0; /* Disable auto reply mode */
   	CANIDT2  = 0;
   	CANIDT3  = 0;
   	CANIDT4  = 0;
   	CANIDM1  = 0; /* accept all ID's */
   	CANIDM2  = 0;
   	CANIDM3  = 0;
   	CANIDM4  = 0;

	/* MOb 1 is used for Tx */
	CANPAGE  = (1<<MOBNB0); /* select MOb 1 */
   	CANCDMOB = 0;
   	CANSTMOB = 0;
   	CANIDT1  = 0;
   	CANIDT2  = 0;
   	CANIDT3  = 0;
   	CANIDT4  = 0;
   	CANIDM1  = 0;
   	CANIDM2  = 0;
   	CANIDM3  = 0;
   	CANIDM4  = 0;


	/* reset all other MOb's */
	for (num_mob=2; num_mob<15; num_mob++){
   		CANPAGE  = (num_mob<<MOBNB0);
   		CANCDMOB = 0;
   		CANSTMOB = 0;
   		CANIDT1  = 0;
   		CANIDT2  = 0;
   		CANIDT3  = 0;
   		CANIDT4  = 0;
   		CANIDM1  = 0;
   		CANIDM2  = 0;
   		CANIDM3  = 0;
   		CANIDM4  = 0;

 		for (num_data = 0; num_data < 8; num_data++){
   			CANMSG = 0;
		}
 	}

	/* configure the MOb 0 interrupt */
	CANIE1 = 0;
	CANIE2 = (1<<IEMOB0); /*<- interrupt on mob0 (rx)*/

	/* enable CAN (ENA/STB bit) */
        CANGCON |= (1 << ENASTB);

	/* wait until CAN is enabled */
 	while(!(CANGSTA & (1<<ENFG)))

	/* CAN general & Rx interrupt enable */
 	CANGIE = (1<<ENRX)|(1<<ENIT);

	/* configure the MOb 0 interrupt */

	sei();
	LED_DEBUG(false);
	while (true){
		frame->id = i++;
		can_tx_msg(frame);
		LED_DEBUG(true);
		_delay_ms(250);
		LED_DEBUG(false);
		_delay_ms(250);
	}
}

ISR(CANIT_vect){

	/* backup the current MOb page */
	canpage_bkp = (CANPAGE & 0xF0);

	/* select MOb 0 (RX) */
	CANPAGE = (0<<MOBNB0);

	/* if received interrupt is RXOK */
	if(CANSTMOB & (1 << RXOK)){
/*		data_buff[head].id = (((int)(CANIDT2))>>5) + (((int)(CANIDT1))<<3); // V2.0 part A */
		data = CANMSG;
		data = CANMSG;
		data = CANMSG;
		data = CANMSG;
		data = CANMSG;
		data = CANMSG;
		data = CANMSG;
		data = CANMSG;

		LED_DEBUG(data & 0x01);
	}

	CANSTMOB=0; /* clear all interrupt flags */
	CANCDMOB = 8|(1<<CONMOB1); /* enable rx, max data length */

	/* restore the current MOb page */
	CANPAGE = (CANPAGE & 0xF0)|canpage_bkp;
}
