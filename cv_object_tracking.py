# Anjali Punnoose
# LunaLink Systems
# Fall 2024

# Program to Conduct Computer Vision based Object Tracking via Raspberry Pi Camera
# and Display Camera feed onto Node-Red Dashboard


import time
import keyboard
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import requests



def send_image_nodered(img):
    # Function to Send Image Frame to Node-Red via HTTP Request

    # IP Changes based on RPi and Connection Method
    # Possible IPs:  WIFI:[10.251.190.11, 10.250.148.190] OR via Switch:[192.168.88.6, 192.168.88.7]
    node_red_url = "http://10.251.35.190/:1880/image"
    # Encode the image as JPEG
    _, buffer = cv2.imencode('.jpg', img)

    # Send to Node-RED
    try:
        requests.post(node_red_url, data=buffer.tobytes(), headers={"Content-Type": "image/jpeg"})
    except requests.exceptions.RequestException as e:
        print(f"Failed to send image to Node-RED: {e}")
         


# Create a PiCamera object
with PiCamera() as camera:
    time.sleep(2)

    # Set the camera resolution (optional)
    camera.resolution = (912, 768)
    camera.framerate = 64
    rawCapture = PiRGBArray(camera, size=(912, 768))
    # rawCapture = PiRGBArray(camera, size=(357, 300))

    # Allow the camera to warm up
    time.sleep(0.1)

    # Define the color range for the object to track (HSV values)
    # HSV values for green object: 
    lower_color = np.array([40, 70, 70])  # Adjust the values for your object color
    upper_color = np.array([80, 255, 255])

    # Loop over frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Grab the frame from the NumPy array
        image = frame.array

        # Convert the frame to the HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask for the color using the boundaries
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Proceed if any contours were found
        if len(contours) > 0:
            # Find the largest contour in the mask, then use it to compute the bounding box
            largest_contour = max(contours, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(largest_contour)

            # Draw a rectangle around the object
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Optionally, calculate the center of the object and mark it
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)
            cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
            print("Largest Contour Area: ", cv2.contourArea(largest_contour))

        # Show the resulting frame
        cv2.imshow("Object Tracking", image)
        send_image_nodered(image)

        # Clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # Break from the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close any open windows
    cv2.destroyAllWindows()
