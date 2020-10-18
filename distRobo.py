import RPi.GPIO as GPIO                    #Import GPIO library
import time
from time import sleep
import cv2
import numpy as np
import face_recognition
import os


TRIG = 27
ECHO = 17

m11=25
m12=12
m21=20
m22=16

name = None

#Save images
path = 'images'
images = []
classnames = []
myList = os.listdir(path)
print(myList)

#Create Encodings and save before actual code starts
for cl in myList:
    curImg  = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classnames.append(os.path.splitext(cl)[0])

print(classnames)

def findEncodings(images):
    encodeList = []
    for img in images:
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

def setup() :
    #Import time library
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)                    # programming the GPIO by BCM pin numbers

    GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs
    GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input

    GPIO.setup(m11,GPIO.OUT)
    GPIO.setup(m12,GPIO.OUT)
    GPIO.setup(m21,GPIO.OUT)
    GPIO.setup(m22,GPIO.OUT)
    
    time.sleep(1)

def loop():

        
    def stop():
        print ("stop")
        GPIO.output(m11, 0)
        GPIO.output(m12, 0)
        GPIO.output(m21, 0)
        GPIO.output(m22, 0)
        
        while True:
            print ("Camera started")
            success, img = cap.read()
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            faceLocCur = face_recognition.face_locations(imgS)
            encodeCur = face_recognition.face_encodings(imgS,faceLocCur)

            for encodeFace,faceLoc in zip(encodeCur,faceLocCur):
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                print("FaceDistance: " , faceDis)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classnames[matchIndex].upper()
                    print(name)
                    y1,x2,y2,x1 = faceLoc

                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,name,(x1+5,y2-5),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                cv2.imshow('Webcam',img)
                cv2.waitKey(1)
            
                if (name=='PRI') :
                    GPIO.output(m11, 1)
                    GPIO.output(m12, 0)
                    GPIO.output(m21, 0)
                    GPIO.output(m22, 0)
                    print ("right")
                    time.sleep(0.5)
                    GPIO.output(m11, 0)
                    GPIO.output(m12, 0)
                    GPIO.output(m21, 0)
                    GPIO.output(m22, 0)

    def forward():
        GPIO.output(m11, 1)
        GPIO.output(m12, 0)
        GPIO.output(m21, 1)
        GPIO.output(m22, 0)
        print ("Forward")

    def back():
        GPIO.output(m11, 0)
        GPIO.output(m12, 1)
        GPIO.output(m21, 0)
        GPIO.output(m22, 1)
        print ("back")

    def left():
        GPIO.output(m11, 0)
        GPIO.output(m12, 0)
        GPIO.output(m21, 1)
        GPIO.output(m22, 0)
        print ("left")

    def right():
        GPIO.output(m11, 1)
        GPIO.output(m12, 0)
        GPIO.output(m21, 0)
        GPIO.output(m22, 0)
        print ("right")

    stop()
    count=0
    while True:
        i=0
        avgDistance=0
        for i in range(5):
            GPIO.output(TRIG, False)                 #Set TRIG as LOW
            time.sleep(0.1)                                   #Delay

            GPIO.output(TRIG, True)                  #Set TRIG as HIGH
            time.sleep(0.00001)                           #Delay of 0.00001 seconds
            GPIO.output(TRIG, False)                 #Set TRIG as LOW

            while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW
               #GPIO.output(led, False)
              pulse_start = time.time()

            while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH
               #GPIO.output(led, False)
              pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor

            distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
            distance = round(distance,2)                 #Round to two decimal points
            avgDistance=avgDistance+distance
            avgDistance=avgDistance/5
            print (avgDistance)
     
    if avgDistance < 15:      #Check whether the distance is within 15 cm range
        stop()

    else:
        forward()
    
def destroy():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()