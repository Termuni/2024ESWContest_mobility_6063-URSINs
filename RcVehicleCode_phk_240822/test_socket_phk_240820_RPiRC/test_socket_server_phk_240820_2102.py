import socket

def start_server():
    host = '0.0.0.0'  # Bind to all interfaces
    port = 9090

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Received: ", repr(data))
            print(type(repr(data)))

start_server()