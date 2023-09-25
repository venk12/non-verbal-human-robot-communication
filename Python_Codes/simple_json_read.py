import time
import serial
import json

arduinoData = serial.Serial('com3',115200)
time.sleep(1)

while True:
    while(arduinoData.inWaiting()==0):
        pass
    dataPacket = arduinoData.readline()
    dataPacket = dataPacket.decode('utf-8').strip('\r\n')
    json_object = json.loads(dataPacket)
    print(json_object['dynamic'])
