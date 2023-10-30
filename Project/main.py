import serial
import time
import pygame

import speech_recog as listen
import detect_intent as detect

import threading

# Initialize pygame
pygame.init()
pygame.mixer.init()

ser = serial.Serial('COM8', 115200)

import re

substring_mapping = {
        "address": "headrest",
        "head dress": "headrest",
        "head rest": "headrest",
        "aheadrest": "headrest",
        "hat rest": "footrest",
        "food rest": "footrest",
        "foot rest": "footrest",
        "hatch rest": "headrest",
        "had to rest": "headrest",
        "food restaurant": "footrest",
        "remove": "move",
        "higher": "up",
        "increase": "up",
        "lower": "down",
        "decrease": "down",
        
        "foodrestaurant":"footrest"
        # Add more mappings as needed
    }


# Use regular expressions to find and replace substrings
pattern = re.compile("|".join(re.escape(key) for key in substring_mapping.keys()))

# Function to replace substrings using regular expressions
def replace_substrings(match):
    # Get the matched substring
    matched_substring = match.group(0)

    # Define your mapping object as a dictionary where keys are substrings to find, and values are their replacements.

    # Look up the matched substring in the mapping, or keep it as is
    replacement = substring_mapping.get(matched_substring, matched_substring)

    return replacement

def map_intent_to_sound(intent):
    if intent == 'confirm':
        return 'confirm_apprehensive.wav'
    if intent == 'move_up':
        return 'move-up.mp3'
    if intent == 'move_down':
        return 'move-down.mp3'
    if intent == 'up_down':
        return 'up_down.mp3'
    if intent == 'headrest':
        return 'click_on.ogg'
    if intent == 'footrest':
        return 'click_off.ogg'
    if intent == 'sleep':
        return 'snore.mp3'
    if intent == 'turn_off':
        return 'bye.mp3'
    if intent == 'wait':
        return 'wait.mp3'
    if intent == 'confuse':
        return 'question.mp3'
    if intent == 'ok':
        return 'yeah.mp3'
    if intent == 'hello':
        return 'hello.mp3'



# first color hex is for headrest
# second color hex is for footrest
def execute_wait():  # waiting after giving the headrest footrest selection
    data = str(0) + "," + str(2) + "," + "0xFFBF00," + "0xFFBF00," #Yellow

    for i in range(3):
        print("sending data :", data.encode())

        audio_file = './new_audio_files/' + map_intent_to_sound('wait')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        ser.write(data.encode())
        time.sleep(0.75)


# first color hex is for headrest
# second color hex is for footrest
def select_headrest(headrest_angle):  # selecting the headrest, degree1, color1, color2
    up = str(1) + "," + str(headrest_angle+10) + "," + '0x0000ff,' + '0x0000ff,'  # up is blue,
    down = str(1) + "," + str(headrest_angle-10) + "," + '0xffff00,' + '0xffff00,'  # down is yellow

    for i in range(2):
        audio_file = './new_audio_files/' + map_intent_to_sound('up_down')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        print("sending data :", up.encode())
        ser.write(up.encode())
        time.sleep(1)
        print("sending data :", down.encode())
        ser.write(down.encode())
        time.sleep(1)

        #execute_wait()


# first color hex is for headrest
# second color hex is for footrest
def select_footrest(footrest_angle):  # selecting the footrest, degree1, color1, color2
    up = str(2) + "," + str(footrest_angle+10) + "," + '0x0000ff,' + '0x0000ff,'# up is blue,
    down = str(2) + "," + str(footrest_angle-10) + "," + '0xffff00,' + '0xffff00,'# down is yellow

    for i in range(2):
        audio_file = './new_audio_files/' + map_intent_to_sound('up_down')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        print("sending data :", up.encode())
        ser.write(up.encode())
        time.sleep(1)
        print("sending data :", down.encode())
        ser.write(down.encode())
        time.sleep(1)

        #execute_wait()


# def setColors():
#     data = str(0) + "," + str(0) + "," + "0xFFFFFF," + "0xFFFFFF,"
#     print("sending data :", data.encode())
#     ser.write(data.encode())


