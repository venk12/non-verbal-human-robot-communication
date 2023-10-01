#include <ArduinoJson.h>
#include "rgb_lcd.h"
#include <Adafruit_NeoPixel.h>

#define LED_PIN       4
#define NUMPIXELS    74

Adafruit_NeoPixel pixels(NUMPIXELS, LED_PIN);
int LED_BRIGHTNESS = 8;  // 0-255

long timer1;
enum Emotion {NEUTRAL, HAPPY, ANGRY, SAD};
Emotion emotion = NEUTRAL;

rgb_lcd lcd;

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

byte angry[] = {
  B0000,
  B10000,
  B110000,
  B1111000,
  B111110,
  B11111,
  B1111
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

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  // Initialize the leds
  pixels.begin();

  // lcd.blink();
  lcd.setColorWhite();
}

void loop() {
  // put your main code here, to run repeatedly:

  DynamicJsonDocument jsonData(1024);

  while(Serial.available()){
    // Read the incoming JSON data
    DeserializationError error = deserializeJson(jsonData, Serial);

    if (error) {
      Serial.print("Error parsing JSON: ");
      Serial.println(error.c_str());
    }

    else {
      // Successfully parsed JSON, now you can access its elements
      const char* static_value = jsonData["static"];

      
      int dynamic_value = jsonData["dynamic"];

      Serial.print("Received static: ");
      Serial.println(static_value);

      lcd.begin(16, 2);  // Initialize the LCD with 16 columns and 2 rows
      lcd.setRGB(255, 0, 0);  // Set the backlight color (red in this case)
      lcd.setCursor(0, 0);  // Set the cursor to the top-left corner
      lcd.print(static_value);  // Print the first line

       if (strcmp(static_value, "HAPPY") == 0) {
        emotion = HAPPY;
        lcd.setCursor(0, 1);
        lcd.print(emotion);
      }
       else if (strcmp(static_value, "ANGRY") == 0) {
        emotion = ANGRY;
        lcd.setCursor(0, 1);
        lcd.print(emotion);  
      } 
      else if (strcmp(static_value, "SAD") == 0) {
        emotion = SAD;
        lcd.setCursor(0, 1);
        lcd.print(emotion);
      } 
      else if(strcmp(static_value, "NEUTRAL") == 0) {
        emotion = NEUTRAL; 
        lcd.setCursor(0, 1);
        lcd.print(emotion);
      }
      else {
        emotion = NEUTRAL; 
        lcd.setCursor(0, 1);
        lcd.print(emotion);
      }

    }
  }

    // Ever 20 milliseconds, update the servos
    if (millis() - timer1 >= 200){
      timer1 = millis();
      run_emotions();
    }
}

void run_emotions(){
  pixels.clear();  

  switch (emotion) {
    case NEUTRAL:
      display_eyes(neutral, 125);
      break;

    case HAPPY:
      display_eyes(happy, 80);
      break;

    case SAD:
      display_eyes(sad, 80);
      break;

    case ANGRY:
      display_eyes(angry,100);
      break;
  }

  pixels.show();
}

void display_eyes(byte arr[], int hue){
   display_eye(arr, hue, true);
   display_eye(arr, hue, false);
}

void display_eye(byte arr[], int hue, bool left) {
  // We will draw a circle on the display
  // It is a hexagonal matrix, which means we have to do some math to know where each pixel is on the screen

  int rows[] = {4, 5, 6, 7, 6, 5, 4};      // The matrix has 4, 5, 6, 7, 6, 5, 4 rows.
  int NUM_COLUMNS = 7;                     // There are 7 columns
  int index = (left) ? 0 : 37;             // If we draw the left eye, we have to add an offset of 37 (4+5+6+7+6+5+4)
  for (int i = 0; i < NUM_COLUMNS; i++) {
    for (int j = 0; j < rows[i]; j++) {
      int brightness = LED_BRIGHTNESS * bitRead(arr[i], (left) ? rows[i] - 1 - j : j);
      pixels.setPixelColor(index, pixels.ColorHSV(hue * 256, 255, brightness));
      index ++;
    }
  }
}
