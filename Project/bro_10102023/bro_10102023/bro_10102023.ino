/*  Example code for the Social Robot Interaction course
    Code Changed by Venkat - 10-10-2023

    Connections:
    // MP3 MODULE    -> <Laptop Audio>
    LED EYES      -> <Footrest LED1  D3 , Headrest LED2 D1>
    SERVOS        -> D7
    TOUCH_SENSOR  -> A0
    HUSKY_LENS    -> I2C <To be Removed>
*/

// --------------------------------------------------------------------------------- //
// ----------------------------------- VARIABLES ----------------------------------- //
// --------------------------------------------------------------------------------- //
// Let's start by including the needed libraries
#include <Adafruit_NeoPixel.h>
#include <SoftwareSerial.h>
#include <MP3Player_KT403A.h>
#include "HUSKYLENS.h"
#include <Servo.h>

// Then we define global constants
#define LED_PIN_1     4
#define LED_COUNT_1   37

#define LED_PIN_2     5
#define LED_COUNT_2   37

#define TOUCH_PIN     A0
#define SERVO_PIN_1   8
#define SERVO_PIN_2   7

Adafruit_NeoPixel pixels1(LED_COUNT_1, LED_PIN_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels2(LED_COUNT_2, LED_PIN_2, NEO_GRB + NEO_KHZ800);

int LED_BRIGHTNESS = 10;  // 0-255

bool prev_touch_value = 0;
enum Emotion {NEUTRAL, HAPPY, SAD, CONFIRMATION};
Emotion emotion = NEUTRAL;

enum Color {RED, GREEN, BLUE, ORANGE};
Color color = BLUE;

Servo S_headrest, S_footrest;

int S_headrest_angle = 90;
int S_footrest_angle = 90;

long timer1, timer2, timer3;

bool pc_connected = false;

bool voice_switch = false;

byte neutral[] = {
  B0000,
  B01110,
  B011110,
  B0111110,
  B011110,
  B01110,
  B0000
};

byte happy[] = {
  B1111,
  B11111,
  B111111,
  B1100011,
  B000000,
  B00000,
  B0000
};

byte sad[] = {
  B0000,
  B00001,
  B000011,
  B0001111,
  B011111,
  B11111,
  B1111
};

byte confirmation[] = {
  B1111,
  B11111,
  B111111,
  B1111111,
  B111111,
  B11111,
  B1111
};


void setup() {
  // put your setup code here, to run once:
  // put your setup code here, to run once:
  pinMode(TOUCH_PIN, INPUT);

  // Initialize the NeoPixel libraries
  pixels1.begin();
  pixels1.show();
  
  pixels2.begin();
  pixels2.show();

  // Serial communication
  Serial.begin(115200);

  // Servos
  S_headrest.attach(SERVO_PIN_1);
  S_footrest.attach(SERVO_PIN_2);
  // servo1.write(90);
  // servo2.write(90);
}

void loop() {
  bool touch_value = digitalRead(TOUCH_PIN);

  if(touch_value && voice_switch){
    voice_switch = false;
    selectMovement(1, pixels1.Color(0, 0, 0), pixels2.Color(0, 0, 0));
  }

  else if(touch_value && !voice_switch){
    voice_switch = true;
    selectMovement(1, pixels1.Color(255, 255, 255) , pixels2.Color(255, 255, 255));
  }

  if(voice_switch){
    if (millis() - timer2 >= 10 && voice_switch){
      timer2 = millis();
      communication();
    }
  }
}

void colorWipe(Adafruit_NeoPixel &strip, uint32_t color, int wait, int LED_BRIGHTNESS) {
  for (int i = 0; i < strip.numPixels(); i++) {
    uint8_t r = (color >> 16) & 0xFF; // Extract red component
    uint8_t g = (color >> 8) & 0xFF;  // Extract green component
    uint8_t b = color & 0xFF;         // Extract blue component

    r = (r * LED_BRIGHTNESS) / 255;   // Adjust red component brightness
    g = (g * LED_BRIGHTNESS) / 255;   // Adjust green component brightness
    b = (b * LED_BRIGHTNESS) / 255;   // Adjust blue component brightness

    strip.setPixelColor(i, strip.Color(r, g, b));
    strip.show();
    // delay(wait);
  }
  // strip.clear();
}

void switchOffLED(Adafruit_NeoPixel &strip){
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));
    strip.show();
  }
}

