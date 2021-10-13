# Imports
import imageprocessingmodule as IMP
import keyboard
import math
import socket

HOST = "127.0.0.1"
PORT = 5656

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hej varld osv')
    data = s.recv(1024)
print("Server response: ", repr(data))

while True:
    if keyboard.is_pressed("home"):
        while not keyboard.is_pressed("end"):
            IMP.getLineLengths(IMP.getProcessedScreenshot(), 0, 0, 0)
        print("Done recording")
    if keyboard.is_pressed("o"):
        img = IMP.getProcessedScreenshot()
        lines = IMP.getLineLengths(img, math.pi/12, math.pi-(math.pi/12), 5*math.pi/(6*12))
        print("Line values:")
        for l in lines:
            print(l)
        IMP.visualizeLines(img, lines, math.pi/12, math.pi-(math.pi/12),  5*math.pi/(6*12))
    if keyboard.is_pressed("esc"):
        break
