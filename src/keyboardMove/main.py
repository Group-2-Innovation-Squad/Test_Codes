import tty
import threading
import termios
import time
import sys
import os
import cv2

import hiwonder.Board as Board
import hiwonder.Camera as Camera
import hiwonder.ActionGroupControl as AGC
import hiwonder.yaml_handle as yaml_handle

running = True
yCoord = 1500
xCoord = 1500

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

def processInput():
    while running:
        ch = cv2.waitKey(0)
        if ch == b'w':
            print('Move Forward\r')
            AGC.runActionGroup('go_forward')
        elif ch == b'a':
            print('Turn Left\r')
            AGC.runActionGroup('turn_left')
        elif ch == b's':
            print('Move Backward\r')
            AGC.runActionGroup('back')
        elif ch == b'd':
            print('Turn Right\r')
            AGC.runActionGroup('turn_right')
        elif ch == b'q':
            running = False
            print('Quitting...\r')
        elif ch == b'h':
            print('Move Camera Left\r')
            xCoord -= 20
            xCoord = 500 if xCoord < 500 else xCoord
            Board.setPWMServoPulse(2, xCoord, 0.001)
        elif ch == b'j':
            print('Move Camera Down\r')
            yCoord -= 20
            yCoord = 1000 if yCoord < 1000 else yCoord
            Board.setPWMServoPulse(1, yCoord, 0.001)
        elif ch == b'k':
            print('Move Camera Up\r')
            yCoord += 20
            yCoord = 2000 if yCoord > 2000 else yCoord
            Board.setPWMServoPulse(1, yCoord, 0.001)
        elif ch == b'l':
            print('Move Camera Right\r')
            xCoord += 20
            xCoord = 2500 if xCoord > 2500 else xCoord
            Board.setPWMServoPulse(2, xCoord, 0.001)

def runningWindow(cam):
    while running:
        ret, frame = cam.read()
        cv2.imshow('TonyPi Camera', frame)

def main():
    fd, oSet = enterRaw()
    print(instructions)
    ch = ''
    os.set_blocking(sys.stdin.fileno(), False)
    cam = initCamera()

    t1 = threading.Thread(target=runningWindow, args=(cam,))
    t2 = threading.Thread(target=processInput)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
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
    exitRaw(fd, oSet)
    AGC.stopActionGroup()

if __name__ == '__main__':
    main()
