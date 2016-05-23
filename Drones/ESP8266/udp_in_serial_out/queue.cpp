/*
 * queue.cpp
 *
 *  Created on: May 10, 2016
 *      Author: Mathias Neerup
 */

#include "queue.h"



QueueHandle_t QueueCreate(uint8_t queuesize, uint8_t typesize){
  static uint8_t id_count = 0;
  QueueHandle_t currentQueue;
  currentQueue.mem = (uint32_t*)calloc(queuesize, typesize);


  currentQueue.wr = 0;
  currentQueue.rd = 0;
  currentQueue.typesize = (typesize);
  currentQueue.queuesize = queuesize;
  currentQueue.elements = 0;
  currentQueue.id = id_count++;
  return currentQueue;
}


uint8_t QueueSend(QueueHandle_t *queue, const void * dataIn){
	uint8_t retval = false;
/*
	//Write-pointer overrun
	queue->wr %= queue->queuesize;

	if(queue->elements < queue->queuesize){
		++queue->elements;
		//Copy content of void * dataIn to the queue, and increment write-pointer
		memcpy ( queue->mem+((queue->typesize)*(queue->wr++)), dataIn, queue->typesize );
		retval = true;
	}

*/
	uint8_t wr_next = (queue->wr+1 )% queue->queuesize;

	if(wr_next != queue->rd){
		//queue->elements++;
		memcpy ( queue->mem+((queue->typesize)*(queue->wr)), dataIn, queue->typesize );
		retval = 1;
		queue->wr = wr_next;
	}
	return retval;
}

uint8_t QueueReceive(QueueHandle_t *queue, void * dataOut){
	uint8_t retval = false;
/*
	//check if data is available
	if(queue->elements > 0){
		--queue->elements;
		//Copy content of queue to dataOut
		memcpy( dataOut, queue->mem+((queue->typesize)*(queue->rd++)), queue->typesize);
		//Pointer read overrun
		queue->rd %= queue->queuesize;
		retval = true;
	}
*/
	if(queue->wr != queue->rd){
		//queue->elements--;
		memcpy( dataOut, queue->mem+((queue->typesize)*(queue->rd)), queue->typesize);
		queue->rd = (queue->rd + 1) % queue->queuesize;
		retval=true;
	} else {
		//no items or queue full
		retval = false;
	}

	return retval;
}

uint8_t QueueSpaceLeft(QueueHandle_t *queue){
	return ((queue->queuesize)-(queue->elements));
}

uint8_t QueuePeek(QueueHandle_t *queue, void * dataOut){
	uint8_t retval = false;

	//check if data is available
	if(queue->elements > 0){
		//Copy content of queue to dataOut
		memcpy( dataOut, queue->mem+(queue->typesize*queue->rd), queue->typesize);
		retval = true;
	}

	return retval;
}


/*
int main(){

	QueueHandle_t Queue1 = QueueCreate(8, sizeof(char));
	char dataOut;

	char dataIn = 'A';
	QueueSend(&Queue1, &dataIn);
	dataIn = 'B';
	QueueSend(&Queue1, &dataIn);
	dataIn = 'C';
	QueueOverwrite(&Queue1,&dataIn);
	dataIn = 'D';
	QueueSend(&Queue1, &dataIn);
	dataIn = 'E';
	QueueSend(&Queue1, &dataIn);
	dataIn = 'F';
	QueueSend(&Queue1, &dataIn);
	dataIn = 'G';
	QueueSend(&Queue1, &dataIn);
	dataIn = 'H';
	QueueSend(&Queue1, &dataIn);

	dataIn = 'I';
	QueueOverwrite(&Queue1, &dataIn);
	dataIn = 'J';
	QueueOverwrite(&Queue1, &dataIn);

	int i = 0;
	for(; i < 10; i++){
		if(QueueReceive(&Queue1, &dataOut)){
			uartprintf("%d: Out from queue: %c \r\n",i ,dataOut);
		} else {
			uartprintf("No data available\r\n");
		}
	}

	return 1;
}
*/
