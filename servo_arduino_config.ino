#include <Servo.h>
#define STARTMARKER '<'
#define ENDMARKER   '>'

Servo servo[3];

const byte numBytes = 6;
byte pins[3];

struct servoStruct {
  short activePin = -1;
  short angle = -1;
} ss;

servoStruct userPromptGUI() {
  servoStruct temp;
  short val = -1;
  byte receivedBytes[numBytes];
  byte dividerPos = 0;
  static bool receivingData = false;
  static byte idx = 0;

  while (true) {
    while (Serial.available()) {
      byte recv = Serial.read();
  
      if (recv == ENDMARKER) {
        receivingData = false;
        receivedBytes[idx] = '\0';
        if (idx != 1) {
          temp.angle = 0;
          for (byte i = dividerPos+1; i < idx; i++) {
            temp.angle += (receivedBytes[i]-'0') * ceil(pow(10, idx-i-1));
          }
  //        Serial.println(ss.activePin);
  //        Serial.println(ss.angle);
        }
        else {
          servo[receivedBytes[0]-'0'].write(0);
          delay(1000);
          servo[receivedBytes[0]-'0'].write(180);
          delay(1000);
          servo[receivedBytes[0]-'0'].write(0);
        }
        idx = 0;
      }
      
      if (receivingData) {
        receivedBytes[idx] = recv;
        if (recv == ':') {
          dividerPos = idx;
          temp.activePin = 0;
          for (byte i = 0; i < dividerPos; i++) {
            temp.activePin += (receivedBytes[i]-'0') * ceil(pow(10, dividerPos-i-1));
          }
        }
        idx++;
      }
  
      if (recv == STARTMARKER) {
        receivingData = true;
        memset(receivedBytes, '\0', numBytes);
      }
    }
    if (temp.angle >= 0 && temp.activePin >= 0) break;
  }
  return temp;
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
   ss = userPromptGUI();
  if (ss.activePin != -1 && ss.angle != -1) {
    servo[ss.activePin].write(ss.angle);
  }
  ss.activePin = -1;
  ss.angle = -1;
  Serial.flush();
}
