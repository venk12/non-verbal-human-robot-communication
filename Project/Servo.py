# import pygame
# import serial
import tkinter as tk
import serial

# Define the serial port
ser = serial.Serial('COM5', 115200)  # Replace 'COMX' with your Arduino's COM port

def update_servo_positions():
    # Get servo positions from sliders and send to Arduino
    servo1_pos = servo1_slider.get()
    servo2_pos = servo2_slider.get()
    emotion = selected_emotion.get()
    data = f"{servo1_pos},{servo2_pos},{emotion},"
    ser.write(data.encode())

# Create a Tkinter window
root = tk.Tk()
root.title("Servo Control")

# Create servo position sliders
servo1_slider = tk.Scale(root, label="Servo 1 Position", from_=0, to=180)
servo1_slider.pack()
servo2_slider = tk.Scale(root, label="Servo 2 Position", from_=0, to=180)
servo2_slider.pack()

# Create emotion selection
selected_emotion = tk.StringVar()
emotions = ["NEUTRAL", "SUPRISED", "HAPPY", "ANGRY", "SAD"]
emotion_menu = tk.OptionMenu(root, selected_emotion, *emotions)
selected_emotion.set("NEUTRAL")
emotion_menu.pack()

# Create a button to update servo positions
update_button = tk.Button(root, text="Update Servos", command=update_servo_positions)
update_button.pack()

# Start the Tkinter main loop
root.mainloop()


