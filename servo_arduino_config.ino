#include <Servo.h>
#define STARTMARKER '<'
#define ENDMARKER   '>'
#define DELIMIT     ":"
#define TEST_SERVO  "T"
#define SET_PIN     "S"

Servo servo[4];

const byte numBytes = 10;
byte pins[4];

void serialRead() {
  char data[numBytes];
  char* key;
  char* value;
  static byte idx = 0;
  static bool receivingData = false;
  
  while (Serial.available()) {
    byte recv = Serial.read();

    if (recv == ENDMARKER) {
      receivingData = false;
      data[idx] = NULL;
      key = strtok(data, DELIMIT);    // split data before ':'
      value = strtok(NULL, DELIMIT);  // split data after ':' and before end of str

      if (strcmp(key, TEST_SERVO) == 0) {  // scan for 'T' in key
        // e.g <T:0> or <T:1>
        char* splitData;
        byte v = strtol(value, &splitData, 10);   // convert str to long

        servo[v].write(0);
        delay(1000);
        servo[v].write(180);
        delay(1000);
        servo[v].write(0);
        delay(1000);
      }
      else if (strspn(key, SET_PIN) != 0) {   // scan for 'S' in key
        // e.g <S0:6>
        char extractedData[strlen(key)];
        char* splitData;
        byte k;
        byte v;
        for (byte i = 0; i < strlen(key)-1; i++) extractedData[i] = key[i+1];
        extractedData[strlen(key)-1] = NULL;
        
        k = strtol(extractedData, &splitData, 10);
        v = strtol(value, &splitData, 10);
//        pins[k] = v;    // debug use
        if (servo[k].attached() == true) servo[k].detach();
        servo[k].attach(v);
      }
      else {
        // e.g <1:180>
        char* splitData;
        byte k = strtol(key, &splitData, 10);   // convert str to long
        byte v = strtol(value, &splitData, 10); // convert str to long
        servo[k].write(v);  
      }
      idx = 0;
    }

    if (receivingData) data[idx++] = recv;
    
    if (recv == STARTMARKER) receivingData = true;
  }
}

void setup() {
  Serial.begin(9600);
//  Serial.println("Please start with '<' and end with '>'!!");
}

void loop() {
  serialRead();
}
