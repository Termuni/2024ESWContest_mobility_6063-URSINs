import socket

def start_server():
    host = '0.0.0.0'  # Bind to all interfaces
    port = 9090

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    return(conn)

def while_server(conn):
    #while True:
    #while True:
    print("while_server...line test1")
    data = conn.recv(1024)
    print("while_server...line test2")    
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
    
    #==============================
    #1. split 'a' (get three parts)
    #2. cut behind 'z'
    #ex. 222a42a12z41-12   ->  222, 42, 12  
    input_str = data.decode()
    index_of_e = input_str.find('z')
    if index_of_e != -1:
        input_str = input_str[:index_of_e]
    parts = input_str.split('a',2)
    while len(parts) < 3:
        parts.append('0')
    
    part_Handle = int(parts[0])
    part_Accel = int(parts[1])
    part_Brake = int(parts[2])
    #==============================
    
    print(part_Handle)
    print(part_Accel)
    print(part_Brake)
    return(part_Handle, part_Accel, part_Brake)
#start_server()


