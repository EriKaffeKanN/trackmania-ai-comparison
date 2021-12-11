import socket
import json
import selectors
import types
import sys
import keras
import numpy as np

sys.path.append("../")
from billyrocket.billyrocket import BillyRocket

# Load AI
br = BillyRocket(keras.models.load_model("../billyrocket/state"))
gameState = {"velocity": 0}

# Connection settings
f = open("../../../connection.config.json", "r")
config = json.loads(f.read())
f.close()

HOST = config["HOST"]
PORT = config["PORT"]

# Fix backup
f1 = open("../billyrocket/training-data-backup.json", 'w')
f2 = open("../billyrocket/training-data.json", 'r')
tmpDat = json.load(f2)
f1.write(json.dumps(tmpDat))
f1.close()
f2.close()

# Setup socket
sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print("Listening on ", HOST, PORT)
s.setblocking(False)
sel.register(s, selectors.EVENT_READ, data=None)

# Registers incoming traffic
def acceptWrapper(sock):
    conn, addr = sock.accept()
    print("Connected by ", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, request=b'', indata=b'', outdata=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

# Handles requests / sent data from registered client sockets
def serviceConnection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            parsedRecvData = recv_data.split(b'|')
            data.request = parsedRecvData[0]
            data.indata = parsedRecvData[1]
        else:
            print("Connection closed with ", data.addr[0])
            sel.unregister(sock)
            sock.close()
        if data.request == b'runNetwork':
            aBrInput = list(data.indata)
            aBrInput.append(gameState["velocity"])
            brInput = np.array([aBrInput], dtype=np.float32)
            outputNeurons = br.runNetwork(brInput)
            prediction = np.argmax(outputNeurons)
            data.outdata = str(prediction).encode("UTF-8")
        # Thank god strings in AngelScripts are the same as C strings
        elif data.request == b'trainNetwork':
            # data.indata will look like this: [l0, l1, ..., l10, GAS, BRAKE, LEFT, RIGHT]
            # where GAS, BRAKE, LEFT, RIGHT are all C booleans
            lineLengths = list(data.indata[:11])
            buttonsPressed = list(data.indata[11:])
            
            trainingData = None
            with open("../billyrocket/training-data.json", 'r') as f:
                trainingData = json.load(f)
                trainingData["TrainingExamples"].append({
                    "LineLengths": lineLengths,
                    "GameState": [gameState["velocity"]],
                    "KeyboardInput": buttonsPressed
                    })
            with open("../billyrocket/training-data.json", 'w') as f:
                f.write(json.dumps(trainingData))
        elif data.request == b'updateGameState':
            gameState["velocity"] = float(data.indata)
    if mask & selectors.EVENT_WRITE:
        if data.outdata and (not (sock.fileno() == -1)):
            sent = sock.send(data.outdata)
            data.outdata = data.outdata[sent:]

def main():
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                acceptWrapper(key.fileobj)
            else:
                serviceConnection(key, mask)

if __name__ == "__main__":
    main()