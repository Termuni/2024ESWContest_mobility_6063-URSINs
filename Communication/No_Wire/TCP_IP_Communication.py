import socket

def Init_Socket(HOST = '0.0.0.0', PORT = 9091):
    
    # HOST = '0.0.0.0'  # 서버는 모든 IP에서 접속을 허용합니다.
    # PORT = 9091  # 클라이언트와 동일한 포트 사용
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print('Server listening...')

    conn, addr = s.accept()
    print('Connected by', addr)
    return conn

def Receive_Socket(conn):
    data = conn.recv(1024)
    print("Client : ", data.decode())
    return data

def Send_Socket(conn, data = "a"):
    conn.sendall(data.encode())

def Close_Socket(conn):
    conn.close()