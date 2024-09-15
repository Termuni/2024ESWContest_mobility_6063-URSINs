import CCU_UartMaster_240904_1101 as uart #import init_uart, master_communication, close_uart
import time

ser = uart.init_uart()

try:
    while True:
        # 데이터가 없으면 None, 있으면 실제 데이터를 입력
        data_to_send = None  # 혹은 실제 데이터를 입력 (예: "Temperature: 25C")
        response = uart.master_communication(ser, data_to_send)
        print(f"Response from Slave: {response}")
        time.sleep(2)  # 2초 간격으로 데이터 송수신
except KeyboardInterrupt:
    uart.close_uart(ser)