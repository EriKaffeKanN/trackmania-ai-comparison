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

"""with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        if keyboard.is_pressed("q"):
            s.sendall(b'runNetwork' + b'|' + b'Hej varld osv')
            data = s.recv(1024)
            print("Server response: ", repr(data))
        if keyboard.is_pressed("esc"):
            break"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        if keyboard.is_pressed("home"):
            while not keyboard.is_pressed("end"):
                img = IPM.getProcessedScreenshot()
                IPM.getLineLengths(img, math.pi/12, math.pi-(math.pi/12), 5*math.pi/(6*11))
            print("Done recording")
        if keyboard.is_pressed("o"):
            img = IPM.getProcessedScreenshot()
            lines = IPM.getLineLengths(img, math.pi/12, math.pi-(math.pi/12), 5*math.pi/(6*11))
            iLines = map(math.floor, lines) # list[float] -> list[int]
            bLines = bytes(iLines) # list[int] -> bytes
            s.sendall(b'runNetwork|' + bLines)
            data = s.recv(1024)
            print("Server response: ", repr(data))
            #IPM.visualizeLines(img, lines, math.pi/12, math.pi-(math.pi/12),  5*math.pi/(6*11))
        if keyboard.is_pressed("esc"):
            break