// --------------------------------------------------------------------------------- //
// ---------------------------------- SERVO MOTORS --------------------------------- //
// --------------------------------------------------------------------------------- //
// Duration of each breath cycle in milliseconds
// frequency Adjust this to change the speed of breathing
// Calculate the step size based on frequency and duration for smooth breathing
void moveServo(int position, int duration, double frequency, bool mirror, Servo serv){
  int startPos = position+20;
  int endPos = position-20;
  float stepSize = (2 * PI) / (duration / 2);
  // Perform a breathing cycle
  for (float t = 0; t <= PI; t += stepSize) {
    int pos = startPos + ((endPos - startPos) / 2) * (1 + sin(t));
    if(mirror == true){
      S_footrest.write(pos);
    }
    serv.write(pos);
    delay(15);
  }
}



void setHeadrest(int endPos){
  int increment = 1;  // Increment step for smooth movement
  int delayTime = 15; // Delay time between steps (adjust as needed)
  S_footrest.detach();

  if (S_headrest_angle < endPos) {
    for (int pos = S_headrest_angle; pos <= endPos; pos += increment) {
      S_headrest.write(pos);
      delay(delayTime);
    }
  } else {
    for (int pos = S_headrest_angle; pos >= endPos; pos -= increment) {
      S_headrest.write(pos);
      delay(delayTime);
    }
  }
  S_headrest_angle = endPos;
  S_footrest.attach(SERVO_PIN_2);
}

void setFootrest(int endPos){
  int increment = 1;  // Increment step for smooth movement
  int delayTime = 15; // Delay time between steps (adjust as needed)
  S_headrest.detach();

  if (S_footrest_angle < endPos) {
    for (int pos = S_footrest_angle; pos <= endPos; pos += increment) {
      S_footrest.write(pos);
      delay(delayTime);
    }
  } else {
    for (int pos = S_footrest_angle; pos >= endPos; pos -= increment) {
      S_footrest.write(pos);
      delay(delayTime);
    }
  }
  S_footrest_angle = endPos;
  S_headrest.attach(SERVO_PIN_1);
}

uint32_t hexToRGB_P2(String hexColorString) {
  // Remove the leading "0x" if it's present
  if (hexColorString.startsWith("0x")) {
    hexColorString = hexColorString.substring(2);
  }
  
  // Convert the hex string to an unsigned long
  unsigned long hexColor = strtoul(hexColorString.c_str(), NULL, 16);
  
  int red = (hexColor >> 16) & 0xFF;
  int green = (hexColor >> 8) & 0xFF;
  int blue = hexColor & 0xFF;
  return pixels2.Color(red, green, blue);  
}

uint32_t hexToRGB_P1(String hexColorString) {
  // Remove the leading "0x" if it's present
  if (hexColorString.startsWith("0x")) {
    hexColorString = hexColorString.substring(2);
  }
  
  // Convert the hex string to an unsigned long
  unsigned long hexColor = strtoul(hexColorString.c_str(), NULL, 16);
  
  int red = (hexColor >> 16) & 0xFF;
  int green = (hexColor >> 8) & 0xFF;
  int blue = hexColor & 0xFF;
  return pixels1.Color(red, green, blue);  
}

