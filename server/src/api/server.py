import socket
import json
import selectors
import types

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
            data.outdata = b'Running network lol'
    if mask & selectors.EVENT_WRITE:
        if data.outdata and (not (sock.fileno() == -1)):
            sent = sock.send(data.outdata)
            data.outdata = data.outdata[sent:]

def runEventLoop():
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                acceptWrapper(key.fileobj)
            else:
                serviceConnection(key, mask)

if __name__ == "__main__":
    runEventLoop()