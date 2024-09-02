import TCP_IP_Communication as com

if __name__ == "__main__":
    conn = com.Init_Socket(HOST= '10.211.173.2')
    while True:
        data = com.Receive_Socket(conn)
        decoded_data = data.decode()
        if (decoded_data == 2):
            com.Send_Socket(conn, input("Value Input :"))
        elif decoded_data == 9:
            print("COMMUNICATION END")
            break
    
    com.Close_Socket(conn)