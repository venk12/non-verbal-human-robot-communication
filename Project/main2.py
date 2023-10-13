import serial
import random
import time
import pygame

import speech_recog as listen
import detect_intent as detect

# Initialize pygame
pygame.init()
pygame.mixer.init()

ser = serial.Serial('COM3', 115200)
# data =  str(0) + "," + str(2) +"," 

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
    for i in range(2):
        data =  str(0) + "," + str(3) +","+  "0xFFFF00," +"0xFFFF00,"
        print("sending data :", data.encode())
        ser.write(data.encode())
        time.sleep(0.75)
    for i in range(2):
        data =  str(0) + "," + str(4) +","  + "0xFFFF00," +"0xFFFF00,"
        print("sending data :", data.encode())
        ser.write(data.encode())
        time.sleep(0.75)

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

robot_state = {
     'headrest_angle': 90,
     'footrest_angle': 90,
     'status': ""
}

def receiveData():
    # Receive data from the Arduino. The Arduino sends back what it received.
    read = ""
    while ser.in_waiting > 0:
        incomingData = ser.read().decode()  # Read one byte and decode it as a string
        if incomingData != '\n':
            read += incomingData
    
    if len(read) > 0:
        print(read)
        return read

voice_switch = False

i = 1

while True:
    recv_message = receiveData()

    if (recv_message == "voice switch is on"):
        voice_switch = True
        robot_state['status'] = "on_waiting"
        recv_message = ""

    if (voice_switch == True and robot_state['status'] == "on_waiting"):
        print("Now listening to you speak....")
        content = listen.main()
        print("Detecting intent for text: ", str(content[-1]))
        obj_dialogflow = detect.detect_intent_texts([str(content[-1])])
        detected_intent  = obj_dialogflow['intent']
        print("Detected intent: ", detected_intent)

        if(detected_intent == 'Move the bed'):
            print("Now switch the bed state to 'selection'...")
            robot_state['status'] = 'selection'
            content = ""
            detected_intent = ""
            # pass

    if (voice_switch == True and robot_state['status'] == 'selection'):
        while True:
            print("Now executing 'selection' command...")
            execute_selection()
            print("Now listening to you speak....")
            start_time = time.time()
            content = listen.main()
            obj_dialogflow = detect.detect_intent_texts([str(content[-1])])
            detected_intent  = obj_dialogflow['intent']
            detected_location = obj_dialogflow['location']
            detected_direction = obj_dialogflow['direction']

            if len(detected_direction) > 0:
                parsed_direction = detected_direction[0]
            else:
                parsed_direction = ""

            detected_degree = obj_dialogflow['degree']

            if(detected_intent == ""):
                print("No intent detected...looping again")
                continue

            if(detected_intent == "Move the bed"):
                if(detected_location == 'headrest'):
                    print("Moving the headrest now")
                    select_headrest()

                if(detected_location == 'footrest'):
                    print("Moving the footrest now")
                    select_footrest()
                
                break
                # try:
                #     obj_dialogflow = detect.detect_intent_texts([str(content[-1])])
                #     detected_intent  = obj_dialogflow['intent']
                #     bed_part = obj_dialogflow['bed_part']
                #     bed_degree = obj_dialogflow['bed_degree']
                    
                #     if(bed_part==""):
                #         continue

                # except ValueError:
                #     print("Invalid input. Please enter a valid number.")

                # if(bed_part == 'headrest'):
                #     robot_state['status'] = 'selection_headrest'
                
                # if(bed_part == 'footrest'):
                #     robot_state['status'] = 'selection_footrest'

    # 
    # execute_selection()
# # time.sleep(1.5) 
# # setColors()
# time.sleep(5)
    # select_headrest()
    # time.sleep(5)
# select_footrest()
# time.sleep(5)
# set_headrest(90)
# set_footrest(30)



