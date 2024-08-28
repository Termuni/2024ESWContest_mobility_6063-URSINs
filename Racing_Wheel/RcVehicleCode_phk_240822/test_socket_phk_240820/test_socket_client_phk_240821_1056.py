import socket

def send_data_str():
    host = '192.168.0.8'
    port = 9091

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        print("test1")
        input_int1 = int(input("Enter a Number1 (int): "))
        input_int2 = int(input("Enter a Number2 (int): "))
        result_str = str(input_int1) +'a'+ str(input_int2)
        
        s.sendall(result_str.encode())
        

try:
    send_data_str()

except KeyboardInterrupt:
    print("Stopped by User")

