/*
    This file is part of AutoQuad.

    AutoQuad is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    AutoQuad is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with AutoQuad.  If not, see <http://www.gnu.org/licenses/>.

    Copyright © 2011-2014  Bill Nesbitt
*/

#include "canSensors.h"
#include "aq_timer.h"
#include "radio.h"
#include <CoOS.h>
#include "gps.h"
#include "comm.h" /* AQ_PRINTF() */
#include <stdio.h>
#include "util.h"
#include "config.h"
#include <string.h>

#define CAN_DOC_LAT 0x01
#define CAN_DOC_LON 0x02
#define CAN_DOC_DOP 0x03
#define CAN_DOC_ACC 0x04
#define CAN_DOC_VEL 0x05
#define CAN_DOC_ALT 0x06


canSensorsStruct_t canSensorsData;

void canSensorsReceiveTelem(uint8_t canId, uint8_t doc, void *data) {
    // Mathias
    // Check if switch is 0 (+-100 is limit)

    int16_t chan = radioData.channels[(int)(p[RADIO_AUX4_CH]-1)];
    if(canId == CAN_SENSORS_CAN_GPS ){
      if(chan > -100 && chan < 100){
        double data_double;
        memcpy(&data_double,data,8);
        switch(doc){
        case CAN_DOC_LAT:
          gpsData.lat = data_double;
          break;
        case CAN_DOC_LON:
          gpsData.lon = data_double;
          break;
        case CAN_DOC_DOP:
        {
          uint8_t* data_int = (uint8_t * ) data;

          gpsData.pDOP = ((float)data_int[0])/10;
          gpsData.hDOP = ((float)data_int[1])/10;
          gpsData.vDOP = ((float)data_int[2])/10;
          gpsData.tDOP = ((float)data_int[3])/10;
          gpsData.nDOP = ((float)data_int[4])/10;
          gpsData.eDOP = ((float)data_int[5])/10;
          gpsData.gDOP = ((float)data_int[6])/10;
        }
        break;
        case CAN_DOC_ACC:
        {
          uint8_t* data_int = (uint8_t * ) data;
          // Satellites
          gpsData.satellites = data_int[0];
          // GPS fix
          gpsData.fix = data_int[1];
          // Speed accuracy
          gpsData.sAcc = ((float)data_int[2])/10;
          // Course accuracy
          gpsData.cAcc = ((float)data_int[3])/10;
          // Horizontal accuracy
          gpsData.hAcc = ((float)data_int[4])/10;
          // Vertical accuracy
          gpsData.vAcc = ((float)data_int[5])/10;
          // Heading
          uint16_t * tmp = (uint16_t * )data;
          gpsData.heading = ((float)tmp[3])/100;
        }
        break;
        case CAN_DOC_VEL:
        {
          int16_t* data_int = (int16_t * ) data;
          // Satellites
          gpsData.velN  = ((float)data_int[0])/100;  //  m/s
          gpsData.velE  = ((float)data_int[1])/100;  //  m/s
          gpsData.velD  = ((float)data_int[2])/100;  //  m/s
          gpsData.speed = ((float)data_int[3])/100;  //  m/s
        }
        break;
        case CAN_DOC_ALT:
          gpsData.height = data_double;
          //if(gpsData.fix == 1){
            if(gpsData.hDOP < 3){
                if(gpsData.satellites >= 5){
                  //AQ_PRINTF("Recv. Valid GPGGA\n", 0);
                    gpsData.lastPosUpdate = timerMicros();
                    gpsData.lastVelUpdate = timerMicros();
                    CoSetFlag(gpsData.gpsPosFlag);
                    CoSetFlag(gpsData.gpsVelFlag);
                } else {
                  AQ_PRINTF("Satellites: %f \n", gpsData.satellites);
                }
            } else {
              AQ_PRINTF("hDOP: %f\n", (double)gpsData.hDOP);
             }
          //} else {
          //  AQ_PRINTF("Fix: %f\n", gpsData.fix);
          //}     
        break;
      } // End switch
     }  // End switch-check
    } // end canID check
    else {
      // Else just save the value
      canSensorsData.values[canId] = *(float *)data;
    }
    // record reception time
    canSensorsData.rcvTimes[canId] = timerMicros();
}

void canSensorsInit(void) {
    int i;

    for (i = 0; i < CAN_SENSORS_NUM; i++) {
        if ((canSensorsData.nodes[i] = canFindNode(CAN_TYPE_SENSOR, i)) != 0) {
            canTelemRegister(canSensorsReceiveTelem, CAN_TYPE_SENSOR);

            // request telemetry
            canSetTelemetryValue(CAN_TT_NODE, canSensorsData.nodes[i]->networkId, 0, CAN_TELEM_VALUE);
            canSetTelemetryRate(CAN_TT_NODE, canSensorsData.nodes[i]->networkId, CAN_SENSORS_RATE);
        }
    }
}
