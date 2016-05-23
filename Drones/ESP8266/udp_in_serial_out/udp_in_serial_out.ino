#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>

#define PACKET_SIZE 34

/* SLIP special character codes  */
#define SLIP_END    192      /* 0xC0 indicates end of packet */
#define SLIP_ESC    219      /* 0xDB indicates byte stuffing */
#define SLIP_ESC_END  220    /* 0xDC ESC ESC_END means END data byte */
#define SLIP_ESC_ESC  221    /* 0xDD ESC ESC_ESC means ESC data byte */

// wifi connection variables
const char* ssid = "ESPtest";
const char* password = "12345678";

boolean wifiConnected = false;

// UDP variables
unsigned int localPort = 8888;
WiFiUDP UDP;
boolean udpConnected = false;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet,
char ReplyBuffer[] = "acknowledged"; // a string to send back
char ReplyBufferPktTooSmall[] = "Pkt too small";
char ReplyBufferOk[] = "ok"; // a string to send back

void setup() {
  // Initialise Serial connection
  Serial.begin(9600);

  // Keep trying to connect to AP
  do {
    wifiConnected = connectWifi();
  } while(!wifiConnected);

  udpConnected = connectUDP();

  // Start OTA server.
  ArduinoOTA.setHostname("Drone2");
  ArduinoOTA.begin();
}


void loop() {
  // check if the WiFi and UDP connections were successful
  if (wifiConnected) {
    if (udpConnected) {
      // if there’s data available, read a packet
      int packetSize = UDP.parsePacket();
      UDP.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
      
      if(packetSize == PACKET_SIZE){

        //Serial.write(SLIP_END);
        for(int i = 0; i < PACKET_SIZE; i++){
          switch(packetBuffer[i]){
            case SLIP_END:
              Serial.write(SLIP_ESC);
              Serial.write(SLIP_ESC_END);
            break;
            
            case SLIP_ESC:
              Serial.write(SLIP_ESC);
              Serial.write(SLIP_ESC_ESC);
            break;

            default:
              Serial.write(packetBuffer[i]);
          }
        }
        Serial.write(SLIP_END);

        UDP.beginPacket(UDP.remoteIP(), UDP.remotePort());
        UDP.write(ReplyBufferOk);
        UDP.endPacket();
        delay(10);
      } else {
        UDP.beginPacket(UDP.remoteIP(), UDP.remotePort());
        UDP.write(ReplyBufferPktTooSmall);
        UDP.endPacket();
        delay(10);
      }
    }

  }
    // Handle OTA server.
  ArduinoOTA.handle();
}

// connect to UDP – returns true if successful or false if not
boolean connectUDP() {
  boolean state = false;

  Serial.println("");
  Serial.println("Connecting to UDP");

  if (UDP.begin(localPort) == 1) {
    Serial.println("Connection successful");
    state = true;
  }
  else {
    Serial.println("Connection failed");
  }

  return state;
}
// connect to wifi – returns true if successful or false if not
boolean connectWifi() {
  boolean state = true;
  int i = 0;
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("Connecting to WiFi");

  // Wait for connection
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (i > 10) {
      state = false;
      break;
    }
    i++;
  }
  if (state) {
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  }
  else {
    Serial.println("");
    Serial.println("Connection failed.");
  }
  return state;
}
