import serial
import time
import random
import pygame
import re
import sys

import speech_recog as listen
import detect_intent as detect

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Define the serial port and baud rate (adjust the port as needed)
ser = serial.Serial('COM3', 115200)  # Replace 'COMX' with your Arduino's serial port
emotions = ["NEUTRAL", "ANGRY", "SAD", "HAPPY"]

map_intent_to_sound = {
    "Default Welcome Intent": {
      "Emotion":"HAPPY",
      "Sound_1":"answer.wav",
      "Sound_2":"Ja.mp3"
    },
    "Default Fallback Intent": {
      "Emotion":"QUESTION",
      "Sound_1":"what.mp3",
      "Sound_2":""
    },
    "Move the bed": {
      "Emotion": "CONFIRMATION",
      "Sound_1":"okay.mp3",
      "Sound_2":""
    },
    "Sleep": {
      "Emotion":"NEUTRAL",
      "Sound_1":"music-box-lullaby.wav",
      "Sound_2":"male-sleep-breathe.wav"
    },
    "Understood": {
      "Emotion":"HAPPY",
      "Sound_1":"ah ha.mp3",
      "Sound_2":""
    },
    "Wakeup": {
      "Emotion":"SAD",
      "Sound_1":"yawn.wav",
      "Sound_2":"Ja.mp3"
    },
    "Cleaning": {
      "Emotion":"SUPRISED",
      "Sound_1":"awww.mp3",
      "Sound_2":""
    },
    "Nurse": {
      "Emotion":"NURSE",
      "Sound_1":"ding-dong.wav",
      "Sound_2":""
    }
}

def generate_random_servo_pos():
    
    # Servo 1 position : 90 (flat + Incline) to 60 (footrest down) - Footrest
    # Servo 2 positions: 90 (Flat) to 165 (Vertical) - Headrest

    servoPos = [random.randint(60, 90), random.randint(90, 165)]
    return servoPos

def update_emotions(emotions):
    while True:
        random_emotion = random.choice(emotions)
        yield random_emotion

def sendData(intent):
    print("Sending data to arduino...")
    servo_pos = generate_random_servo_pos()
    emotion_generator = update_emotions(emotions)
    emotion = next(emotion_generator)

    # emotion = map_intent_to_sound[intent]['Emotion']
    print("Emotion detected:",emotion)
    
    data =  str(servo_pos[0]) + "," + str(servo_pos[1]) + "," + emotion+ "," + "footrest," 
    print("data :", data.encode())
    ser.write(data.encode())

    # print("Now playing the corresponding sound for...:", emotion)

    audio_file = './audio/'+ map_intent_to_sound[intent]['Sound_1']
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def receiveData():
    # Receive data from the Arduino. The Arduino sends back what it received.
    read = ""
    while ser.in_waiting > 0:
        incomingData = ser.read().decode()  # Read one byte and decode it as a string
        if incomingData != '\n':
            read += incomingData
    
    if len(read) > 0:
        print(read)
        # You can add your own code here to process the received data if needed

i = 1
# Example usage:
try:
    while True:
        # listen_and_transcribe()
        
        if(i == 1):
            detected_intent = "Default Welcome Intent"
          
        elif(i != 1):
          print("Now listening to you speak....")
          content = listen.main()
          print("Detecting intent for text: ", str(content[-1]))
          obj_dialogflow = detect.detect_intent_texts([str(content[-1])])

          detected_intent  = obj_dialogflow['intent']
          bed_part = obj_dialogflow['bed_part']
          bed_degree = obj_dialogflow['bed_degree']

          if(content == ""):
              print("No transcription.. ")
              detected_intent = "Default Fallback Intent"

          elif(content != ""):
            obj_dialogflow = detect.detect_intent_texts([str(content[-1])])
            detected_intent  = obj_dialogflow['intent']
            bed_part = obj_dialogflow['bed_part']
            bed_degree = obj_dialogflow['bed_degree']
            
            print('Intent Detected:', detected_intent)
            
            if(detected_intent=='Move the bed'):
              print("Move the bed intent detected! ")
              print("Move the ", bed_part," to degrees: ", bed_degree)  
            
            elif(detected_intent==''):
              print("No Intent Detected..")
              detected_intent = "Default Fallback Intent"
              break
        
        sendData(detected_intent)
        receiveData()

        i+=1
        # break;

except KeyboardInterrupt:
    print("Ctrl+C pressed. Cleaning up resources...")
    pygame.mixer.quit()
    pygame.quit()
    # Reinitialize audio resources if needed
    # audio_interface = pyaudio.PyAudio()
    # stream = audio_interface.open(
    #     format=pyaudio.paInt16,
    #     channels=1,
    #     rate=RATE,
    #     input=True,
    #     frames_per_buffer=CHUNK,
    #     stream_callback=_fill_buffer,
    # )
    
    sys.exit(0)

      # Call sendData() to send data to the Arduino
    # time.sleep(5)  # Call receiveData() to receive data from the Arduino
