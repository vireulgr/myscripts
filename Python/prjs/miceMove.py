#!/usr/bin/python

import time
import win32api, win32con
import sys

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def move( fromx, fromy, tox, toy ):
    steps = 10
    for step in range(steps):
        alpha = float(step)/steps
        ptx = fromx + (tox-fromx)*(alpha)
        pty = fromy + (toy-fromy)*(alpha)
        #win32api.SetCursorPos( (ptx, pty) )
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 
            int(ptx/SCREEN_WIDTH*65535.0), int(pty/SCREEN_HEIGHT*65535.0))
        time.sleep( 0.2 )
    pass

def main( argv ):
    move( 100, 100, 500, 500 )
    pass

if __name__ == "__main__":
    main( sys.argv )
