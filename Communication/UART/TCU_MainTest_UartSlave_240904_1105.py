from TCU_UartSlave_240904_1102 import init_uart, slave_communication, close_uart
import time

ser = init_uart()

try:
    while True:
        # �����Ͱ� ������ None, ������ ���� �����͸� �Է�
        data_to_send = None  # Ȥ�� ���� �����͸� �Է� (��: "Humidity: 60%")
        received_message = slave_communication(ser, data_to_send)
        print(f"Message from Master: {received_message}")
        time.sleep(2)  # 2�� �������� ������ �ۼ���
except KeyboardInterrupt:
    close_uart(ser)