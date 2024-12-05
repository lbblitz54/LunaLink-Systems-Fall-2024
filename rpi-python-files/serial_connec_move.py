# Anjali Punnoose
# LunaLink Systems
# Fall 2024

# Program to Establish Serial Connection between RPi and Arduino Mega 2560
# to simultaneously control 2 NEMA 17 Motors for vertical and horizontal movement

import serial
import time
import log

# Open the serial port corresponding to the Arduino
ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1)
ser.flush()
word = ""
line = ""

while True:

    word = input("Enter move command (EX: right 20 & up 30 steps & 300 us pulse delay: \"R 20 U 30 300\" ): ")
    print(word)
    ser.write(f"{word}\n".encode('utf-8'))
    ser.flush()
    time.sleep(1)

    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()  # Read response from Arduino
        print(f"Arduino Output: {line}")
    # Force wait Arduino to return value
    if line != "end-motion" and line != "":
        # Force wait Arduino to return value
        while ser.in_waiting <= 0:
                continue
    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()  # Read response from Arduino
        print(f"Arduino Output: {line}")
