# Imports
from keyboard import on_release
from imageprocessingmodule import ImageProcessingModule as IPM
from pynput import keyboard
import math
import socket
import json

f = open("../../connection.config.json")
config = json.loads(f.read())
f.close()

HOST = config["HOST"]
PORT = config["PORT"]

def onPress(key):
    if key == keyboard.Key.home:
        img = IPM.getProcessedScreenshot()
        fLines = IPM.getLineLengths(img, math.pi/11, math.pi-(math.pi/11), 5*math.pi/(6*10))
        fNormalisedLines = map(lambda l: l * 255.0/1445.0, fLines)
        iLines = map(math.floor, fNormalisedLines) # list[float] -> list[int]
        bLines = bytes(iLines) # list[int] -> bytes
        s.sendall(b'runNetwork|' + bLines)
        data = s.recv(1024)
        print("Server response: ", repr(data))
    elif key == keyboard.Key.esc:
        return False # Terminates program

def onRelease(key):
    pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    """while True:
        # Continuous recording
        if keyboard.is_pressed("home"):
            while not keyboard.is_pressed("end"):
                img = IPM.getProcessedScreenshot()
                IPM.getLineLengths(img, math.pi/12, math.pi-(math.pi/12), 5*math.pi/(6*11))
            print("Done recording")
        # Single screenshots (for debug purposes)
        elif keyboard.is_pressed("o"):
            img = IPM.getProcessedScreenshot()
            fLines = IPM.getLineLengths(img, math.pi/11, math.pi-(math.pi/11), 5*math.pi/(6*10))
            fNormalisedLines = map(lambda l: l * 255.0/1445.0, fLines)
            iLines = map(math.floor, fNormalisedLines) # list[float] -> list[int]
            bLines = bytes(iLines) # list[int] -> bytes
            s.sendall(b'runNetwork|' + bLines)
            data = s.recv(1024)
            print("Server response: ", repr(data))
            #IPM.visualizeLines(img, fLines, math.pi/11, math.pi-(math.pi/11),  5*math.pi/(6*10))
        elif keyboard.is_pressed("esc"):
            break"""
    with keyboard.Listener(
            on_press=onPress,
            on_release=onRelease) as listener:
        listener.join()