# first color hex is for headrest
# second color hex is for footrest
def execute_selection():  # smaking the selection of headrest and footrest, color1, color2
    for i in range(2):
        data = str(0) + "," + str(3) + "," + "0x00ffff," + "0x00ffff," #headrest blue
        print("sending data :", data.encode())

        audio_file = './new_audio_files/' + map_intent_to_sound('headrest')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        ser.write(data.encode())
        time.sleep(0.75)

    for i in range(2):
        data = str(0) + "," + str(4) + "," + "0x00ffff," + "0x00ffff," #footrest blue
        print("sending data :", data.encode())

        audio_file = './new_audio_files/' + map_intent_to_sound('footrest')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        ser.write(data.encode())
        time.sleep(0.75)

    execute_wait()


def confirmation():
    audio_file = './new_audio_files/' + map_intent_to_sound('confirm')
    pygame.mixer.music.load(audio_file)

    data = str(0) + "," + str(2) + "," + "0x0DAC16," + "0x0DAC16," #green
    for i in range(2):
        print("sending data :", data.encode())

        pygame.mixer.music.play()
        ser.write(data.encode())
        time.sleep(1)

def hello():
    audio_file = './new_audio_files/' + map_intent_to_sound('hello')
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

def sleep():
    audio_file = './new_audio_files/' + map_intent_to_sound('sleep')
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

def confusion():
    audio_file = './new_audio_files/' + map_intent_to_sound('confuse')
    pygame.mixer.music.load(audio_file)
    data = str(0) + "," + str(2) + "," + "0x7e28d4," + "0x7e28d4," #purple
    print("sending data :", data.encode())
    pygame.mixer.music.play()
    ser.write(data.encode())
    time.sleep(1)

# first color hex is for headrest
# second color hex is for footrest
def set_footrest(i):  # selecting the footrest, degree1, color1, color2
    if i>=90:
        audio_file = './new_audio_files/' + map_intent_to_sound('move_up')
    if i<90:
        audio_file = './new_audio_files/' + map_intent_to_sound('move_down')
    pygame.mixer.music.load(audio_file)
    data = str(2) + "," + str(i) + "," + '0x00ffff,' + '0x00ffff,'#blue
    print("sending data :", data.encode())
    ser.write(data.encode())
    for i in range(1):
        pygame.mixer.music.play()
        time.sleep(2)
    confirmation()




# first color hex is for headrest
# second color hex is for footrest
def set_headrest(i):  # selecting the footrest, degree1, color1, color2
    if i >= 90:
        audio_file = './new_audio_files/' + map_intent_to_sound('move_up')
    if i < 90:
        audio_file = './new_audio_files/' + map_intent_to_sound('move_down')
    pygame.mixer.music.load(audio_file)
    data = str(1) + "," + str(i) + "," + '0x00ffff,' + '0x00ffff,'#blue
    print("sending data :", data.encode())
    ser.write(data.encode())
    for i in range(1):
        pygame.mixer.music.play()
        time.sleep(2)
    confirmation()




def turn_off():
    data = str(0) + "," + str(2) + "," + "0xFFFFFF," + "0xFFFFFF," #white

    audio_file = './new_audio_files/' + map_intent_to_sound('turn_off')
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
        print("serial port:"+ read)
        return read


voice_switch = False

i = 1

