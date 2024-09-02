import TCP_IP_Communication as com

if __name__ == "__main__":
    conn = com.Init_Socket(HOST= '10.211.173.2')
    while True:
        com.Connect_Socket(conn)