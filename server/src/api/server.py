import socket

HOST = "127.0.0.1"
PORT = 5656

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    (conn, addr) = s.accept()
    with conn:
        print("Connection received from " + str(addr[0]) + " on port " + str(addr[1]))
        while True:
            data = conn.recv(1024) # Data buffer size is 1024
            if not data:
                print("Session ended with client " + str(addr))
                break
            conn.sendall(data)