import cv2
import threading
import os
import subprocess
import sys
import cv2


#region Streaming Client
# 스트리밍 URL 설정
def Get_Streaming_Pipeline(default_ip = '10.211.173.3', default_port = 8080):
    pipeline = f"tcpclientsrc host={default_ip} port={default_port} ! multipartdemux ! jpegdec ! videoconvert ! appsink sync=false"
    return pipeline

# 비디오 캡처 객체 생성
def Get_VideoCapture_Variable(pipeline):
    vd_cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    return vd_cap

def Get_Streaming(cap):
    if not cap.isOpened():
        print("Error: Unable to open stream")
        return
    # 비디오 스트리밍 재생
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to retrieve frame")
            break
        
        cv2.imshow('Raspberry Pi Stream', frame)

        # 'q'를 누르면 스트리밍 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def Thread_Streaming(cap):
    try:
        # 쓰레딩으로 두개 센서 데이터 한 번에 수집
        stream_thread = threading.Thread(
            target=Get_Streaming, 
            args=(cap, ))

        # 스레딩 시작
        stream_thread.start()
    except:
        cap.release()
        cv2.destroyAllWindows()
        

streaming_ppl_lv3 = Get_Streaming_Pipeline('10.211.173.3', 9090)
vd_cap_lv3 = Get_VideoCapture_Variable(streaming_ppl_lv3)

Get_Streaming(vd_cap_lv3)
