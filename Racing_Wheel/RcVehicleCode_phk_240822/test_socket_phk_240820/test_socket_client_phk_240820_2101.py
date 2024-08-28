import socket

def send_data_str():
    host = '192.168.0.8'
    port = 9090

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        print("test1")
        user_input = input("Enter a message1: ")
        s.sendall(user_input.encode())
        
def send_data_int():
    host = '192.168.0.8'
    port = 9090

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        print("test1")
        user_input1 = int(input("Enter a message1: "))
        user_input2 = int(input("Enter a message2: "))
        list_input = [user_input1, user_input2]
        s.sendall(bytes(list_input))

try:
    send_data_str()
    #send_data_int()
except KeyboardInterrupt:
    print("Stopped by User")
