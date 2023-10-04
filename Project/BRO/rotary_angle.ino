const int analogPin = A0;  // Define the analog pin for the rotary angle sensor
const int minSensorValue = 0;  // Minimum sensor value
const int maxSensorValue = 1023;  // Maximum sensor value
const int minAngle = 0;  // Minimum angle (in degrees)
const int maxAngle = 360;  // Maximum angle (in degrees)

void setup() {
  Serial.begin(9600);  // Initialize serial communication at 9600 baud
}

void loop() {
  // Read the analog value from the rotary angle sensor
  int sensorValue = analogRead(analogPin);

  // Map the sensor value to an angle between minAngle and maxAngle
  int angle = map(sensorValue, minSensorValue, maxSensorValue, minAngle, maxAngle);

  // Print the angle to the serial monitor
  Serial.print("Angle: ");
  Serial.print(angle);
  Serial.println(" degrees");

  delay(1000);  // Delay for 1 second (adjust as needed)
}
