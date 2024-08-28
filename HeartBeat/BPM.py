'''
Functions That Could Be Used
1. Init_BPM() => Setting Values for Global
2. Get_BPM_Data(
    ppg_ch = 0, ppg_thd = 0.9, ppg_min_intv = 2.0, ppg_A = 0.75, ppg_cal_fact = 240,
    ecg_ch = 1, ecg_thd = 1.8, ecg_min_intv = 2.0, ecg_A = 0.75, ecg_cal_fact = 240)
    => Getting BPM Data by setting each values
'''
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

    def Read(self, channel=0):
        assert 0 <= channel <= 7, "Channel must be between 0 and 7"
        cmd1 = 6 | (channel >> 2)
        cmd2 = (channel & 3) << 6
        adc = MCP3208._spi.xfer2([cmd1, cmd2, 0])
        data = ((adc[1] & 15) << 8) + adc[2]
        return data

    def Close(self):
        if MCP3208._spi:
            MCP3208._spi.close()
            MCP3208._spi = None


#low pass filter
def Low_Pass_Filter(data, alpha, prev_filtered_data):
    return alpha * data + (1 - alpha) * prev_filtered_data


#bpm 계산법
def Calculate_BPM(peaks, calibration_factor=60):
    if len(peaks) < 2:
        return 0
    intervals = [t - s for s, t in zip(peaks, peaks[1:])]
    avg_interval = sum(intervals) / len(intervals)
    bpm = calibration_factor / avg_interval if avg_interval > 0 else 0
    return int(bpm)


#Init BPM Values
def Init_BPM():
    #변수 초기화
    global p_adc, e_adc
    global ppg_peaks, ppg_count_bpm, ppg_avg_bpm, ppg_tot_bpm, ppg_filtered_bpm
    global ecg_peaks, ecg_count_bpm, ecg_avg_bpm, ecg_tot_bpm, ecg_filtered_bpm
    
    if (isinstance(p_adc, MCP3208) == False):
        p_adc = MCP3208()
        ppg_peaks = []
        ppg_count_bpm = 0
        ppg_avg_bpm = 0
        ppg_tot_bpm = 0
        ppg_filtered_bpm = 0
        
    if (isinstance(e_adc, MCP3208) == False):
        e_adc = MCP3208()
        ecg_peaks = []
        ecg_count_bpm = 0
        ecg_avg_bpm = 0
        ecg_tot_bpm = 0
        ecg_filtered_bpm = 0


# Getting Value : Peak, BPM
def Get_Values_For_Monitor_Sensor(sensor_type, channel):
    global p_adc, ppg_peaks, ppg_count_bpm, ppg_avg_bpm, ppg_tot_bpm, ppg_filtered_bpm
    global e_adc, ecg_peaks, ecg_count_bpm, ecg_avg_bpm, ecg_tot_bpm, ecg_filtered_bpm
    
    if sensor_type == "PPG":
        value = p_adc.Read(channel)
        return value, ppg_peaks, ppg_count_bpm, ppg_avg_bpm, ppg_tot_bpm, ppg_filtered_bpm
    
    elif sensor_type == "ECG":
        value = e_adc.Read(channel)
        return ecg_peaks, ecg_count_bpm, ecg_avg_bpm, ecg_tot_bpm, ecg_filtered_bpm
    
    
# Setting Value : Peak, BPM
def Set_Values_After_Monirot_Sensor(sensor_type, peaks, count_bpm, avg_bpm, tot_bpm, filtered_bpm):
    
    global ppg_peaks, ppg_count_bpm, ppg_avg_bpm, ppg_tot_bpm, ppg_filtered_bpm
    global ecg_peaks, ecg_count_bpm, ecg_avg_bpm, ecg_tot_bpm, ecg_filtered_bpm
    
    if sensor_type == "PPG":
        ppg_peaks = peaks
        ppg_count_bpm = count_bpm
        ppg_avg_bpm = avg_bpm
        ppg_tot_bpm = tot_bpm
        ppg_filtered_bpm = filtered_bpm
    
    elif sensor_type == "ECG":
        ecg_peaks = peaks
        ecg_count_bpm = count_bpm
        ecg_avg_bpm = avg_bpm
        ecg_tot_bpm = tot_bpm
        ecg_filtered_bpm = filtered_bpm


def Monitor_Sensor(sensor_type, channel, threshold, min_interval, alpha, calibration_factor):
    # 아날로그값 측정
    value, peaks, count_bpm, avg_bpm, tot_bpm, filtered_bpm = Get_Values_For_Monitor_Sensor(sensor_type, channel)
    voltage = (value * 3.3) / 4096
    current_time = time.time()

    #임계값 넘어가면 피크 측정통해 bpm 계산
    if voltage > threshold:
        if len(peaks) == 0 or (current_time - peaks[-1]) > min_interval:
            peaks.append(current_time)
            if len(peaks) > 10:
                peaks.pop(0)
            bpm = Calculate_BPM(peaks, calibration_factor)
            filtered_bpm = Low_Pass_Filter(bpm, alpha, filtered_bpm)
            
            if filtered_bpm != 0:
                count_bpm += 1
                tot_bpm += filtered_bpm
                avg_bpm = tot_bpm / count_bpm

    Set_Values_After_Monirot_Sensor(sensor_type, peaks, count_bpm, avg_bpm, tot_bpm, filtered_bpm)



def Get_BPM_Data(
    ppg_ch = 0, ppg_thd = 0.9, ppg_min_intv = 2.0, ppg_A = 0.75, ppg_cal_fact = 240,
    ecg_ch = 1, ecg_thd = 1.8, ecg_min_intv = 2.0, ecg_A = 0.75, ecg_cal_fact = 240):
    '''
    BPM 데이터를 받아오는 함수입니다
    Init_BPM 함수가 실행되어 있지 않다면, 실행되지 않습니다.
    (함수 내부에서 Init_BPM을 진행하나, 권장하지 않습니다)
    
    Args : 캘리브레이션 요소, ppg, ecg 각각 존재
        channel = _ch
        threshold = _thd
        minimum_interval = min_intv
        alpha = _A
        calibration_factor = cal_fact
    
    Returns : PPG and ECG Values
    '''
    #If You want, You can use these values
    global p_adc, e_adc
    global ppg_peaks, ppg_count_bpm, ppg_avg_bpm, ppg_tot_bpm, ppg_filtered_bpm
    global ecg_peaks, ecg_count_bpm, ecg_avg_bpm, ecg_tot_bpm, ecg_filtered_bpm
    
    if (isinstance(p_adc, MCP3208) == False) or (isinstance(e_adc, MCP3208) == False):
        Init_BPM()
        return 0, 0
    
    try:        
        # 쓰레딩으로 두개 센서 데이터 한 번에 수집 
        ppg_thread = threading.Thread(
            target=Monitor_Sensor, 
            args=("PPG", ppg_ch, ppg_thd, ppg_min_intv, ppg_A, ppg_cal_fact))

        ecg_thread = threading.Thread(
            target=Monitor_Sensor, 
            args=("ECG", ecg_ch, ecg_thd, ecg_min_intv, ecg_A, ecg_cal_fact))

        # 스레딩 시작
        ppg_thread.start()
        ecg_thread.start()

        # 두 스레드 끝날대 까지 기다리기
        ppg_thread.join()
        ecg_thread.join()
        
    except KeyboardInterrupt:
        p_adc.Close()
        e_adc.Close()
        print("monitoring stopped")
    

    #return ppg_avg_bpm, ecg_avg_bpm