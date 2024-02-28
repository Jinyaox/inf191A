# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
import RPi.GPIO as GPIO
import time
import os


# Setup GPIO 
L1 = 25
L2 = 8
L3 = 7
L4 = 1

C1 = 12
C2 = 16
C3 = 20
C4 = 21

# Initialize the GPIO pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[0]
    if(GPIO.input(C2) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[1]
    if(GPIO.input(C3) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[2]
    if(GPIO.input(C4) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[3]


if __name__=="__main__":
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    output = np.empty((240, 320, 3), dtype=np.uint8)
    directory="./imageset"

    # Initialize some variables
    face_locations = []
    face_encodings = []
    names=[]

    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
    
    # Iterate over files in the directory
    for file_name in os.listdir(directory):
        # Check if the item is a file (not a directory)
        if os.path.isfile(os.path.join(directory, file_name)):
            print(file_name)
            face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(file_name))[0])
            names.append(file_name)

    try:

        while True:

            # call the readLine function for each row of the keypad
            if readLine(L3, ["7","8","9","C"])=="C":
                name = "<Unknown Person>"
                camera.capture(output, format="rgb")
                face_locations = face_recognition.face_locations(output)
                face = face_recognition.face_encodings(output, face_locations)
                
                for i in range(len(face_encodings)):
                    match = face_recognition.compare_faces([face_encodings[i]], face[0])
                    if match[0]:
                        name = names[i]
                        print("Name Exists")
                
                print("User Not Found")
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nApplication stopped!")

