/*
 * queue.h
 *
 *  Created on: May 10, 2016
 *      Author: Mathias Neerup
 */

#ifndef QUEUE_H_
#define QUEUE_H_


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef struct {
        uint8_t wr;
        uint8_t rd;
        uint8_t typesize;
        uint8_t queuesize;
        uint32_t* mem;
        uint8_t elements;
        uint8_t id;
} QueueHandle_t;


QueueHandle_t QueueCreate(uint8_t queuesize, uint8_t typesize);
uint8_t QueueSend(QueueHandle_t *queue, const void * dataIn);
uint8_t QueueSpaceLeft(QueueHandle_t *queue);
uint8_t QueuePeek(QueueHandle_t *queue, void * dataOut);
uint8_t QueueReceive(QueueHandle_t *queue, void * dataOut);

#endif /* QUEUE_H_ */
