import tty
import termios
import time
import sys
import os
import hiwonder.ActionGroupControl as AGC

instructions = '''Controls:\r
w: Move Forward\r
a: Turn Left\r
s: Move Backward\r
d: Turn Right\r
q: Quit\r'''

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
        except:
            continue
    exitRaw(fd, oSet)
    AGC.stopActionGroup()

if __name__ == '__main__':
    main()
