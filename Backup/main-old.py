from arduino_connection import establish_arduino_connection, send_data
from speech_to_text import listen_and_transcribe

import time
import random



    # Open connection to Arduino through COM3
arduinoSerial = establish_arduino_connection('com3', 115200)

def update_emotions(emotions_list):
    while True:
        random_emotion = random.choice(emotions_list)
        # print(f"Current emotion: {random_emotion}")
        yield random_emotion  # Yield the random emotion as a generator
        # time.sleep(0.5) # Sleep for 5 seconds before updating to the next random emotion

# from speech_to_text import transcribe_speech

def receiveData():
    # Receive data from the Arduino. The Arduino sends back what it received.
    read = ""
    while arduinoSerial.in_waiting > 0:
        incomingData = arduinoSerial.read().decode()  # Read one byte and decode it as a string
        if incomingData != '\n':
            read += incomingData
    
    if len(read) > 0:
        print(read)
        # You can add your own code here to process the received data if needed

    emotions = ["NEUTRAL", "ANGRY", "SAD", "HAPPY"]
    emotion_generator = update_emotions(emotions)

    # data = {"static": "whatever"}
    # send_data(arduinoSerial, data)
    # Start streaming microphone input and transcribe it using speech to text
    while True:
        intent = next(emotion_generator)
        print("Now sending intent:", intent)
        data = "94,84,"+intent+","
        send_data(arduinoSerial, data.encode())
        receiveData(arduinoSerial)
        time.sleep(0.5)
    
    # ser.close()
    

    # Send the transcribed text to dialogflow to get the intent of the text

    
    # Send the intent to arduino