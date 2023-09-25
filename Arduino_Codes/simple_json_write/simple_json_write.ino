#include <ArduinoJson.h>

const int button = 3;


void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  pinMode(button, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  int value = digitalRead(button);
  DynamicJsonDocument root(1024);

  root["static"] ="Monday";
  root["dynamic"] = value;

  serializeJson(root, Serial);
  Serial.println();
  
  delay(100);

}
