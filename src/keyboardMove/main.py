import tty
import termios
import time
import sys
import os

import hiwonder.Board as Board
import hiwonder.Camera as Camera
import hiwonder.ActionGroupControl as AGC

instructions = '''Controls:\r
w: Move Forward\r
a: Turn Left\r
s: Move Backward\r
d: Turn Right\r
q: Quit\r'''

def initCamera():
    Board.setPWMServoPulse(1, 1500, 500)
    Board.setPWMServoPulse(2, 1500, 500)

def enterRaw():
    fd = sys.stdin.fileno()
    oSettings = termios.tcgetattr(fd)
    tty.setraw(fd)
    return fd, oSettings

def exitRaw(fd, oSet):
    termios.tcsetattr(fd, termios.TCSADRAIN, oSet)

def main():
    fd, oSet = enterRaw()
    print(instructions)
    ch = ''
    os.set_blocking(sys.stdin.fileno(), False)
    initCamera()
    yCoord = 1500
    xCoord = 1500
    while ch != 'q':
        try:
            ch = chr(os.read(sys.stdin.fileno(), 1024)[-1])
            if ch == 'w':
                print('Move Forward\r')
                AGC.runActionGroup('go_forward')
            elif ch == 'a':
                print('Turn Left\r')
                AGC.runActionGroup('turn_left')
            elif ch == 's':
                print('Move Backward\r')
                AGC.runActionGroup('back')
            elif ch == 'd':
                print('Turn Right\r')
                AGC.runActionGroup('turn_right')
            elif ch == 'q':
                print('Quitting...\r')
            elif ch == 'h':
                print('Move Camera Left\r')
                xCoord -= 20
                xCoord = 500 if xCoord < 500 else xCoord
                Board.setPWMServoPulse(2, xCoord, 0.001)
            elif ch == 'j':
                print('Move Camera Down\r')
                yCoord -= 20
                yCoord = 1000 if yCoord < 1000 else yCoord
                Board.setPWMServoPulse(1, yCoord, 0.001)
            elif ch == 'k':
                print('Move Camera Up\r')
                yCoord += 20
                yCoord = 2000 if yCoord > 2000 else yCoord
                Board.setPWMServoPulse(1, yCoord, 0.001)
            elif ch == 'l':
                print('Move Camera Right\r')
                xCoord += 20
                xCoord = 2500 if xCoord < 2500 else xCoord
                Board.setPWMServoPulse(2, xCoord, 0.001)
        except:
            continue
    exitRaw(fd, oSet)
    AGC.stopActionGroup()

if __name__ == '__main__':
    main()
