import TCP_IP_Communication as com

if __name__ == "__main__":
    conn = com.Init_Socket()
    while True:
        data = com.Receive_Socket(conn)
        if (data == 9):
            break
        com.Send_Socket(conn, input("Enter Data : "))
        
    com.Close_Socket(conn)