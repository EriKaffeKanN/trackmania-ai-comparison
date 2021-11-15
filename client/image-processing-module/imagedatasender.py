# Imports
from imageprocessingmodule import ImageProcessingModule as IPM
import keyboard
import math
import socket
import json

f = open("../../connection.config.json")
config = json.loads(f.read())
f.close()

HOST = config["HOST"]
PORT = config["PORT"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        # Continuous recording
        if keyboard.is_pressed("home"):
            while not keyboard.is_pressed("end"):
                img = IPM.getProcessedScreenshot()
                IPM.getLineLengths(img, math.pi/12, math.pi-(math.pi/12), 5*math.pi/(6*11))
            print("Done recording")
        # Single screenshots (for debug purposes)
        if keyboard.is_pressed("o"):
            img = IPM.getProcessedScreenshot()
            fLines = IPM.getLineLengths(img, math.pi/11, math.pi-(math.pi/11), 5*math.pi/(6*10))
            fNormalisedLines = map(lambda l: l * 255.0/1445.0, fLines)
            iLines = map(math.floor, fNormalisedLines) # list[float] -> list[int]
            bLines = bytes(iLines) # list[int] -> bytes
            s.sendall(b'runNetwork|' + bLines)
            data = s.recv(1024)
            print("Server response: ", repr(data))
            #IPM.visualizeLines(img, fLines, math.pi/11, math.pi-(math.pi/11),  5*math.pi/(6*10))
        if keyboard.is_pressed("esc"):
            break
