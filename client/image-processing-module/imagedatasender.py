# Imports
import imageprocessingmodule as IMP
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
    s.sendall(b'Hej varld osv')
    data = s.recv(1024)
print("Server response: ", repr(data))

while True:
    if keyboard.is_pressed("home"):
        while not keyboard.is_pressed("end"):
            img = IMP.getProcessedScreenshot()
            IMP.getLineLengths(img, math.pi/12, math.pi-(math.pi/12), 5*math.pi/(6*11))
        print("Done recording")
    if keyboard.is_pressed("o"):
        lines = IMP.getLineLengths(img, math.pi/12, math.pi-(math.pi/12), 5*math.pi/(6*11))
        print("Line values:")
        for l in lines:
            print(l)
        IMP.visualizeLines(img, lines, math.pi/12, math.pi-(math.pi/12),  5*math.pi/(6*11))
    if keyboard.is_pressed("esc"):
        break
