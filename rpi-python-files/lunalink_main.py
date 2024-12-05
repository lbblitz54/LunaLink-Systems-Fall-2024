# Anjali Punnoose
# LunaLink Systems
# Fall 2024

# Program to Conduct Main Tasks of LunaLink Systems :
#     - Camera Based Computer Vision Object Tracking of Green Laser 
#     - Manual Control of 2D Rotational Movement
#     - Automated Alignment of System with Reciprocal System
#     - Displays and Interaction with GUI on Node-Red Dashboard

# Previously Named : alignment_rpiCam.py   


import time
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import serial
import subprocess
import requests
import threading
from flask import Flask, request



### VARIABLES ###

# HSV range for green laser
lower_green = np.array([40, 70, 70])  
upper_green = np.array([80, 255, 255]) 

# X & Y Movements by Stage (units of DC Motor steps)
delta_x_1 = 100
delta_y_1 = 50
delta_x_2 = 20
delta_y_2 = 20
vel_1 = 250
vel_2 = 150

# X & Y Current Position (units of DC Motor steps)
x_pos = 0
y_pos = 33000

# X & Y Total Range of Motion (units of DC Motor steps)
x_max_pos = 50000 # 
y_max_pos = 33000

# X & Y Bounds of Motion varying by stage (units of DC Motor steps)
x_upper_bound = x_max_pos
x_lower_bound = 0
y_upper_bound = y_max_pos
y_lower_bound = 0


# IP of other device being pinged
# IP Changes based on RPi and Connection Method
# Possible IPs:  WIFI:[10.251.190.11, 10.250.148.190] OR via Switch:[192.168.88.6, 192.168.88.7]
other_device_ip = "10.251.190.11" 

# Conditional Requirements for movement
is_moving = False
target_detected = False
ping_successful = False
direction_right = False # [0:"LEFT", 1:"RIGHT"]
direction_down = True # [0: "UP", 1: "DOWN"]
target_not_detected_count = 0 # Count how many times
toggle_state_auto = False

frame_x = 912
frame_y = 720

stage = 1




# NODE RED DASHBOARD HTTP REQUEST INIT 

app = Flask(__name__)

@app.route('/up', methods=['POST'])    # UP Arrow Button
def up_logic():
    global toggle_state_auto, y_pos
    if( not toggle_state_auto and y_pos < y_upper_bound):
        word = "R 0 U 100 100"
        line = ""
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
        y_pos += 100
        print("UP Button clicked! Logic triggered.")
    else:
        print(x_pos, y_pos, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound)
    return "Logic executed", 200

@app.route('/down', methods=['POST'])    # DOWN Arrow Button
def down_logic():
    global toggle_state_auto, y_pos
    if( not toggle_state_auto and y_pos > y_lower_bound):
        line = ""
        word = "R 0 D 100 100"
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
        y_pos -= 100
        print("DOWN Button clicked! Logic triggered.")
    else:
        print(x_pos, y_pos, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound)

    return "Logic executed", 200

@app.route('/left', methods=['POST'])    # LEFT Arrow Button
def left_logic():
    global toggle_state_auto, x_pos
    if( not toggle_state_auto and x_pos > x_lower_bound):
        line = ""
        word = "L 100 U 0 100"
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
        x_pos -= 100
        print("LEFT Button clicked! Logic triggered.")
    else:
        print(x_pos, y_pos, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound)

    return "Logic executed", 200

@app.route('/right', methods=['POST'])    # RIGHT Arrow Button
def right_logic():
    global toggle_state_auto, x_pos
    if( not toggle_state_auto and x_pos < x_upper_bound):
        line = ""
        word = "R 100 U 0 100"
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
        x_pos += 100
        print("RIGHT Button clicked! Logic triggered.")
    else:
        print(x_pos, y_pos, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound)
    return "Logic executed", 200

@app.route('/toggle', methods=['POST']) # MANUAL/AUTOMATIC Toggle Switch
def toggle_logic():
    #Assumes that Toggle switch is at False (Manual) before running
    global toggle_state_auto, stage, is_moving
    toggle_state_auto = not toggle_state_auto
    if(not toggle_state_auto):
        stage = 1
        x_upper_bound = x_max_pos
        x_lower_bound = 0
        y_upper_bound = y_max_pos
        y_lower_bound = 0
    is_moving = False
    print(f"Toggle state updated: {toggle_state_auto}")
    return str(toggle_state_auto), 200

