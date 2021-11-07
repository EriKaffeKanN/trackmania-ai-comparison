import socket
import json
import selectors
import keyboard

f = open("../../../connection.config.json", "r")
config = json.loads(f.read())
f.close()

HOST = config["HOST"]
PORT = config["PORT"]

sel = selectors.DefaultSelector()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print("Listening on ", HOST, PORT)
s.setblocking(False)
sel.register(s, selectors.EVENT_READ, data=None)

# Adds data to the output which is then sent back to the client
def appendOutData(data, append):
    data += append
    return data

# Removes pieces of the output data in order to not send duplicates (all data is not always sent i a single cycle)
def capOutData(data, cap):
    outDataIndexZero = getOutDataIndex(data)
    data = data[:outDataIndexZero + 1] + data[outDataIndexZero + 1 + cap:]
    return data

def getOutDataIndex(data):
    outDataIndexZero = 0
    for i in range(len(data)):
        outDataIndexZero = i
        if data[i] == 0x7C:
            return outDataIndexZero
    print("Data not properly formatted, outDataIndex could not be found")
    return None

def getPortIndex(data):
    portIndex = 0
    for i in range(len(data)):
        portIndex = i
        if data[i] == 0x3A:
            return portIndex
    print("Data not properly formatted, portIndex could not be found")
    return None

def getAddrIndex(data):
    addrIndex = 0
    for i in range(len(data)):
        addrIndex = i
        if data[i] == 0x3B: #
            return addrIndex
    print("Data not properly formatted, addrIndex could not be found")
    return None

def getRequestData(data):
    return data[:getAddrIndex(data)]

def getAddr(data):
    print(data)
    return data[getAddrIndex(data)+1:getPortIndex(data)]

def getPort(data):
    return data[getPortIndex(data)+1:getOutDataIndex(data)]

def getOutData(data):
    return data[getOutDataIndex(data)+1:]

# Registers incoming traffic
def acceptWrapper(sock):
    conn, addr = sock.accept()
    print("Connected by ", addr)
    conn.setblocking(False)
    data = str(addr[0]).encode("UTF-8") + b':' + str(addr[1]).encode("UTF-8") + b';' + b'|'
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

# Handles requests / sent data from registered client sockets
def serviceConnection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data = appendOutData(data, recv_data) # TODO: Make this read request type as well
        else:
            print("Connection closed with ", getAddr(data))
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if getOutData(data):
            sent = sock.send(getOutData(data))
            data = capOutData(data, sent)

def runEventLoop():
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if keyboard.is_pressed("esc"):
                return
            if key.data is None:
                acceptWrapper(key.fileobj)
            else:
                serviceConnection(key, mask)
runEventLoop()