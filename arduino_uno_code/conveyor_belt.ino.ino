#define MOTOR_A1 9
#define MOTOR_A2 10

void setup()
{   
    Serial.begin(9600);
    pinMode(A0,INPUT);
    pinMode(MOTOR_A1, OUTPUT);
    pinMode(MOTOR_A2, OUTPUT);
}

void loop()
{
  char input = 'B';
  if(Serial.available() > 0) { //시리얼에 값이 있으면
    Serial.println("input:");
    input = Serial.read(); //시리얼 값을 읽어라
    Serial.println(input);
  }

  //unsigned int vr = map(analogRead(A0), 0, 1023, 0,511);
  if(input=='A'){
        analogWrite(MOTOR_A1, 511);
        analogWrite(MOTOR_A2, 0);
        Serial.print("stop - ");
        Serial.println(0);
        delay(4000);
  }
  else{    
        analogWrite(MOTOR_A1, 0);
        analogWrite(MOTOR_A2, 0);
        Serial.print("front - ");
        Serial.println(0);
  }
  delay(100);

}