def ping():
    ## Function to ping another device and print the ping attempt result
    ## Returns whether successful ping or not based on the return code
    global other_device_ip
    command = ["ping", "-c", "4", other_device_ip]  # Command to Send 4 ICMP packets
    result = subprocess.run(command, stdout=subprocess.PIPE)
    print(result)
    return result.returncode == 0 

def get_move_cmd():
    ## Function to determine movement based on stage of alignment, direction of motion, and current location 
    ## Returns constructed movement command to send to Arduino

    global direction_right, x_pos, x_upper_bound, x_lower_bound, y_pos, y_lower_bound, y_upper_bound, direction_down
    global delta_x_1, delta_x_2, delta_y_1, delta_y_2, vel_1, vel_2

    cmd = "stop"
    if(stage == 1):
        if(direction_right and x_pos < x_upper_bound):
            cmd = "R " + str(delta_x_1) + " U 0 " + str(vel_1)
            x_pos += delta_x_1
        elif(not direction_right and x_pos > x_lower_bound):
            cmd = "L " + str(delta_x_1) + " U 0 " + str(vel_1)
            x_pos -= delta_x_1
        elif(direction_down and y_pos > y_lower_bound):
            cmd = "L 0 D " + str(delta_y_1) + " " + str(vel_1)
            y_pos -= delta_y_1
            direction_right = not direction_right
        elif(not direction_down and y_pos < y_upper_bound):
            cmd = "L 0 U " + str(delta_y_1) + " " + str(vel_1)
            y_pos += delta_y_1
            direction_right = not direction_right
        else:
            direction_down = not direction_down

    elif(stage == 2):
        if(direction_right and x_pos < x_upper_bound):
            cmd = "R " + str(delta_x_2) + " U 0 " + str(vel_2)
            x_pos += delta_x_2
        elif(not direction_right and x_pos > x_lower_bound):
            cmd = "L " + str(delta_x_2) + " U 0 " + str(vel_2)
            x_pos -= delta_x_2
        elif(direction_down and y_pos > y_lower_bound):
            cmd = "L 0 D " + str(delta_y_2) + " " + str(vel_2)
            y_pos -= delta_y_2
            direction_right = not direction_right
        elif(not direction_down and y_pos < y_upper_bound):
            cmd = "L 0 U " + str(delta_y_2) + " " + str(vel_2)
            y_pos += delta_y_2
            direction_right = not direction_right
        else:
            direction_down = not direction_down

    elif(stage == 3): #Stage 3 Alignment based on pings
        global ping_successful 
        ping_successful = ping()
        if(not ping_successful): 
            if(direction_right and x_pos < x_upper_bound):
                cmd = "R " + str(delta_x_2) + " U 0 " + str(vel_2)
                x_pos += delta_x_2
            elif(not direction_right and x_pos > x_lower_bound):
                cmd = "L " + str(delta_x_2) + " U 0 " + str(vel_2)
                x_pos -= delta_x_2
            elif(direction_down and y_pos > y_lower_bound):
                cmd = "L 0 D " + str(delta_y_2) + " " + str(vel_2)
                y_pos -= delta_y_2
                direction_right = not direction_right
            elif(not direction_down and y_pos < y_upper_bound):
                # cmd = move_cmds.get("up-2")
                cmd = "L 0 U " + str(delta_y_2) + " " + str(vel_2)
                y_pos += delta_y_2
                direction_right = not direction_right
            else:
                direction_down = not direction_down

    return cmd

def send_image_nodered(image):
 
    node_red_url = "http://10.250.148.190:1880/image"  # IP Changes based on RPi and Connection Method
    # Encode the image as JPEG
    _, buffer = cv2.imencode('.jpg', image)

    # Send to Node-RED
    try:
        requests.post(node_red_url, data=buffer.tobytes(), headers={"Content-Type": "image/jpeg"})
    except requests.exceptions.RequestException as e:
        print(f"Failed to send image to Node-RED: {e}")
                   

def run_flask():
    # Function to Run the Flask server (called in a different thread)
    # Flask server used to handle HTTP requests from Node-Red Server
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

