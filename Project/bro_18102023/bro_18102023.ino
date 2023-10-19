#include <Adafruit_NeoPixel.h>
#include <SoftwareSerial.h>
#include <MP3Player_KT403A.h>
#include "HUSKYLENS.h"
#include <Servo.h>

// NeoPixel configuration
#define LED_PIN_1 4
#define LED_COUNT_1 37
#define LED_PIN_2 5
#define LED_COUNT_2 37

// Touch sensor pin
#define TOUCH_PIN A0

// Servo pins
#define SERVO_PIN_1 8
#define SERVO_PIN_2 7

// NeoPixel instances
Adafruit_NeoPixel pixels1(LED_COUNT_1, LED_PIN_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels2(LED_COUNT_2, LED_PIN_2, NEO_GRB + NEO_KHZ800);

// LED brightness
const int LED_BRIGHTNESS = 10; // 0-255

// Touch sensor
bool prev_touch_value = false;

// Emotion and color enums
enum Emotion { NEUTRAL, HAPPY, SAD, CONFIRMATION };
Emotion emotion = NEUTRAL;
enum Color { RED, GREEN, BLUE, ORANGE };
Color color = BLUE;

// Servo instances
Servo S_headrest, S_footrest;
int S_headrest_angle = 90;
int S_footrest_angle = 90;

// Timers
long timer1, timer2, timer3;

// PC connection flag
bool pc_connected = false;

// Voice switch flag
bool voice_switch = false;

// LED patterns
byte neutralPattern[] = {B0000, B01110, B011110, B0111110, B011110, B01110, B0000};
byte happyPattern[] = {B1111, B11111, B111111, B1100011, B000000, B00000, B0000};
byte sadPattern[] = {B0000, B00001, B000011, B0001111, B011111, B11111, B1111};
byte confirmationPattern[] = {B1111, B11111, B111111, B1111111, B111111, B11111, B1111};

// First activation flag
bool first_activation = false;

void setup() {
  pinMode(TOUCH_PIN, INPUT);

  // Initialize NeoPixels
  pixels1.begin();
  pixels1.show();
  pixels2.begin();
  pixels2.show();

  // Serial communication
  Serial.begin(115200);

  // Attach servos
  S_headrest.attach(SERVO_PIN_1);
  S_footrest.attach(SERVO_PIN_2);
}

void loop() {
  bool touch_value = digitalRead(TOUCH_PIN);

  if (touch_value && voice_switch) {
    voice_switch = false;
    selectMovement(1, pixels1.Color(0, 0, 0), pixels2.Color(0, 0, 0));
  } else if (touch_value && !voice_switch) {
    voice_switch = true;
    selectMovement(1, pixels1.Color(255, 255, 255), pixels2.Color(255, 255, 255));
  }

  if (voice_switch) {
    if (millis() - timer2 >= 10 && voice_switch) {
      timer2 = millis();
      if (!first_activation) {
        Serial.println("voice switch is on");
        first_activation = true;
      }
      communication();
    }
  }

  if (!voice_switch && first_activation) {
    Serial.println("voice switch is off");
    first_activation = false;
    voice_switch = false;
  }
}

void colorWipe(Adafruit_NeoPixel &strip, uint32_t color, int wait, int brightness) {
  for (int i = 0; i < strip.numPixels(); i++) {
    uint8_t r = (color >> 16) & 0xFF;
    uint8_t g = (color >> 8) & 0xFF;
    uint8_t b = color & 0xFF;

    r = (r * brightness) / 255;
    g = (g * brightness) / 255;
    b = (b * brightness) / 255;

    strip.setPixelColor(i, strip.Color(r, g, b));
    strip.show();
  }
}

void switchOffLED(Adafruit_NeoPixel &strip) {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));
    strip.show();
  }
}

void moveServo(int position, int duration, double frequency, bool mirror, Servo serv) {
  int startPos = position + 20;
  int endPos = position - 20;
  float stepSize = (2 * PI) / (duration / 2);
  for (float t = 0; t <= PI; t += stepSize) {
    int pos = startPos + ((endPos - startPos) / 2) * (1 + sin(t));
    if (mirror == true) {
      S_footrest.write(pos);
    }
    serv.write(pos);
    delay(15);
  }
}

