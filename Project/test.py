import serial
import random
import time
import pygame

import speech_recog as listen
import detect_intent as detect

import threading

# Initialize pygame
pygame.init()
pygame.mixer.init()

ser = serial.Serial('COM3', 115200)

def map_intent_to_sound(intent):
    if intent == 'wake_up':
        return 'wake_up.mp3'
    if intent == 'confirm':
        return 'confirm_apprehensive.wav'
    if intent == 'headrest':
        return 'headrest.mp3'
    if intent == 'footrest':
        return 'footrest.mp3'
    if intent == 'move_up':
        return 'click_on.ogg'
    if intent == 'move_down':
        return 'click_off.ogg'
    if intent == 'sleep':
        return 'sleep.mp3'
    if intent == 'turn_off':
        return 'turn_off.wav'
    if intent == 'wait':
        return 'wait_click.wav'

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


# first color hex is for headrest
# second color hex is for footrest
def execute_wait():  # waiting after giving the headrest footrest selectionj
    data = str(0) + "," + str(2) + "," + "0xFFFFFF," + "0xFFFFFF,"
    for i in range(3):
        print("sending data :", data.encode())

        audio_file = './new_audio_files/'+ map_intent_to_sound('wait')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        ser.write(data.encode())
        time.sleep(0.75)


# first color hex is for headrest
# second color hex is for footrest
def select_headrest():  # selecting the headrest, degree1, color1, color2
    up = str(1) + "," + str(120) + "," + '0x0F22B8,' + '0x0F22B8,'  # first is green,
    down = str(1) + "," + str(80) + "," + '0xA115A3,' + '0xA115A3,'  # first is red

    for i in range(2):
        print("sending data :", up.encode())

        audio_file = './new_audio_files/'+ map_intent_to_sound('move_up')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()


        ser.write(up.encode())
        time.sleep(0.5)
        print("sending data :", down.encode())

        audio_file = './new_audio_files/'+ map_intent_to_sound('move_down')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        ser.write(down.encode())
        time.sleep(1)

        execute_wait()


# first color hex is for headrest
# second color hex is for footrest
def select_footrest():  # selecting the footrest, degree1, color1, color2
    up = str(2) + "," + str(120) + "," + '0x0F22B8,' + '0x0F22B8,'
    down = str(2) + "," + str(80) + "," + '0xA115A3,' + '0xA115A3,'

    for i in range(2):
        print("sending data :", up.encode())

        audio_file = './new_audio_files/'+ map_intent_to_sound('move_up')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        ser.write(up.encode())
        time.sleep(0.5)
        print("sending data :", down.encode())

        audio_file = './new_audio_files/'+ map_intent_to_sound('move_down')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        ser.write(down.encode())
        time.sleep(1)

        execute_wait()


# def setColors():
#     data = str(0) + "," + str(0) + "," + "0xFFFFFF," + "0xFFFFFF,"
#     print("sending data :", data.encode())
#     ser.write(data.encode())


# first color hex is for headrest
# second color hex is for footrest
def execute_selection():  # smaking the selection of headrest and footrest, color1, color2
    for i in range(2):
        data = str(0) + "," + str(3) + "," + "0xFFBF00," + "0xFFBF00,"
        print("sending data :", data.encode())

        audio_file = './new_audio_files/'+ map_intent_to_sound('move_up')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        ser.write(data.encode())
        time.sleep(0.75)

    for i in range(2):
        data = str(0) + "," + str(4) + "," + "0xFFBF00," + "0xFFBF00,"
        print("sending data :", data.encode())

        audio_file = './new_audio_files/'+ map_intent_to_sound('move_down')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        ser.write(data.encode())
        time.sleep(0.75)

    execute_wait()

def confirmation():
    
    audio_file = './new_audio_files/'+ map_intent_to_sound('confirm')
    pygame.mixer.music.load(audio_file)

    data = str(0) + "," + str(2) + "," + "0x0DAC16," + "0x0DAC16,"
    for i in range(2):
        print("sending data :", data.encode())
        
        pygame.mixer.music.play()   
        ser.write(data.encode())
        time.sleep(1)
        
    # time.sleep(2)

# first color hex is for headrest
# second color hex is for footrest
def set_footrest(i):  # selecting the footrest, degree1, color1, color2
    data = str(2) + "," + str(i) + "," + '0xFF0000,' + '0x00FF00,'
    print("sending data :", data.encode())
    ser.write(data.encode())
    # execute_wait()
    # time.sleep(2)


# first color hex is for headrest
# second color hex is for footrest
def set_headrest(i):  # selecting the footrest, degree1, color1, color2
    data = str(1) + "," + str(i) + "," + '0xFF0000,' + '0x00FF00,'
    print("sending data :", data.encode())
    ser.write(data.encode())
    execute_wait()
    # time.sleep(2)


