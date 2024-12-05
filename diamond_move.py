# Anjali Punnoose
# LunaLink Systems
# Fall 2024

# Program to demonstrate simultaneous vertical and horizontal system rotational movement in a diamond shape 

import serial
import time
import log

# Open the serial port corresponding to the Arduino
ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1)
ser.flush()
time.sleep(1) # Allow Serial Connection time to set up

move_cmds = ["R 20000 U 20000 100", "R 20000 D 20000 100", "L 20000 D 20000 100", "L 20000 U 20000 100"]
cmd_index = 0

while True:
    cmd = move_cmds[cmd_index]
    ser.write(f"{cmd}\n".encode('utf-8'))
    ser.flush()
    time.sleep(1)
    line = ""

    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()  # Read response from Arduino
        print(f"Arduino Output: {line}")
    
    if line != "end-motion" and line != "":
        # Force wait Arduino to return value
        while ser.in_waiting <= 0:
                continue
    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()  # Read response from Arduino
        print(f"Arduino Output: {line}")
    

    cmd_index += 1

    # reset index 
    if cmd_index >= 4:
        cmd_index = 0
    
