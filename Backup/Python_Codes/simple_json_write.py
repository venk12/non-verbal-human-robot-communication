import serial
import json
import time

arduinoData = serial.Serial('com3', 115200)

dynamic_data = 1

while True:
    # Create a JSON object
    data = {
        "static": "Hello from BRO",
        "dynamic": dynamic_data,
        # "eye_emotion":'happy'
    }
    
    print("Now sending this data to arduino:", str(data))

    json_string = json.dumps(data)

    arduinoData.write(json_string.encode('utf-8'))
    # arduinoData.close()

    time.sleep(1)
    dynamic_data+=1

# arduinoData.close()