def turn_off():
    data = str(0) + "," + str(2) + "," + "0xFFFFFF," + "0xFFFFFF,"
    
    audio_file = './new_audio_files/'+ map_intent_to_sound('turn_off')
    pygame.mixer.music.load(audio_file)

    for i in range(2):
        print("sending data :", data.encode())
        ser.write(data.encode())
        time.sleep(0.75)

    pygame.mixer.music.play()

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
    # turn_off()
    # time.sleep(2)

    # execute_selection()
    # time.sleep(2)

    # select_headrest()
    # time.sleep(2)

    # select_footrest()
    # time.sleep(2)

    # confirmation()
    # time.sleep(2)

    # turn_off()
    # time.sleep(2)
    recv_message = receiveData()

    if (recv_message == "voice switch is on"):
        voice_switch = True

        robot_state['status'] = "on_waiting"
        recv_message = ""
        print(voice_switch,robot_state)

    if (voice_switch == True and robot_state['status'] == "on_waiting"):
        print("Now listening to you speak....")
        content = listen.main()
        print("Detecting intent for text: ", str(content[-1]))
        obj_dialogflow = detect.detect_intent_texts([str(content[-1])])
        detected_intent = obj_dialogflow['intent']
        if ("Move the bed" in detected_intent):
            detected_location = obj_dialogflow['location']
            detected_direction = obj_dialogflow['direction']
            detected_degree = obj_dialogflow['degree']
            print("Now switch the bed state to 'selection'...")
            robot_state['status'] = 'selection'

            if (len(detected_location)!=0):
                print("Now switch the bed state to 'upordown'...")
                robot_state['status'] = 'upordown'

    while (voice_switch == True and robot_state['status'] == 'selection'):
        print("Now executing 'selection' command...")
        execute_selection()
        print("Now listening to you speak....")
        content = listen.main()
        obj_dialogflow = detect.detect_intent_texts([str(content[-1])])
        detected_intent = obj_dialogflow['intent']
        if ("Move the bed" not in detected_intent):
            print("No intent detected...looping again")
            continue
        else:
            detected_location = obj_dialogflow['location']
            detected_direction = obj_dialogflow['direction']
            if (len(detected_location) != 0):
                print("Now switch the bed state to 'upordown'...")
                robot_state['status'] = 'upordown'

    while (voice_switch == True and robot_state['status'] == 'upordown'):
        if (detected_location == 'headrest'):
            while( len(detected_direction) ==0):
                print("head UP or Down?")
                select_headrest()
                execute_wait()
                content = listen.main()
                obj_dialogflow = detect.detect_intent_texts([str(content[-1])])
                detected_intent = obj_dialogflow['intent']
                if ("Move the bed" not in detected_intent):
                    print("No intent detected...looping again")
                    continue
                detected_direction = obj_dialogflow['direction']

            else:
                if ('up' in detected_direction):
                    if (detected_degree != ""):
                        robot_state['headrest_angle']=robot_state['headrest_angle']+int(detected_degree)
                        set_headrest(robot_state['headrest_angle'])
                    else:
                        robot_state['headrest_angle'] = robot_state['headrest_angle']+15
                        set_headrest(robot_state['headrest_angle'])
                    print('move the headrest up now')
                    confirmation()

                if ('down' in detected_direction):
                    if (detected_degree!=""):
                        robot_state['headrest_angle'] = robot_state['headrest_angle'] - int(detected_degree)
                        set_headrest(robot_state['headrest_angle'])
                    else:
                        robot_state['headrest_angle'] = robot_state['headrest_angle']-15
                        set_headrest(robot_state['headrest_angle'])
                    print('move the headrest down now')
                    confirmation()


        if (detected_location == 'footrest'):
            while (len(detected_direction) == 0):
                print("foot UP or Down?")
                select_footrest()
                execute_wait()
                content = listen.main()
                obj_dialogflow = detect.detect_intent_texts([str(content[-1])])
                detected_intent = obj_dialogflow['intent']
                if ("Move the bed" not in detected_intent):
                    print("No intent detected...looping again")
                    continue
                detected_direction = obj_dialogflow['direction']

            else:
                if ('up' in detected_direction):
                    if (detected_degree != ""):
                        robot_state['footrest_angle']=robot_state['footrest_angle']+ int(detected_degree)
                        set_footrest(robot_state['footrest_angle'] )
                    else:
                        robot_state['footrest_angle'] =robot_state['footrest_angle']+15
                        set_footrest(robot_state['footrest_angle'])
                    print('move the footrest up now')
                    confirmation()

                if ('down' in detected_direction):
                    if (detected_degree != ""):
                        robot_state['footrest_angle'] = robot_state['footrest_angle'] - int(detected_degree)
                        set_footrest(robot_state['footrest_angle'] )
                    else:
                        robot_state['footrest_angle'] =robot_state['footrest_angle']-15
                        set_footrest(robot_state['footrest_angle'])
                    print('move the footrest down now')
                    confirmation()

    #     robot_state['status'] = "on_waiting"
    #     break