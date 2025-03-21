#include<Servo.h>
#define numOfValsRec 5
#define digitsPerValRec 1

Servo servoThump;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1;//$00000
int counter = 0;
bool counterStart = false; //flag
String recievedString;

void setup() {
  Serial.begin(9600);
  servoThump.attach(7);
  servoIndex.attach(6);
  servoMiddle.attach(11);
  servoRing.attach(8);
  servoPinky.attach(10);
}

void recieveData(){
  while (Serial.available())
  {
    char c = Serial.read();
    
    if (c == '$'){
      counterStart = true;
    }
    if (counterStart){
      if (counter < stringLength){
        recievedString = String(recievedString + c);
        counter ++;
      }
      if (counter >= stringLength){
        //$00000
        for (int i = 0; i < numOfValsRec; i++){
          int num = (i * digitsPerValRec) + 1;
          valsRec[i] = recievedString.substring(num,num+digitsPerValRec).toInt();
        }
        recievedString = "" ;
        counter = 0;
        counterStart = false;
      }
    }
  }
}

void loop() {
  recieveData();
  if (valsRec[0] == 1){ servoThump.write(0);}else{ servoThump.write(175);}
  if (valsRec[1] == 1){ servoIndex.write(0);}else{ servoIndex.write(178);}
  if (valsRec[2] == 1){ servoMiddle.write(0);}else{ servoMiddle.write(175);}
  if (valsRec[3] == 1){ servoRing.write(0);}else{ servoRing.write(175);}
  if (valsRec[4] == 1){ servoPinky.write(0);}else{ servoPinky.write(175);} 
}