while True:
    recv_message = receiveData()

    if (recv_message == "Start"):
        voice_switch = True
        robot_state['status'] = "on_waiting"
        recv_message = ""
        print(voice_switch, robot_state)

    if (voice_switch == False and robot_state['status'] == "on_waiting"):
        print("Now sleeping....")
        sleep()
        content = listen.main()
        content =  pattern.sub(replace_substrings, str(content[-1]))
        print("Detecting intent for text: ", content)
        obj_dialogflow = detect.detect_intent_texts([content])
        detected_intent = obj_dialogflow['intent']
        if ("Default Welcome Intent" in detected_intent):
            voice_switch = True
            pygame.mixer.music.stop()

    if (voice_switch == True and robot_state['status'] == "on_waiting"):
        hello()
        print("Now listening to you speak....")
        content = listen.main()
        content =  pattern.sub(replace_substrings, str(content[-1]))
        print("Detecting intent for text: ", content)
        obj_dialogflow = detect.detect_intent_texts([content])
        detected_intent = obj_dialogflow['intent']
        if ("Move the bed" in detected_intent):
            detected_location = obj_dialogflow['location']
            detected_direction = obj_dialogflow['direction']
            detected_degree = obj_dialogflow['degree']
            print("Now switch the bed state to 'selection'...")
            robot_state['status'] = 'selection'

            if (len(detected_location) != 0):
                print("Now switch the bed state to 'upordown'...")
                robot_state['status'] = 'upordown'
        elif("Finish" in detected_intent):
            turn_off()
        else:
            confusion()

    while (voice_switch == True and robot_state['status'] == 'selection'):
        print("Now executing 'selection' command...")
        execute_selection()
        print("Now listening to you speak....")
        content = listen.main()
        content =  pattern.sub(replace_substrings, str(content[-1]))
        obj_dialogflow = detect.detect_intent_texts([content])
        detected_intent = obj_dialogflow['intent']
        if ("Move the bed" not in detected_intent):
            confusion()
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
            while (len(detected_direction) == 0):
                print("head UP or Down?")
                select_headrest(robot_state['headrest_angle'])
                execute_wait()
                content = listen.main()
                content =  pattern.sub(replace_substrings, str(content[-1]))
                obj_dialogflow = detect.detect_intent_texts([content])
                detected_intent = obj_dialogflow['intent']
                if ("Move the bed" not in detected_intent):
                    confusion()
                    print("No intent detected...looping again")
                    continue
                detected_direction = obj_dialogflow['direction']

            else:
                if ('up' in detected_direction):
                    if (detected_degree != ""):
                        robot_state['headrest_angle'] = robot_state['headrest_angle'] + int(detected_degree)
                        set_headrest(robot_state['headrest_angle'])
                    else:
                        robot_state['headrest_angle'] = robot_state['headrest_angle'] + 15
                        set_headrest(robot_state['headrest_angle'])
                    print('move the headrest up now')


                if ('down' in detected_direction):
                    if (detected_degree != ""):
                        robot_state['headrest_angle'] = robot_state['headrest_angle'] - int(detected_degree)
                        set_headrest(robot_state['headrest_angle'])
                    else:
                        robot_state['headrest_angle'] = robot_state['headrest_angle'] - 15
                        set_headrest(robot_state['headrest_angle'])
                    print('move the headrest down now')


        if (detected_location == 'footrest'):
            while (len(detected_direction) == 0):
                print("foot UP or Down?")
                select_footrest(robot_state['footrest_angle'])
                execute_wait()
                content = listen.main()
                content =  pattern.sub(replace_substrings, str(content[-1]))
                obj_dialogflow = detect.detect_intent_texts([content])
                detected_intent = obj_dialogflow['intent']
                if ("Move the bed" not in detected_intent):
                    confusion()
                    print("No intent detected...looping again")
                    continue
                detected_direction = obj_dialogflow['direction']

            else:
                if ('up' in detected_direction):
                    if (detected_degree != ""):
                        robot_state['footrest_angle'] = robot_state['footrest_angle'] + int(detected_degree)
                        set_footrest(robot_state['footrest_angle'])
                    else:
                        robot_state['footrest_angle'] = robot_state['footrest_angle'] + 15
                        set_footrest(robot_state['footrest_angle'])
                    print('move the footrest up now')


                if ('down' in detected_direction):
                    if (detected_degree != ""):
                        robot_state['footrest_angle'] = robot_state['footrest_angle'] - int(detected_degree)
                        set_footrest(robot_state['footrest_angle'])
                    else:
                        robot_state['footrest_angle'] = robot_state['footrest_angle'] - 15
                        set_footrest(robot_state['footrest_angle'])
                    print('move the footrest down now')

        voice_switch = False
        robot_state['status'] = "on_waiting"
        break
