#include <Servo.h>
#define STARTMARKER '<'
#define ENDMARKER   '>'

Servo servo[3];

const byte numBytes = 6;
byte pins[3];

byte userPrompt() {
  short val = -1;
  byte receivedBytes[numBytes];
  static bool receivingData = false;
  static byte idx = 0;

  while (true) {
    while (Serial.available()) {
      byte recv = Serial.read();
  
      if (recv == ENDMARKER) {
        receivingData = false;
        receivedBytes[idx] = '\0';
        val = 0;
        for (byte i = 0; i < idx; i++) {
          val += (receivedBytes[i]-'0') * ceil(pow(10, idx-i-1));
        }
        idx = 0;
      }
  
      if (receivingData) {
        receivedBytes[idx] = recv;
        idx++;
      }
  
      if (recv == STARTMARKER) {
        receivingData = true;
        memset(receivedBytes, '\0', numBytes);
      }
    }

    if (val >= 0) break;
  }
  return val;
}

void setup() {
  Serial.begin(9600);
  Serial.println("Please start with '<' and end with '>'!!");

  servo[0].attach(6);
  servo[1].attach(9);
  servo[2].attach(10);

//  for (byte i = 0; i < 3; i++) {
//    Serial.print("Please enter servo "); Serial.print(i+1);
//    Serial.println(" pin");
//    pins[i] = userPrompt();
//    servo[i].attach(pins[i]);
//    Serial.println(pins[i]);
//  }
}

void loop() {
  byte servoIdx, angle;
  
  Serial.println("Debug which servo?");
  servoIdx = userPrompt();
  Serial.println(servoIdx);
  Serial.println("How much angle?");
  Serial.println(angle);
  servo[servoIdx].write(angle);
}
