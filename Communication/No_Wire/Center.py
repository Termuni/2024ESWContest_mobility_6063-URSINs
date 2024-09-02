import TCP_IP_Communication as com

if __name__ == "__main__":
    conn = com.Init_Socket()
    while True:
        com.Connect_Socket(conn)