void setHeadrest(int endPos) {
  int increment = 1;
  int delayTime = 15;
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

void setFootrest(int endPos) {
  int increment = 1;
  int delayTime = 15;
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
  if (hexColorString.startsWith("0x")) {
    hexColorString = hexColorString.substring(2);
  }
  unsigned long hexColor = strtoul(hexColorString.c_str(), NULL, 16);
  int red = (hexColor >> 16) & 0xFF;
  int green = (hexColor >> 8) & 0xFF;
  int blue = hexColor & 0xFF;
  return pixels2.Color(red, green, blue);
}

uint32_t hexToRGB_P1(String hexColorString) {
  if (hexColorString.startsWith("0x")) {
    hexColorString = hexColorString.substring(2);
  }
  unsigned long hexColor = strtoul(hexColorString.c_str(), NULL, 16);
  int red = (hexColor >> 16) & 0xFF;
  int green = (hexColor >> 8) & 0xFF;
  int blue = hexColor & 0xFF;
  return pixels1.Color(red, green, blue);
}

void selectMovement(int i, uint32_t headrestpixel, uint32_t footrestpixel) {
  switch (i) {
    case 0:
      colorWipe(pixels1, headrestpixel, 0, LED_BRIGHTNESS);
      colorWipe(pixels2, footrestpixel, 0, LED_BRIGHTNESS);
      break;
    case 1:
      colorWipe(pixels1, headrestpixel, 0, LED_BRIGHTNESS);
      colorWipe(pixels2, footrestpixel, 0, LED_BRIGHTNESS);
      moveServo(90, 200, 0.5, true, S_headrest);
      break;
    case 2:
      S_headrest.detach();
      S_footrest.detach();
      colorWipe(pixels1, headrestpixel, 0, LED_BRIGHTNESS);
      colorWipe(pixels2, footrestpixel, 0, LED_BRIGHTNESS);
      delay(150);
      switchOffLED(pixels1);
      switchOffLED(pixels2);
      delay(150);
      S_headrest.attach(SERVO_PIN_1);
      S_footrest.attach(SERVO_PIN_2);
      break;
    case 3:
      colorWipe(pixels1, headrestpixel, 0, LED_BRIGHTNESS);
      moveServo(S_headrest_angle, 200, 1, false, S_headrest);
      switchOffLED(pixels1);
      break;
    case 4:
      colorWipe(pixels2, footrestpixel, 0, LED_BRIGHTNESS);
      moveServo(S_footrest_angle, 200, 1, false, S_footrest);
      switchOffLED(pixels2);
      break;
    default:
      Serial.println("Unknown switch state");
      break;
  }
}

void communication() {
  char val = ' ';
  String data = "";
  if (Serial.available()) {
    do {
      val = Serial.read();
      if (val != -1) data = data + val;
    } while (val != -1);
  }

  if (data.length() > 1 && data.charAt(data.length() - 1) == ',') {
    pc_connected = true;

    int value1, value2;
    String value3, value4;
    String value;
    for (int i = 0; data.length() > 0; i++) {
      value = data.substring(0, data.indexOf(','));
      data = data.substring(data.indexOf(',') + 1, data.length());

      if (i == 0) value1 = value.toInt();
      if (i == 1) value2 = value.toInt();
      if (i == 2) value3 = String(value);
      if (i == 3) value4 = String(value);
    }

    switch (value1) {
      case 0:
        selectMovement(value2, hexToRGB_P1(value3), hexToRGB_P2(value4));
        break;
      case 1:
        switchOffLED(pixels2);
        colorWipe(pixels1, hexToRGB_P1(value3), 0, LED_BRIGHTNESS);
        setHeadrest(value2);
        switchOffLED(pixels1);
        break;
      case 2:
        switchOffLED(pixels1);
        colorWipe(pixels2, hexToRGB_P2(value4), 0, LED_BRIGHTNESS);
        setFootrest(value2);
        switchOffLED(pixels2);
        break;
    }
  }
}