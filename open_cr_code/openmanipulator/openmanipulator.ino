#include <DynamixelWorkbench.h>

#if defined(__OPENCM904__)
#define DEVICE_NAME "3"  //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
#define DEVICE_NAME ""
#endif

#define BAUDRATE 1000000
#define DXL_ID1 11
#define DXL_ID2 12
#define DXL_ID3 13
#define DXL_ID4 14
#define DXL_ID5 15

int counte1 = 0;
int counte2 = 0;
int counte3 = 0;
int countb = 0;
int countf = 0;

DynamixelWorkbench dxl_wb;

bool result = false;

uint8_t dxl_id1 = DXL_ID1;
uint8_t dxl_id2 = DXL_ID2;
uint8_t dxl_id3 = DXL_ID3;
uint8_t dxl_id4 = DXL_ID4;
uint8_t dxl_id5 = DXL_ID5;

uint16_t model_number = 0;

void setup() {
  const char *log;

  Serial.begin(115200);  // baud rate
  //while (!Serial) {

  result = dxl_wb.init(DEVICE_NAME, BAUDRATE, &log);
  if (result == false) {
    Serial.println(log);
    Serial.println("Failed to init");
  } else {
    Serial.print("Succeeded to init : ");
    Serial.println(BAUDRATE);
  }

  result = (dxl_wb.ping(dxl_id1, &model_number, &log) && dxl_wb.ping(dxl_id2, &model_number, &log) && dxl_wb.ping(dxl_id3, &model_number, &log) && dxl_wb.ping(dxl_id4, &model_number, &log) && dxl_wb.ping(dxl_id5, &model_number, &log));
  if (result == false) {
    Serial.println(log);
    Serial.println("Failed to ping");
  } else {
    Serial.println("Succeeded to ping");
    Serial.print("id : ");
    //Serial.print(dxl_id);
    Serial.print(" model_number : ");
    Serial.println(model_number);
  }

  result = (dxl_wb.jointMode(dxl_id1, 0, 0, &log) && dxl_wb.jointMode(dxl_id2, 0, 0, &log) && dxl_wb.jointMode(dxl_id3, 0, 0, &log) && dxl_wb.jointMode(dxl_id4, 0, 0, &log) && dxl_wb.jointMode(dxl_id5, 0, 0, &log));
  if (result == false) {
    Serial.println(log);
    Serial.println("Failed to change joint mode");
  } else {
    Serial.println("Succeed to change joint mode");
    Serial.println("Dynamixel is moving...");

    // first position
    dxl_wb.goalPosition(dxl_id1, (int32_t)2048);  // 11
    dxl_wb.goalPosition(dxl_id2, (int32_t)2048);  // 12
    dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
    dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
    dxl_wb.goalPosition(dxl_id5, (int32_t)1023);  // 15
    delay(5000);


    //        // 15 : (int32_t) 1023 ~ 3000
    //        // 14 : (int32_t) 2048 ~ 3072 rect
    //        // 13 : (int32_t) 1024 ~ 2048 rect
    //        // 12 : (int32_t) 1024 ~ 2048 rect
    //        // 11 : right 1024 front 2048 left 3072
    //      }
  }
  //}
}

void loop() {
  // put your main code here, to run repeatedly:
  // if (Serial.available() > 0) {
  char input = 'K';

  if(Serial.available() > 0) { //시리얼에 값이 있으면
    Serial.println("input:");
    input = Serial.read(); //시리얼 값을 읽어라
    Serial.println(input);
  }

  if(input=='E'){
    economy3();
    delay(100);
  }
  else if(input=='B'){    
    business();
    delay(100);
  }
  else if(input=='F'){
    first();
    delay(100);
  }
  else if(input=='G'){
    economy2();
    delay(100);
  }
  else if(input=='H'){
    economy1();
    delay(100);
  }  
  delay(100);

}

void economy1() {

  uint8_t dxl_id1 = DXL_ID1;
  uint8_t dxl_id2 = DXL_ID2;
  uint8_t dxl_id3 = DXL_ID3;
  uint8_t dxl_id4 = DXL_ID4;
  uint8_t dxl_id5 = DXL_ID5;

  // grip
  dxl_wb.goalPosition(dxl_id3, (int32_t)1520);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2700);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2690);  // 2720
  delay(2000);

  // if ( "3cm이면" ) {
  //   dxl_wb.goalPosition(dxl_id5, (int32_t)2300); // 3cm
  // } else {
  //   dxl_wb.goalPosition(dxl_id5, (int32_t)2020); // 4cm
  // }
  dxl_wb.goalPosition(dxl_id5, (int32_t)2300);  // 1820 5cm 2020 4cm 2300 3cm
  delay(2000);

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  delay(2000);

  // rotate
  dxl_wb.goalPosition(dxl_id1, (int32_t)(3072 + counte1 * 120));
  delay(2000);

  // put
  dxl_wb.goalPosition(dxl_id3, (int32_t)1365);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2660);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2870);  // 2830
  delay(2000);

  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);
  delay(200);

  // first position

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id1, (int32_t)2048);  // 11
  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);  // 15
  delay(3000);

  counte1 += 1;
}


