import tty
import termios
import time
import sys
import os
import cv2

import hiwonder.Board as Board
import hiwonder.Camera as Camera
import hiwonder.ActionGroupControl as AGC
import hiwonder.yaml_handle as yaml_handle

open_once = yaml_handle.get_yaml_data('/boot/camera_setting.yaml')['open_once']
if open_once:
    my_camera = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream?dummy=param.mjpg')
else:
    my_camera = Camera.Camera()
    my_camera.camera_open()        
# pic = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream?dummy=param.mjpg') # video capture source camera (Here webcam of laptop) 

while(True):
    ret,frame = my_camera.read() # return a single frame in variable `frame`
    cv2.imshow('img1',frame) #display the captured image
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        # cv2.imwrite('images/c1.png',frame)
        cv2.destroyAllWindows()
        break

pic.release()

