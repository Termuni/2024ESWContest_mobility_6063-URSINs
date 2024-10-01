import cv2
import threading
import os
import subprocess

#region Streaming Client
# 스트리밍 URL 설정
def Get_Streaming_URL(default_port = 8080):
    url = f"http://10.211.173.3:{default_port}/stream/video.mjpeg"
    return url

# 비디오 캡처 객체 생성
def Get_VideoCapture_Variable(url):
    vd_cap = cv2.VideoCapture(url)
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
        
        
test_url = Get_Streaming_URL()
test_cap = Get_VideoCapture_Variable(test_url)
Thread_Streaming(test_cap)

#endregion Streaming Client

#region Streaming

def Run_Command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return False
    return True

# 1. 라즈베리파이 카메라 설정
def Setup_Camera():
    print("Setting up Raspberry Pi Camera...")
    Run_Command("vcgencmd get_camera")
    with open("/etc/modules", "a") as f:
        f.write("bcm2835-v4l2\n")
    print("Camera setup complete.")

# 2. UV4L 설치
def Install_UV4L():
    print("Adding UV4L repo key...")
    Run_Command("curl https://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -")
    
    print("Adding UV4L repo to sources list...")
    with open("/etc/apt/sources.list", "a") as f:
        f.write("deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ $(lsb_release -sc) main\n")
    
    print("Updating package lists...")
    Run_Command("sudo apt-get update")
    
    print("Installing UV4L and related packages...")
    Run_Command("sudo apt-get install uv4l uv4l-raspicam uv4l-raspicam-extras uv4l-server uv4l-uvc uv4l-xscreen uv4l-mjpegstream uv4l-dummy uv4l-raspidisp")

# 3. UV4L 서비스 시작
def Start_UV4L_Service():
    print("Starting UV4L service...")
    Run_Command("sudo service uv4l_raspicam restart")
    print("UV4L service started.")

# 4. 스트리밍 중지
def Stop_UV4L_Service():
    print("Stopping UV4L service...")
    Run_Command("sudo pkill uv4l")
    print("UV4L service stopped.")

# 전체 설정 및 시작 프로세스
def Setup_And_Start_Streaming():
    Setup_Camera()
    #Install_UV4L()
    Start_UV4L_Service()

# 메인 함수
# if __name__ == "__main__":
    # Setup_And_Start_Streaming()

#endregion Streaming

