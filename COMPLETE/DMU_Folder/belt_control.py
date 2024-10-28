import gpiozero
import threading
import time

# GPIO 핀 번호 설정 (BCM 기준)
LED_PIN = 12
BELT_PUT_PIN = 26  # 스위치가 연결된 핀
CLK_PIN = 17  # 로터리 엔코더 CLK 핀
DT_PIN = 18   # 로터리 엔코더 DT 핀

# 글로벌 변수
Lv_Belt = 0  # Lv_Belt 초기값 0
count = 0    # 로터리 인코더 카운터
last_change_time = time.time()  # 마지막 변화 시간
last_clk_state = None  # 로터리 엔코더 CLK 핀의 마지막 상태
thread = None

# GPIO 리셋


# GPIO 설정
led = gpiozero.LED(LED_PIN)
belt_put_switch = gpiozero.Button(BELT_PUT_PIN)
clk = gpiozero.Button(CLK_PIN)
dt = gpiozero.Button(DT_PIN)

# LED를 깜빡이는 함수 (별도의 스레드에서 실행)
def blink_led(led, stop_event):
    while not stop_event.is_set():
        led.on()  # LED ON
        time.sleep(0.3)
        led.off()  # LED OFF
        time.sleep(0.3)

# 로터리 인코더 카운트 처리 함수
def handle_encoder(clk, dt):
    global Lv_Belt, count, last_clk_state, last_change_time

    current_clk_state = clk.is_pressed
    dt_state = dt.is_pressed

    if last_clk_state is None:
        last_clk_state = current_clk_state  # 첫 상태 설정

    if last_clk_state == 0 and current_clk_state == 1:
        if dt_state == 0:
            count += 1
            print(f"Clockwise. Count: {count}")
        else:
            count -= 1
            print(f"Counter-Clockwise. Count: {count}")

        last_change_time = time.time()

        if count >= 20 or count <= -20:
            Lv_Belt = 2
            print("Lv_Belt set to 2")
        elif Lv_Belt == 2 and -10 <= count <= 10:
            Lv_Belt = 1
            print("Lv_Belt reset to 1")    

    last_clk_state = current_clk_state

# LED 제어 및 로터리 인코더 상태 관리 함수
def control_lv_belt(belt_put_switch, led, clk, dt, stop_event):
    global Lv_Belt, count, last_change_time, thread

    if belt_put_switch.is_pressed:
        Lv_Belt = 0
        count = 0
        stop_event.set()
        if thread is not None:
            thread.join()
        led.on()
    elif not belt_put_switch.is_pressed and Lv_Belt == 0:
        Lv_Belt = 1
        print("Lv_Belt set to 1")
    elif Lv_Belt == 1:
        stop_event.set()
        if thread is not None:
            thread.join()
        led.off()
        handle_encoder(clk, dt)
        if time.time() - last_change_time > 5:
            count = 0
            print("No change for 5 seconds. Count reset to 0.")
            last_change_time = time.time()
    elif Lv_Belt == 2:
        if thread is None or not thread.is_alive():
            stop_event.clear()
            thread = threading.Thread(target=blink_led, args=(led, stop_event))
            thread.start()
        handle_encoder(clk, dt)

    return Lv_Belt  # Lv_Belt 값 반환

# 벨트 제어 함수 실행
def run_belt_control(stop_event):
    try:
        while True:
            Lv_Belt_value = control_lv_belt(belt_put_switch, led, clk, dt, stop_event)
            time.sleep(0.001)
    except KeyboardInterrupt:
        stop_event.set()
    return Lv_Belt_value


# 벨트 제어를 스레드로 실행하는 함수
def belt_control_thread(stop_event):
    Lv_Belt_value = run_belt_control(stop_event)
    return Lv_Belt_value

def Function_Belt():
    stop_event = threading.Event()

    # 벨트 제어 스레드 실행
    belt_thread = threading.Thread(target=belt_control_thread, args=(stop_event,))
    belt_thread.start()

    try:
        while True:
            # Lv_Belt 값을 메인 루프에서 사용
            Lv_Belt_value = Lv_Belt  # belt_control 모듈에서 Lv_Belt 값을 가져옴
            print(f"Main loop Lv_Belt: {Lv_Belt_value}")
            time.sleep(1)  # 1초마다 상태 확인
    except KeyboardInterrupt:
        print("Main program interrupted.")
        led.close()
        belt_put_switch.close()
        clk.close()
        dt.close()
        stop_event.set()  # 벨트 제어 스레드 종료 요청
        belt_thread.join()  # 벨트 제어 스레드 종료 대기

def Thread_Belt():
    belt_th = threading.Thread(target=Function_Belt, args=())
    belt_th.start()

def Get_Lv_Belt():
    global Lv_Belt
    return Lv_Belt

