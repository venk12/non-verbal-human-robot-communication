import serial
import random
import time

ser = serial.Serial('COM3', 115200)
data =  str(0) + "," + str(2) +"," 

def receiveData():
    print("Receiving data from Arduino...")
    # Receive data from the Arduino. The Arduino sends back what it received.
    read = ""
    while ser.in_waiting > 0:
        incomingData = ser.read().decode()  # Read one byte and decode it as a string
        if incomingData != '\n':
            read += incomingData
    
    if len(read) > 0:
        print("Arduino data on serial port: ", read)


def execute_wait():
    data =  str(0) + "," + str(2) +"," 
    for i in range(3):
        print("sending data :", data.encode())
        ser.write(data.encode())
        time.sleep(1)


def select_headrest():
    up =  str(1) + "," + str(130) +"," 
    down =  str(1) + "," + str(70) +"," 

    for i in range(3):
            print("sending data :", up.encode())
            ser.write(up.encode())
            time.sleep(2)
            print("sending data :", down.encode())
            ser.write(down.encode())
            time.sleep(2)

def select_footrest():
    up =  str(2) + "," + str(130) +"," + '(0,255,255),'
    down =  str(2) + "," + str(70) +"," + 'green,'

    for i in range(3):
            print("sending data :", up.encode())
            ser.write(up.encode())
            time.sleep(2)
            print("sending data :", down.encode())
            ser.write(down.encode())
            time.sleep(2)


def execute_selection():
    for i in range(3):
        data =  str(0) + "," + str(3) +"," 
        print("sending data :", data.encode())
        ser.write(data.encode())
        time.sleep(1)
    for i in range(3):
        data =  str(0) + "," + str(4) +"," 
        print("sending data :", data.encode())
        ser.write(data.encode())
        time.sleep(1)

    execute_wait()



while True:
    select_footrest()
    # print("sending data :", data.encode())
    # ser.write(data.encode())
    # receiveData()

