# Imports
from keyboard import on_release
from imageprocessingmodule import ImageProcessingModule as IPM
from pynput import keyboard as pp
from pynput.keyboard import Key, Controller
import pyautogui
import math
import socket
import json

y = [0, 0, 0, 0] # W, SPACE, A, D

# Connection settings
f = open("../../connection.config.json")
config = json.loads(f.read())
f.close()

HOST = config["HOST"]
PORT = config["PORT"]

def bGetLineLengths() -> bytes:
    img = IPM.getProcessedScreenshot()
    fLines = IPM.getLineLengths(img, math.pi/11, math.pi-(math.pi/11), 5*math.pi/(6*10))
    fNormalisedLines = map(lambda l: l * 255.0/1445.0, fLines)
    iLines = map(math.floor, fNormalisedLines) # list[float] -> list[int]
    bLines = bytes(iLines) # list[int] -> bytes
    return bLines

def onPress(key):
    global y

    try:
        if key.char == 'w':
            y[0] = 1
        if key.char == 'a':
            y[2] = 1
        if key.char == 'd':
            y[3] = 1
        if key.char == 'j':
            print(y)
    except AttributeError:
        if key == Key.space:
            y[1] = 1
        if key == Key.home:
            while True:
                lines = bGetLineLengths()
                s.sendall(b'runNetwork|' + lines)
                data = s.recv(1024)
                print(data)
                if data == b'0':
                    pyautogui.press('w')
                    pyautogui.keyUp('a')
                    pyautogui.keyUp('d')
                    pyautogui.keyUp('space')
                elif data == b'1':
                    pyautogui.keyUp('w')
                    pyautogui.keyUp('a')
                    pyautogui.keyUp('d')
                    pyautogui.press('space')
                elif data == b'2':
                    pyautogui.keyUp('w')
                    pyautogui.press('a')
                    pyautogui.keyUp('d')
                    pyautogui.keyUp('space')
                elif data == b'3':
                    pyautogui.keyUp('w')
                    pyautogui.keyUp('a')
                    pyautogui.press('d')
                    pyautogui.keyUp('space')
        elif key == Key.end:
            lines = bGetLineLengths()
            s.sendall(b'trainNetwork|' + lines + bytes(y))
        elif key == Key.esc:
            return False # Terminates program

def onRelease(key):
    global y
    try:
        if key.char == 'w':
            y[0] = 0
        if key.char == 'a':
            y[2] = 0
        if key.char == 'd':
            y[3] = 0
    except AttributeError:
        if key == Key.space:
            y[1] = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    with pp.Listener(
            on_press=onPress,
            on_release=onRelease) as listener:
        listener.join()
