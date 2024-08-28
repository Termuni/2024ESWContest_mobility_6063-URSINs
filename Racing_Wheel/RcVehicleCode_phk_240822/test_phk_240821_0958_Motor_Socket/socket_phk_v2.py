import socket

def start_server():
    host = '0.0.0.0'  # Bind to all interfaces
    port = 9091

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    return(s)

def while_server(s):
    #while True:
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    #while True:
    data = conn.recv(1024)
    if not data:
        print("No Date from Socket...")
        return
        #break
    #print("Received: ", repr(data))
    print("Received: ", data)
    print("Received: ", data.decode())  # TYPE = str
    #print("Received: ", int(data.decode()))
    
    #print(type(repr(data)))
    print(type(data))
    print(type(data.decode())) # TYPE = str
    #print(type(int(data.decode())))
    parts = data.decode().split('a')
    part_degree = int(parts[0])
    part_DcMotor = int(parts[1])
    print(part_degree)
    print(part_DcMotor)
    return(part_degree, part_DcMotor)
#start_server()

