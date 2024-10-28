import socket

def Init_Server_Socket(HOST = '0.0.0.0', PORT = 9091):
    '''
    # HOST = '0.0.0.0'  # 서버는 모든 IP에서 접속을 허용합니다.
    # PORT = 9091  # 클라이언트와 동일한 포트 사용
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    s.setblocking(False)
    print('Server listening...')

    conn, addr = s.accept()
    print('Connected by', addr)
    return conn


def Init_Client_Socket(HOST = '0.0.0.0', PORT = 9091):
    '''
    # HOST = '0.0.0.0'  # 클라이언트는 해당되는 IP에서 접속을 시도합니다.
    # PORT = 9091  # 클라이언트와 동일한 포트 사용
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    #s.setblocking(False)
    return s

def Receive_Socket(conn):
    data = conn.recv(1024)
    #print("Client : ", data.decode())
    return data

def Send_Socket(conn, data = "a"):
    conn.sendall(data.encode())

def Close_Socket(conn):
    conn.close()