### SERIAL CONNECTION TO ARDUINO INIT ###
ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1)
ser.flush()

### INIT SEPARATE THREAD FOR FLASK SERVER ###
# Flask Server is blocking server that takes up main thread and prevents other code from running
# Flask Server used to handle HTTP requests from Node-Red Server for GUI Interaction
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True  # Ensures the Flask thread ends when the main program ends
flask_thread.start()



### MAIN THREAD ###
if __name__ == '__main__':
    # Main thread can perform other tasks
    while True:
        
        # Create a PiCamera object
        with PiCamera() as camera:
            time.sleep(2)

            # Set the camera resolution (optional)
            camera.resolution = (frame_x, frame_y)
            camera.framerate = 100
            # camera.crop = (0,0,500,500)
            rawCapture = PiRGBArray(camera, size=(frame_x, frame_y))
            # Allow the camera to warm up
            time.sleep(0.1)

            # Loop over frames from the camera
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # Grab the frame from the NumPy array
                image = frame.array
                # Convert the frame to the HSV color space
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                # Create a mask for the color using the boundaries
                mask = cv2.inRange(hsv, lower_green, upper_green)
            
                # Find contours in the mask
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                # Proceed if any contours were found
                if len(contours) > 0:
                    # Find the largest contour in the mask, then use it to compute the bounding box
                    largest_contour = max(contours, key=cv2.contourArea)
                    (x, y, w, h) = cv2.boundingRect(largest_contour)

                    # print("largest contour: ", cv2.contourArea(largest_contour))
                    
                    if cv2.contourArea(largest_contour) > 100000:
                        target_detected = True
                    else:
                        target_detected = False

                    # Draw a rectangle around the object
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Optionally, calculate the center of the object and mark it
                    center_x = int(x + w / 2)
                    center_y = int(y + h / 2)
                    cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
                    # print(center_x, center_y)
                    # print("pos: ", x_pos, y_pos)

                # Show the resulting frame
                cv2.imshow("Object Tracking", image)
                send_image_nodered(image) 


                ### AUTOMATIC MODE ###
                if toggle_state_auto:
                    ### TARGET FOUND ### 
                    if target_detected:

                        target_not_detected_count = 0
                        cmd = "stop"
                        ser.write(f"{cmd}\n".encode('utf-8'))
                        ser.flush()
                        time.sleep(0.03)

                        if(stage == 1):
                            stage = 2         
                            x_lower_bound = x_pos - delta_x_1*3
                            x_upper_bound = x_pos + delta_x_1*3
                            y_lower_bound = y_pos - delta_y_1
                            y_upper_bound = y_pos + delta_y_1
                            direction_right = not direction_right
                        elif(stage == 2):
                            stage = 3

                        # Read response from Arduino due to move command
                        while ser.in_waiting > 0:
                            line = ser.readline().decode('utf-8').rstrip()  
                            print(f"Arduino Output: {line}")
                            if line == "end-motion":
                                is_moving = False

                    # Automatic Movement Commands 
                    if(not is_moving and (not target_detected or not ping_successful)):
                        # print(target_detected, ping_successful)
                        cmd = get_move_cmd()
                        print(cmd)
                        # Send Command to Arduino 
                        ser.write(f"{cmd}\n".encode('utf-8'))
                        ser.flush()
                        time.sleep(0.03)

                        # Read response from Arduino due to move command
                        while ser.in_waiting > 0:
                            line = ser.readline().decode('utf-8').rstrip()  
                            print(f"Arduino Output: {line}")
                            if(line.find("Right") != -1 or line.find("Left") != -1):
                                is_moving = True
                            elif line == "end-motion":
                                is_moving = False
                    
                    # Read any pending response from Arduino
                    while ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').rstrip()  
                        print(f"Arduino Output: {line}")

                        if line == "end-motion":
                            is_moving = False

                    # Reset to Stage 1 if Target is undetected for too long
                    if(stage != 1 and not target_detected):
                        if (target_not_detected_count > 2000):
                            stage = 1
                        elif (ping_successful):
                            target_not_detected_count = 0
                        else:
                            target_not_detected_count += 1
                    

                # Clear the stream in preparation for the next frame
                rawCapture.truncate(0)

                # Break from the loop if the user presses 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release the camera and close any open windows
            cv2.destroyAllWindows()
