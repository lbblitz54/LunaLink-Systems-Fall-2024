# LunaLink-Systems-Fall-2024
LunaLink Systems Capstone Software 

By: Anjali Punnoose, Kyle Byrum, Matthew Payne, Adrian Favela

## About the Project
LunaLink Systems is a Capstone Project team of engineering students from Texas A&M University under Dr. Ana Goulart. 

The aim of LunaLink Systems was to develop a Free Space Optics (FSO) device which will autonomously align itself with the reciprocal FSO system via a motorized mount which will use a mounted fiber optic cable connector to enable uninterrupted wireless communication to be sent from one node to another.

This GitHub contains a repository of the main programming files, libraries, and framework

### Built With

This section lists the major frameworks/libraries used to bootstrap the project. 

Devices: 
* Raspberry Pi
* Arduino MEGA 2560

Frameworks and Languages:
* Visual Studio Code
* Node-RED
* python
* C++

Libraries
* python3-opencv
* picamera
* flask
  
Node-RED Palettes
* node-red
* node-red-contrib-ui-led
* node-red-dashboard

## How to Use each file

There are 3 sets of files:
* Arduino Files
* Python Files
* Node-Red Dashboard Files

### Arduino Files:

**1. basic_motor_control.ino:**
   
   This file allows basic motor control directly with 1 NEMA 17 motor.
   The NEMA 17 used in this project were powered with a 24 V supply and was connected to a Motor Driver for closed loop microstepper control.
   The pulse (PUL) pin and direction (DIR) pins were connected to the pins 39 and 35, respectively.
   
   Variables to change:
   
   * _steps_ : number of steps for motor
   * _delay_ : delay between steps in PWM (lower delay = faster motor rotation)
   * _digitalWrite(dirPin, HIGH)_ : shift between HIGH and LOW to change the direction of the shaft rotation

**2. simultaneous_move_vert_and_horiz.ino:**

   This file allows for basic motor control for 2 Motors directly and simultaneously for the same number of steps.
   
   Variables to change:
   
   * The vertical and horizontal pulse and direction GPIO pins should be changed based on your setup.
   * _steps_ : number of steps for motor
   * _pulseDelay_Vertical_ : delay between steps in PWM (lower delay = faster motor rotation)
   * _digitalWrite(dirPin_Vertical, HIGH)_ : shift between HIGH and LOW to change the direction of the shaft rotation for the vertical direction motor
   * _digitalWrite(dirPin_Horizontal, HIGH)_ : shift between HIGH and LOW to change the direction of the shaft rotation for the horizontal direction motor

   
**3. serial_connec_motor_control.ino:**

   This file allows for Serial Communication with Raspberry Pi (RPi) to Control 1 Motor to move CW or CCW. This is done by connecting the Arduino MEGA to the RPi via USB cord. The RPi then sends commands through the serial connection to tell the Arduino how to move the motor. This was used to test the Arduino to RPi connection to acheive basic motor control.

   The Proper Format for the Arduino to receive commands: "[L/R] [step count]" (EX: _L 500_  moves the motor Left for 500 steps) 
   
   Variables to change:
   
   * The motor pulse (PUL) and direction (DIR) GPIO pins should be changed based on your setup.
   * _pulseDelay_: delay between steps in PWM. Found in stepMotor() function. 
   
**4. dual_motor_control_serial_connec.ino:**

**This is the main file loaded to the Arduino during final Demo for LunaLink Tasks**

This file allows for Serial Communication with Raspberry Pi (RPi) to Control 2 NEMA 17 Motors in both horizontal and vertical directions. This is done by connecting the Arduino MEGA to the RPi via USB cord. The RPi then sends commands through the serial connection to tell the Arduino how to move the motor.



   The Proper Format to receive commands: "[L/R] [step count] [U/D] [step count] [pulse delay]" (EX: _L 500 U 200 150_  moves the horizontal motor Left for 500 steps and vertical motor Up for 200 steps both at a pulse delay of 150 us) OR "stop" will stop motion

   
   Variables to change:
   
   * The vertical and horizontal motor pulse (PUL) and direction (DIR) GPIO pins should be changed based on your setup.


  ### Raspberry Pi Python Files:

