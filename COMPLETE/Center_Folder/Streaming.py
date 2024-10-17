import cv2
import threading
import os
import subprocess

import cv2


#region Streaming Client
# 스트리밍 URL 설정
def Get_Streaming_Pipeline(default_ip, default_port):
    pipeline = f"tcpclientsrc host={default_ip} port={default_port} ! queue max-size-buffers=1 ! multipartdemux ! jpegdec ! videoconvert ! appsink sync=false drop=true max-buffers=1"
    #pipeline = f"tcpclientsrc host={default_ip} port={default_port} ! queue max_size-buffers=1 ! multipartdemux ! jpegdec ! autovideosink sync=false"
    
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
        resized_frame = cv2.resize(frame, (640, 480))
        cv2.imshow('Raspberry Pi Stream', resized_frame)

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
        

#ppl = Get_Streaming_Pipeline()
def Run_New_Term():
    subprocess.Popen(['lxterminal','--command',f'sudo python3 /home/ursintcu/Desktop/LV3_Streaming.py'])

#vid_thread = threading.Thread(target = Run_New_Term, args=())
#vid_thread.start()
