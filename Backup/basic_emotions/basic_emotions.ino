#include <ArduinoJson.h>
#include "rgb_lcd.h"

rgb_lcd lcd;

enum Emotion {NEUTRAL, HAPPY, ANGRY, SAD};
Emotion emotion = NEUTRAL;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
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
      Serial.print("Received dynamic: ");
      Serial.println(dynamic_value);

      lcd.begin(16, 2);  // Initialize the LCD with 16 columns and 2 rows
      lcd.setRGB(255, 0, 0);  // Set the backlight color (red in this case)
      lcd.setCursor(0, 0);  // Set the cursor to the top-left corner
      lcd.print(static_value);  // Print the first line
      lcd.setCursor(0, 1);  // Set the cursor to the second line
      lcd.print(dynamic_value);

      if (strcmp(static_value, "HAPPY") == 0) {
        emotion = HAPPY;
        lcd.setCursor(0, 1);
        lcd.print(emotion);
      }
       else if (strcmp(static_value, "ANGRY") == 0) {
        emotion = ANGRY;
        lcd.setColorWhite();
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
}
