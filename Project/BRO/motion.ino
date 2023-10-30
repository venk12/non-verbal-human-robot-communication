#include <Servo.h> 

#define SERVO_PIN_1   6
#define SERVO_PIN_2   7

Void setup(){
    servo1.attach(SERVO_PIN_1);
    servo2.attach(SERVO_PIN_2);
    servo1.write(90);
    servo2.write(90);
}

Void loop(){
    servo1.write(90);
    millis(200);
    servo1.write(80);
    millis(200);
}
