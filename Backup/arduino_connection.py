import serial
import json
import time

# Code to loop 
    # while True:
    #     data = {"static": "Whatever"}  
    #     send_data(arduinoData, data)      
    #     time.sleep(0.5)

def establish_arduino_connection(port, baud_rate):
        arduinoSerial = serial.Serial(port, baud_rate)
        data = "84,90,HAPPY"
        send_data(arduinoSerial, data)

        return arduinoSerial

def send_data(serial_details, data):
    print("Now sending this data to arduino:", str(data))
    json_string = json.dumps(data)
    serial_details.write(json_string.encode('utf-8'))