**1. cv_object_tracking.py:**

  This file allows for Computer Vision based Object Tracking via a Raspberry Pi Camera and Displays the Camera feed onto Node-Red Dashboard. This file uses the picamera and python3-opencv libraries. The Program detects the presence of a green laser and tracks the laser by marking its center with a red dot and its borders with a green box. It also display the camera feed onto the Node-RED Dashboard with an HTTP Request.
   
   Variables to change:
   
   * _node_red_url = "http://10.251.35.190/:1880/image"_ : change the IP address in URL based on the IP of the RaspberryPi Node-RED dashboard (EX: 10.251.35.190)

     
**2. serial_connec_move.py:**
This file allows Serial Connection between Raspberry Pi and Arduino Mega 2560 to simultaneously control 2 NEMA 17 Motors for vertical and horizontal movement. This is done by connecting the Arduino MEGA to the RPi via USB cord. The RPi then asks for input from the user for commands to send through the serial connection to tell the Arduino how to move the motors.
   
   Variables to change:
   
   * _ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1)_ : change the _/dev/ttyACM0_ based on the port that the Arduino MEGA is connected to. This can be determined on RPi terminal with the _ls /dev/tty*_ commmand, which lists all external ports

**3. diamond_move.py:** 

This file demonstrates simultaneous vertical and horizontal system movement in a diamond shape via the Raspberry Pi to Arduino Serial connection. This program loops through the commands infinitely until the program is terminated manually.

     
   Variables to change:
   
   * _ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1)_ : change the _/dev/ttyACM0_ based on the port that the Arduino MEGA is connected to. This can be determined on RPi terminal with the _ls /dev/tty*_ commmand, which lists all external ports
   * _move_cmds = ["R 20000 U 20000 100", "R 20000 D 20000 100", "L 20000 D 20000 100", "L 20000 U 20000 100"]_ : change the numbers to change the number of steps (EX 20000) to control distance and the pulse delay (100) to control speed

**4. lunalink_main.py:**

**This is the main file loaded to the Raspberry Pi during final Demo for LunaLink Tasks**

This file conducts the Main Tasks of LunaLink Systems :
  * Camera Based Computer Vision Object Tracking of Green Laser 
  * Manual Control of 2D Rotational Movement
  * Automated Alignment of System with Reciprocal System
  * Displays and Interaction with GUI on Node-Red Dashboard

  Variables to change:

  * _delta_x_1_ : step change in X (horizontal) position in stage 1
  * _delta_y_1_ : step change in Y (vertical) position in stage 1
  * _delta_x_2_ : step change in X (horizontal) position in stage 2
  * _delta_y_2_ : step change in Y (vertical) position in stage 2
  * _vel_1_ : pulse delay in stage 1 
  * _vel_2_ : pulse delay in stage 2
  * _x_pos_ : starting X (horizontal) position, then updated programmatically to reflect current X Pos (units of DC Motor steps)
  * _y_pos_ : starting Y (vertical) position, then updated programmatically to reflect current Y Pos (units of DC Motor steps)
  * _x_max_pos_ : Maximum Horizontal Step Range of motion (units of DC Motor steps)
  * _y_max_pos_: Maximum Vertical Step Range of motion (units of DC Motor steps)
  * _other_device_ip = "10.251.190.11"_: change to the IP of the OTHER Raspberry Pi that will be searched for during alignment
  * _node_red_url = "http://10.250.148.190/:1880/image"_ : change the IP address in URL based on the IP of the RaspberryPi Node-RED dashboard (EX: 10.250.148.190)


Before Running this file: 
  * Ensure device is manually pre-set to X and Y location that the _x_pos_ and _y_pos_ variables are set to
  * Start Node-RED first : In RPi Terminal enter _node-red start_
  * Open Node-RED Dashboard UI: In Browser go to: _http://<hostname IP>:1880/ui_ (EX: http://192.168.88.7:1880/ui)
  * Ensure the Manual/Automatic Toggle switch is set to Manual
  * Open a NEW RPi terminal (to keep node-red running) and enter: _export DISPLAY=:0_
  * Run this file: _python lunalink_main.py_


### Node-RED Dashboard Files:

**1. node-red-dashboard.txt:**

This file contains the .json in plain text to Import into the Node-RED Dashboard for the Graphical User Interface (GUI). This requires the palettes node-red, node-red-contrib-ui-led, node-red-dashboard to be previously installed. 

To Import this file:
* Open Node-RED 
* Navigate to the Menu tab and choose Import
* Copy and Paste the.json plain text then click import
* The Flow should automatically populate in a tab titled "Test Dashboard"
* Access this Dashboard UI In Browser at: _http://<hostname IP>:1880/ui_ (EX: http://192.168.88.7:1880/ui)