void selectMovement(int i, uint32_t headrestpixel, uint32_t footrestpixel){
  switch (i) {
    case 0:
      colorWipe(pixels1, headrestpixel, 0, LED_BRIGHTNESS); // Cyan
      colorWipe(pixels2, footrestpixel, 0, LED_BRIGHTNESS); // Cyan
      break;
    case 1:
      //wake up bro
      colorWipe(pixels1, headrestpixel, 0, LED_BRIGHTNESS); // Cyan
      colorWipe(pixels2, footrestpixel, 0, LED_BRIGHTNESS); // Cyan
      moveServo(90, 200, 0.5, true, S_headrest);
      break;
    case 2: //waiting after showing 2 options (head and foot)
      S_headrest.detach();
      S_footrest.detach();
      colorWipe(pixels1, headrestpixel, 0, LED_BRIGHTNESS); // Cyan
      colorWipe(pixels2, footrestpixel, 0, LED_BRIGHTNESS); // Cyan
      delay(150);
      switchOffLED(pixels1);
      switchOffLED(pixels2);
      delay(150);
      S_headrest.attach(SERVO_PIN_1);
      S_footrest.attach(SERVO_PIN_2);
      break;
    case 3:
      //select headrest
      colorWipe(pixels1, headrestpixel, 0, LED_BRIGHTNESS); // Cyan
      moveServo(S_headrest_angle, 200, 1, false, S_headrest);
      switchOffLED(pixels1);
      break;
    case 4:
      //select footrest
      colorWipe(pixels2, footrestpixel, 0, LED_BRIGHTNESS); // Cyan
      moveServo(S_footrest_angle, 200, 1, false, S_footrest);
      switchOffLED(pixels2);
      break;
    default:
      Serial.println("Unknown switch state");
      break;
  }
}

// --------------------------------------------------------------------------------- //
// --------------------------------- COMMUNICATION --------------------------------- //
// --------------------------------------------------------------------------------- //
void communication() {
  char val = ' ';
  String data = "";
  if (Serial.available()) {
    do {
      val = Serial.read();
      if (val != -1) data = data + val;
    }
    while ( val != -1);
  }

  // data is a string of what we received, we will split it into the different values
  // We receive multiple values from our PC as in "123,abc,123,"
  // We can then split this string and extract the values out.
  if (data.length() > 1 && data.charAt(data.length() - 1) == ',') {
    // Serial.print(data);
    pc_connected = true; // Once we get a message from the PC, we turn off the touch sensor and do everything with input from the PC

    int value1, value2;// val1 is method, val2 is inpout
    String value3, value4;

    String value;
    for (int i = 0; data.length() > 0; i++){
      value = data.substring(0, data.indexOf(','));
      data = data.substring(data.indexOf(',') + 1, data.length());

      // The serial trigger is of the form '<x>,<y>'
      // where x is the variable to select the robot mode; possible values : [0,1,2]
      // 0: SelectMovement
      // 1: Set headrest
      // 2: Set footrest
      // where y is the variable to pass to these functions
      // range of [1,2,3,4] for selectmovement and [0,180] for setting headrest/footrest positions

      if (i == 0) value1 = value.toInt(); 
      if (i == 1) value2 = value.toInt();
      if (i == 2) value3 = String(value);
      if (i == 3) value4 = String(value);
    }

    // Serial.print('value1:'+ value1+ 'value2:'+ value2 + 'value3:'+ value3);

    switch(value1){
      case 0:
          selectMovement(value2, hexToRGB_P1(value3), hexToRGB_P2(value4));
          // pixels1.clear();
          break;
      case 1: //set headrest
          switchOffLED(pixels2);
          colorWipe(pixels1, hexToRGB_P1(value3), 0, LED_BRIGHTNESS);
          setHeadrest(value2);
          switchOffLED(pixels1);
          break;
      case 2: //setfootrest
          switchOffLED(pixels1);
          colorWipe(pixels2, hexToRGB_P2(value4), 0, LED_BRIGHTNESS);
          setFootrest(value2);
          switchOffLED(pixels2);
          break;
    }
  }


}
