#General Modules
import cv2
import time
import numpy as np
import socket

#PI Camera specific modules
from picamera.array import PiRGBArray
from picamera import PiCamera

#User created modules
import UDP_Server
from Image_Processing import process_image



def getVideo():
    
    #Initialize Camera Stream
    camera = PiCamera()
    camera.resolution=(320,240)

    #These values are subject to change, use the Testing Suite to determine what range of values you want
    camera.brightness =50
    camera.ISO = 100
    
    camera.shutter_speed = 1000
    rawCapture = PiRGBArray(camera,size=(320,240))

    ###Edit the line below and change the IP address to your robot's ip (i.e. "10.30.61.17"), port is an arbitrary number
    server = UDP_Server.server("Robot IP",9000) #(IP,PORT)
    

    #frame_time is a pretty precise way of getting the timestamp of your image if you need it
    frame_time = time.time()
    for frame in camera.capture_continuous(rawCapture,format = 'bgr',use_video_port = True):
        image = frame.array

        ###DO YOUR PROCESSING HERE USING OpenCV and the image variable
        ###Refer to the Image Processing module and call its function process_image here
        process_image(image)
        
        
        ###Input your data and tags into the list below to send data to the rio
        ###This data is converted to a json string FYI, makes the sending faster
        server.sendData({"X":0, "Y":0, "Z":0,"Time":frame_time})
        
        #this trunctates the stream of images to grab the current image
        rawCapture.truncate(0)
        frame_time = time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


getVideo()
