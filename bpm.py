import time
import threading
from spidev import SpiDev

#ADC관련 SPI 초기화 통신
class MCP3208:
    _spi = None

    def __init__(self, bus=0, device=0):
        self.bus, self.device = bus, device
        if MCP3208._spi is None:
            MCP3208._spi = SpiDev()
            MCP3208._spi.open(self.bus, self.device)
            MCP3208._spi.max_speed_hz = 1000000  # 1MHz

    def read(self, channel=0):
        assert 0 <= channel <= 7, "Channel must be between 0 and 7"
        cmd1 = 6 | (channel >> 2)
        cmd2 = (channel & 3) << 6
        adc = MCP3208._spi.xfer2([cmd1, cmd2, 0])
        data = ((adc[1] & 15) << 8) + adc[2]
        return data

    def close(self):
        if MCP3208._spi:
            MCP3208._spi.close()
            MCP3208._spi = None

#low pass filter
def low_pass_filter(data, alpha, prev_filtered_data):
    return alpha * data + (1 - alpha) * prev_filtered_data

#bpm 계산법
def calculate_bpm(peaks, calibration_factor=60):
    if len(peaks) < 2:
        return 0
    intervals = [t - s for s, t in zip(peaks, peaks[1:])]
    avg_interval = sum(intervals) / len(intervals)
    bpm = calibration_factor / avg_interval if avg_interval > 0 else 0
    return int(bpm)


def monitor_sensor(sensor_type, channel, threshold, min_interval, alpha, calibration_factor):
    #변수 초기화
    adc = MCP3208()
    peaks = []
    count_bpm = 0
    avg_bpm = 0
    tot_bpm = 0
    filtered_bpm = 0  

    
    def read_and_process():
        #아날로그값 측정
        nonlocal count_bpm, avg_bpm, tot_bpm, filtered_bpm, peaks
        value = adc.read(channel)
        voltage = (value * 3.3) / 4096
        current_time = time.time()

        #임계값 넘어가면 피크 측정통해 bpm 계산
        if voltage > threshold:
            if len(peaks) == 0 or (current_time - peaks[-1]) > min_interval:
                peaks.append(current_time)
                if len(peaks) > 10:
                    peaks.pop(0)
                bpm = calculate_bpm(peaks, calibration_factor)
                filtered_bpm = low_pass_filter(bpm, alpha, filtered_bpm)
                
                if filtered_bpm != 0:
                    count_bpm += 1
                    tot_bpm += filtered_bpm
                    avg_bpm = tot_bpm / count_bpm

                print(f"{sensor_type} - BPM: {bpm:.2f}, Count: {count_bpm}, Avg BPM: {avg_bpm:.2f}")
                print(f"{sensor_type} - Filtered BPM: {filtered_bpm:.2f}")
        
        print(f"{sensor_type} Voltage: {voltage:.2f} V")

    try:
        while True:
            read_and_process()
            time.sleep(0.1)

    except KeyboardInterrupt:
        adc.close()
        print(f"{sensor_type} monitoring stopped.")


#캘리브레이션 요소 
    #ppg
ppg_channel = 0
ppg_threshold = 0.9
ppg_min_interval = 2.0
ppg_alpha = 0.75
ppg_calibration_factor = 240

    #ecg
ecg_channel = 1
ecg_threshold = 1.8
ecg_min_interval = 2.0
ecg_alpha = 0.75
ecg_calibration_factor = 240

# 쓰레딩으로 두개 센서 데이터 한 번에 수집 
ppg_thread = threading.Thread(target=monitor_sensor, args=("PPG", ppg_channel, ppg_threshold, ppg_min_interval, ppg_alpha, ppg_calibration_factor))
ecg_thread = threading.Thread(target=monitor_sensor, args=("ECG", ecg_channel, ecg_threshold, ecg_min_interval, ecg_alpha, ecg_calibration_factor))

# 스레딩 시작
ppg_thread.start()
ecg_thread.start()

# 두 쓰레기 끝날대 까지 기다리기
ppg_thread.join()
ecg_thread.join()