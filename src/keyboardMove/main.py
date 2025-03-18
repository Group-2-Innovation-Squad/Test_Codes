import tty
import threading
import termios
import time
import sys
import os
import cv2
import numpy as np

import hiwonder.Board as Board
import hiwonder.Camera as Camera
import hiwonder.ActionGroupControl as AGC
import hiwonder.yaml_handle as yaml_handle

running = True
perfAct = ''
yCoord = 1500
xCoord = 1500
lock = threading.Lock()

instructions = '''Controls:\r
w: Move Forward\r
a: Turn Left\r
s: Move Backward\r
d: Turn Right\r
q: Quit\r'''

def initCamera():
    Board.setPWMServoPulse(1, yCoord, 500)
    Board.setPWMServoPulse(2, xCoord, 500)
    open_once = yaml_handle.get_yaml_data('/boot/camera_setting.yaml')['open_once'] 
    if open_once:
        my_camera = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream?dummy=param.mjpg')
        return my_camera
    else:
        my_camera = Camera.Camera()
        my_camera.camera_open()
        return my_camera

def enterRaw():
    fd = sys.stdin.fileno()
    oSettings = termios.tcgetattr(fd)
    tty.setraw(fd)
    return fd, oSettings

def exitRaw(fd, oSet):
    termios.tcsetattr(fd, termios.TCSADRAIN, oSet)

def performAction():
    global perfAct
    while running:
        if len(perfAct) != 0:
            act = perfAct
            perfAct = ''
            AGC.runActionGroup(act)

def processInput():
    print('Input Init')
    global running
    global xCoord
    global yCoord
    while running:
        ch = cv2.waitKey(1)
        #print('Got Key Input')
        if ch == ord('w'):
            print('Move Forward\r')
            AGC.runActionGroup('go_forward')
        elif ch == ord('a'):
            print('Turn Left\r')
            AGC.runActionGroup('turn_left')
        elif ch == ord('s'):
            print('Move Backward\r')
            AGC.runActionGroup('back')
        elif ch == ord('d'):
            print('Turn Right\r')
            AGC.runActionGroup('turn_right')
        elif ch == ord('q'):
            print('Quitting...\r')
            running = False
        elif ch == ord('h'):
            print('Move Camera Left\r')
            xCoord -= 20
            xCoord = 500 if xCoord < 500 else xCoord
            Board.setPWMServoPulse(2, xCoord, 0.001)
        elif ch == ord('j'):
            print('Move Camera Down\r')
            yCoord -= 20
            yCoord = 1000 if yCoord < 1000 else yCoord
            Board.setPWMServoPulse(1, yCoord, 0.001)
        elif ch == ord('k'):
            print('Move Camera Up\r')
            yCoord += 20
            yCoord = 2000 if yCoord > 2000 else yCoord
            Board.setPWMServoPulse(1, yCoord, 0.001)
        elif ch == ord('l'):
            print('Move Camera Right\r')
            xCoord += 20
            xCoord = 2500 if xCoord > 2500 else xCoord
            Board.setPWMServoPulse(2, xCoord, 0.001)

def runningWindow(cam, mapx, mapy):
    print('Window Init')
    while running:
        ret, img = cam.read()
        if ret:
            # print('Update Frame')
            frame = img.copy()
            frame = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
            cv2.imshow('TonyPi Camera', frame)

def main():
    global running
    global perfAct
    global xCoord
    global yCoord
    
    # Path is hard coded into the functions
    param_data = np.load('/home/pi/TonyPi/Functions/CameraCalibration/calibration_param.npz')

    mtx = param_data['mtx_array']
    dist = param_data['dist_array']
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (640, 480), 0, (640, 480))
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (640, 480), 5)

    # fd, oSet = enterRaw()
    print(instructions)
    # os.set_blocking(sys.stdin.fileno(), False)
    cam = initCamera()
    t1 = threading.Thread(target=performAction)
    t1.start()

    while running:
        ret, img = cam.read()
        if ret:
            # print('Update Frame')
            frame = img.copy()
            frame = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
            cv2.imshow('TonyPi Camera', frame)

            ch = cv2.waitKey(1)
            #print('Got Key Input')
            if ch == -1:
                perfAct = ''
            elif ch == ord('w'):
                print('Move Forward\r')
                perfAct = 'go_forward'
            elif ch == ord('a'):
                print('Turn Left\r')
                perfAct = 'turn_left'
            elif ch == ord('s'):
                print('Move Backward\r')
                perfAct = 'back'
            elif ch == ord('d'):
                print('Turn Right\r')
                perfAct = 'turn_right'
            elif ch == ord('q'):
                print('Quitting...\r')
                running = False
            elif ch == ord('h'):
                print('Move Camera Left\r')
                xCoord -= 20
                xCoord = 500 if xCoord < 500 else xCoord
                Board.setPWMServoPulse(2, xCoord, 0.001)
            elif ch == ord('j'):
                print('Move Camera Down\r')
                yCoord -= 20
                yCoord = 1000 if yCoord < 1000 else yCoord
                Board.setPWMServoPulse(1, yCoord, 0.001)
            elif ch == ord('k'):
                print('Move Camera Up\r')
                yCoord += 20
                yCoord = 2000 if yCoord > 2000 else yCoord
                Board.setPWMServoPulse(1, yCoord, 0.001)
            elif ch == ord('l'):
                print('Move Camera Right\r')
                xCoord += 20
                xCoord = 2500 if xCoord > 2500 else xCoord
                Board.setPWMServoPulse(2, xCoord, 0.001)
#    t1 = threading.Thread(target=runningWindow, args=(cam, mapx, mapy,))
#    t2 = threading.Thread(target=processInput)
#
#    t1.start()
#    t2.start()
#
#    print('Created Threads')
#
#    t1.join()
#    t2.join()

#    while True:
#        ret, frame = cam.read()
#        if ret:
#            cv2.imshow('TonyPi Camera', frame)
#        try:
#            ch = chr(os.read(sys.stdin.fileno(), 1024)[-1])
#            if ch == 'w':
#                print('Move Forward\r')
#                AGC.runActionGroup('go_forward')
#            elif ch == 'a':
#                print('Turn Left\r')
#                AGC.runActionGroup('turn_left')
#            elif ch == 's':
#                print('Move Backward\r')
#                AGC.runActionGroup('back')
#            elif ch == 'd':
#                print('Turn Right\r')
#                AGC.runActionGroup('turn_right')
#            elif ch == 'q':
#                print('Quitting...\r')
#            elif ch == 'h':
#                print('Move Camera Left\r')
#                xCoord -= 20
#                xCoord = 500 if xCoord < 500 else xCoord
#                Board.setPWMServoPulse(2, xCoord, 0.001)
#            elif ch == 'j':
#                print('Move Camera Down\r')
#                yCoord -= 20
#                yCoord = 1000 if yCoord < 1000 else yCoord
#                Board.setPWMServoPulse(1, yCoord, 0.001)
#            elif ch == 'k':
#                print('Move Camera Up\r')
#                yCoord += 20
#                yCoord = 2000 if yCoord > 2000 else yCoord
#                Board.setPWMServoPulse(1, yCoord, 0.001)
#            elif ch == 'l':
#                print('Move Camera Right\r')
#                xCoord += 20
#                xCoord = 2500 if xCoord > 2500 else xCoord
#                Board.setPWMServoPulse(2, xCoord, 0.001)
#        except:
#            continue
    # exitRaw(fd, oSet)
    t1.join()
    AGC.stopActionGroup()
    cam.camera_close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
