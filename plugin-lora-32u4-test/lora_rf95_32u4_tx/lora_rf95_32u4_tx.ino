// Feather9x_TX
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messaging client (transmitter)
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.

#include <SPI.h>
#include <RH_RF95.h>

/* for feather32u4 */
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 7

/* for feather m0  
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3
*/

// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup()
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(115200);
  while (!Serial)
  {
    delay(1);
  }

  delay(100);

  //Serial.println("Feather LoRa TX Test!");

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init())
  {
    Serial.println("LoRa radio init failed");
    Serial.println("Uncomment '#define SERIAL_DEBUG' in RH_RF95.cpp for detailed debug info");
    while (1)
      ;
  }
  Serial.println("32u4 RFM95 Tx 1");
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ))
  {
    Serial.println("setFrequency failed");
    while (1)
      ;
  }
  Serial.print("Set Freq to: ");
  Serial.println(RF95_FREQ);

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
}

static char recv_buf[512];

void loop()
{
  while (!Serial.available())
    ;

  // char radiopacket[240] = Serial.readString().c_str();

  // Serial.print(Serial.readString().c_str());

  //String s = Serial.readStringUntil('\r');   // Until CR (Carriage Return)
  String s = Serial.readString();

  //Serial.print(s);

  //String s = "Position,dd2a341d-c238-4f5f-afdc-fd7275ed4b8e,2021-10-08T20:24:37.451Z,Greg_Fire,38.78314000000002,-77.01496,0.001"; //Serial.readString();

  //    Serial.print(s);

  char radiopacket[s.length()];

  for (int i = 0; i < s.length(); i++)
  {
    radiopacket[i] = (char)s[i];
  }

  Serial.println("before send");

  rf95.send((uint8_t *)radiopacket, s.length());

  Serial.println("32u4 RFM95 Tx 1");
  Serial.println(s);

  delay(10);
}
