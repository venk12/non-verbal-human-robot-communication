import serial
import time

# Configure the serial port
ser = serial.Serial('COM3', 115200)  # Replace 'COM3' with the correct port name

# Define the command
command = "45,45,HAPPY"

# Send the command to the Arduino
ser.write(command.encode())

# Optional: Wait for a response from the Arduino (if the Arduino sends a response)
response = ser.readline()
print("Arduino response:", response.decode().strip())

# Close the serial port
ser.close()