#include <Arduino.h>

#define TOF_SERIAL Serial1

// Define constants for frame head and tail
#define FRAME_HEAD_1 0x00
#define FRAME_HEAD_2 0xFF
#define FRAME_TAIL 0xDD

uint8_t rawData[4096*3]; // Assuming the maximum data length
//uint8_t frameData[4096]; // Assuming the maximum data length

void setup() {
  Serial.begin(1500000);
  Serial.println("Starting");
  // Delays prevent uart issues
  delay(1000);
  TOF_SERIAL.begin(115200);
  TOF_SERIAL.write("AT+BAUD=5\r");
  TOF_SERIAL.end();
  
  delay(200);
  TOF_SERIAL.begin(921600);
  delay(200);
  TOF_SERIAL.clear();
  delay(200);
  //delay(100);
  TOF_SERIAL.write("AT+DISP=5\r");
  delay(200);
  TOF_SERIAL.write("AT+FPS=7\r");
  //TOF_SERIAL.write("AT+SAVE\r");
  //
  
  Serial.println("done config");
}
int idx;
    uint16_t dataLen, frameLen, frameDataLen;
    uint8_t frameTail, _sum;
    uint16_t frameID;
    uint8_t resR, resC;

    uint8_t head1flag = 0;

void getSerialBytes(uint8_t* data, uint16_t len)
{
  uint16_t counter=0;

  while(counter < len)
  {
    if(TOF_SERIAL.available())
    {
      data[counter]= TOF_SERIAL.read();
      counter++;
    }
  }
}
void loop() {

    // Read data from UART
    if (TOF_SERIAL.available()) 
    {
        rawData[0] = TOF_SERIAL.read();
        //Serial.println("new data");
        //Serial.print(rawData[0],HEX);
        //Serial.print(" ");

        // Find frame head
        if (rawData[0] == FRAME_HEAD_1) 
        {
          //Serial.println("point 1");
          getSerialBytes(&rawData[1], 1);
          //Serial.println("point 2");
          if(rawData[1] == FRAME_HEAD_2)
          {
            //Serial.println("HEAD FOUND");
            getSerialBytes(&rawData[2], 2);

            dataLen = (rawData[2]) | (rawData[3] << 8);
            //Serial.print("data len: ");
            //Serial.println(dataLen);

            getSerialBytes(&rawData[4], dataLen);
            
            /*
            https://wiki.sipeed.com/hardware/en/maixsense/maixsense-a010/at_command_en.html#UNIT-directive
            +-------------+-----------------------------------------------------------------------------------
            | Bytes       | Purpose
            +-------------+-----------------------------------------------------------------------------------
            | 0-1         | frame head 
            | 2-3         | data len (excludes checksum or end of transmission bytes) encoded little endian (should be 10016 for 100x100 resolution)
            | 4-10019     | data (first 16 bytes is meta data, rest is real data)
            | 10019-10021 | checksum (lower 8 bits) and end of transmission (EOT) 0xDD
            */
            Serial.print("S");
            uint16_t row = 0;
            for(uint16_t i = 0; i< 10000; i++)
            {
              Serial.print(rawData[i+20], HEX); 
              Serial.print(","); 
              /*
              row ++;
              if(row == 100)
              {
                Serial.println("");
                row =0;
              }*/
            }
            Serial.println("N"); 
            //Serial.println(rawData[5000]); 
            // The data is exponentially scaled so values futher away are less accurate than values closer to the sensor. changing the UNIT from 0 to another number (1-9), linear scale, less range. data in mm
            //Serial.println((rawData[5000]/5.1)*(rawData[5000]/5.1));

            uint8_t endbytes[2];
            getSerialBytes(&endbytes[0], 2);

            //Serial.print("checksum: "); 
            //Serial.println(endbytes[0]);
            //Serial.print("eot: ");
            //Serial.println(endbytes[1],HEX);
            
          }
          
        }
    }
    
}