void economy2() {

  uint8_t dxl_id1 = DXL_ID1;
  uint8_t dxl_id2 = DXL_ID2;
  uint8_t dxl_id3 = DXL_ID3;
  uint8_t dxl_id4 = DXL_ID4;
  uint8_t dxl_id5 = DXL_ID5;

  // grip
  dxl_wb.goalPosition(dxl_id3, (int32_t)1520);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2700);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2690);  // 2720
  delay(2000);

  dxl_wb.goalPosition(dxl_id5, (int32_t)2300);  // 1820 5cm 2020 4cm 2300 3cm
  delay(2000);

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  delay(2000);

  // rotate
  dxl_wb.goalPosition(dxl_id1, (int32_t)(3560 + counte2 * 120));
  delay(2000);

  // put
  dxl_wb.goalPosition(dxl_id3, (int32_t)1365);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2660);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2870);  // 2830
  delay(2000);

  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);
  delay(200);

  // first position

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id1, (int32_t)2048);  // 11
  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);  // 15
  delay(3000);

  counte2 += 1;
}

void economy3() {

  uint8_t dxl_id1 = DXL_ID1;
  uint8_t dxl_id2 = DXL_ID2;
  uint8_t dxl_id3 = DXL_ID3;
  uint8_t dxl_id4 = DXL_ID4;
  uint8_t dxl_id5 = DXL_ID5;

  // grip
  dxl_wb.goalPosition(dxl_id3, (int32_t)1520);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2700);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2690);  // 2720
  delay(2000);

  dxl_wb.goalPosition(dxl_id5, (int32_t)2300);  // 1820 5cm 2020 4cm 2300 3cm
  delay(2000);

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  delay(2000);

  // rotate
  dxl_wb.goalPosition(dxl_id1, (int32_t)(3980 + counte3 * 120));
  delay(2000);

  // put
  dxl_wb.goalPosition(dxl_id3, (int32_t)1365);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2660);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2870);  // 2830
  delay(2000);

  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);
  delay(200);

  // first position

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id1, (int32_t)2048);  // 11
  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);  // 15
  delay(3000);

  counte3 += 1;
}

void business() {

  uint8_t dxl_id1 = DXL_ID1;
  uint8_t dxl_id2 = DXL_ID2;
  uint8_t dxl_id3 = DXL_ID3;
  uint8_t dxl_id4 = DXL_ID4;
  uint8_t dxl_id5 = DXL_ID5;

  // grip
  dxl_wb.goalPosition(dxl_id3, (int32_t)1520);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2700);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2690);  // 2720
  delay(2000);

  dxl_wb.goalPosition(dxl_id5, (int32_t)2300);  // 1820 5cm 2020 4cm 2300 3cm
  delay(2000);

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  delay(2000);

  // rotate
  dxl_wb.goalPosition(dxl_id1, (int32_t)(500 + countb * 120));
  delay(2000);

  // put
  dxl_wb.goalPosition(dxl_id3, (int32_t)1365);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2660);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2870);  // 2830
  delay(2000);

  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);
  delay(200);

  // first position

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id1, (int32_t)2048);  // 11
  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);  // 15
  delay(3000);

  countb += 1;
}

void first() {

  uint8_t dxl_id1 = DXL_ID1;
  uint8_t dxl_id2 = DXL_ID2;
  uint8_t dxl_id3 = DXL_ID3;
  uint8_t dxl_id4 = DXL_ID4;
  uint8_t dxl_id5 = DXL_ID5;

  // grip
  dxl_wb.goalPosition(dxl_id3, (int32_t)1520);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2700);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2690);  // 2720
  delay(2000);

  dxl_wb.goalPosition(dxl_id5, (int32_t)2300);  // 1820 5cm 2020 4cm 2300 3cm
  delay(2000);

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  delay(2000);

  // rotate
  dxl_wb.goalPosition(dxl_id1, (int32_t)(1024 + countf * 120));
  delay(2000);

  // put
  dxl_wb.goalPosition(dxl_id3, (int32_t)1365);
  delay(1000);
  dxl_wb.goalPosition(dxl_id4, (int32_t)2660);  // delay(1000);
  dxl_wb.goalPosition(dxl_id2, (int32_t)2870);  // 2830
  delay(2000);

  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);
  delay(200);

  // first position

  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);
  delay(1000);                                  // 12
  dxl_wb.goalPosition(dxl_id1, (int32_t)2048);  // 11
  dxl_wb.goalPosition(dxl_id2, (int32_t)2048);  // 12
  dxl_wb.goalPosition(dxl_id3, (int32_t)2048);  // 13
  dxl_wb.goalPosition(dxl_id4, (int32_t)2400);  // 14
  dxl_wb.goalPosition(dxl_id5, (int32_t)1023);  // 15
  delay(3000);

  countf += 1;
}