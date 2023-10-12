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

#first color hex is for headrest
#second color hex is for footrest
def execute_wait():  #waiting after giving the headrest footrest selectionj
    data =  str(0) + "," + str(2) +"," + "0xFFFFFF," +"0xFFFFFF,"
    for i in range(3):
        print("sending data :", data.encode())
        ser.write(data.encode())
        time.sleep(1)

#first color hex is for headrest
#second color hex is for footrest
def select_headrest(): #selecting the headrest, degree1, color1, color2
    up =  str(1) + "," + str(130) +"," + '0x00FF00,'+'0xFFBF00,' #first is green, 
    down =  str(1) + "," + str(70) +"," + '0xFF0000,'+'0x00FF00,' #first is red

    for i in range(3):
            print("sending data :", up.encode())
            ser.write(up.encode())
            time.sleep(2)
            print("sending data :", down.encode())
            ser.write(down.encode())
            time.sleep(2)

#first color hex is for headrest
#second color hex is for footrest
def select_footrest():#selecting the footrest, degree1, color1, color2
    up =  str(2) + "," + str(130) +"," + '0xFFBF00,'+'0x00FF00,'
    down =  str(2) + "," + str(70) +"," + '0x00FF00,'+'0xFF0000,'

    for i in range(3):
            print("sending data :", up.encode())
            ser.write(up.encode())
            time.sleep(2)
            print("sending data :", down.encode())
            ser.write(down.encode())
            time.sleep(2)

def setColors():
     data =  str(0) + "," + str(0) +"," + "0xFFFFFF," +"0xFFFFFF,"
     print("sending data :", data.encode())
     ser.write(data.encode())


#first color hex is for headrest
#second color hex is for footrest
def execute_selection(): #smaking the selection of headrest and footrest, color1, color2
    for i in range(3):
        data =  str(0) + "," + str(3) +","+  "0x0000FF," +"0x0000FF,"
        print("sending data :", data.encode())
        ser.write(data.encode())
        time.sleep(1)
    for i in range(3):
        data =  str(0) + "," + str(4) +","  + "0x0000FF," +"0x0000FF,"
        print("sending data :", data.encode())
        ser.write(data.encode())
        time.sleep(1)

    execute_wait()

#first color hex is for headrest
#second color hex is for footrest
def set_footrest(i):#selecting the footrest, degree1, color1, color2
    data =  str(2) + "," + str(i) +"," + '0xFFBF00,'+'0x00FF00,'
    print("sending data :", data.encode())
    ser.write(data.encode())
    time.sleep(2)

#first color hex is for headrest
#second color hex is for footrest
def set_headrest(i):#selecting the footrest, degree1, color1, color2
    data =  str(1) + "," + str(i) +"," + '0xFFBF00,'+'0x00FF00,'
    print("sending data :", data.encode())
    ser.write(data.encode())
    time.sleep(2)





time.sleep(5) 
execute_selection()
# time.sleep(1.5) 
# setColors()
time.sleep(5)
select_headrest()
time.sleep(5)
select_footrest()
time.sleep(5)
set_headrest(150)
set_footrest(30)

