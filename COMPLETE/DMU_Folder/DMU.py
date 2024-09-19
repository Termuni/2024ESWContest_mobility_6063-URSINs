import cv2
import mediapipe as mp
import time
import numpy as np
from scipy.spatial import distance

import UART_Communication as wcom

# 위험도 계산 관련 변수
SLEEPY_THRESHOLD_EAR = 0.1  # EAR이 이 값 이하일 때 눈이 감겼다고 간주
MAX_SCORE = 100  # 최대 점수
SCORE_INCREMENT_RATE = 1.5 # 눈이 감긴 시간에 따라 점수가 증가하는 비율 (초당 50점)
SCORE_DECREMENT_RATE = 1  # 눈을 뜰 때 점수가 감소하는 비율 (초당 20점)
# 타이머 설정
alert_display_duration = 3  # 경고 메시지 표시 시간 (초)
    

def Init_Face_Mesh():    
    global mp_face_mesh, mp_drawing, drawing_spec
    # MediaPipe Face Mesh 초기화
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    
def Init_CAM():
    cap = cv2.VideoCapture(0)
    return cap

def Calc_Ear(eye_landmarks):
    # 눈의 EAR 계산
    A = distance.euclidean(eye_landmarks[1], eye_landmarks[5])
    B = distance.euclidean(eye_landmarks[2], eye_landmarks[4])
    C = distance.euclidean(eye_landmarks[0], eye_landmarks[3])

    ear = (A + B) / (2.0 * C)
    return ear

def Get_Eye_landmarks(face_landmarks, eye_indices):
    return [(face_landmarks.landmark[idx].x, face_landmarks.landmark[idx].y) for idx in eye_indices]

def Calc_Drowsiness_Score(ear, eye_closed_start_time, drowsiness_score, last_eye_open_time):
    global SLEEPY_THRESHOLD_EAR, MAX_SCORE, SCORE_INCREMENT_RATE, SCORE_DECREMENT_RATE
    current_time = time.time()
    if ear < SLEEPY_THRESHOLD_EAR:
        if eye_closed_start_time is None:
            eye_closed_start_time = current_time
        elapsed_time = current_time - eye_closed_start_time
        score = min(MAX_SCORE, drowsiness_score + elapsed_time * SCORE_INCREMENT_RATE)
        last_eye_open_time = None  # 눈이 감겼으므로 열려 있는 시간 초기화
    else:
        if last_eye_open_time is None:
            last_eye_open_time = current_time
        elapsed_open_time = current_time - last_eye_open_time
        score = max(0, drowsiness_score - elapsed_open_time * SCORE_DECREMENT_RATE)
        eye_closed_start_time = None  # 눈이 떠졌으므로 감긴 시간 초기화
    return score, eye_closed_start_time, last_eye_open_time

def Process_Frame(frame, face_mesh, eye_closed_start_time, drowsiness_score, drowsy_detected, alert_start_time, last_eye_open_time):
    global mp_face_mesh, mp_drawing, drawing_spec
    # BGR 이미지를 RGB로 변환
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # 얼굴 랜드마크 감지
    results = face_mesh.process(image)

    # BGR로 변환 (OpenCV용)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 얼굴 랜드마크 그리기
            mp_drawing.draw_landmarks(
                image, 
                face_landmarks, 
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )

            # 눈의 랜드마크 좌표 계산 (왼쪽 및 오른쪽 눈)
            left_eye_indices = [362, 385, 387, 263, 373, 380]
            right_eye_indices = [33, 160, 158, 133, 153, 144]

            left_eye_landmarks = Get_Eye_landmarks(face_landmarks, left_eye_indices)
            right_eye_landmarks = Get_Eye_landmarks(face_landmarks, right_eye_indices)

            # 왼쪽 및 오른쪽 눈의 EAR 계산
            left_ear = Calc_Ear(left_eye_landmarks)
            right_ear = Calc_Ear(right_eye_landmarks)
            avg_ear = (left_ear + right_ear) / 2.0

            drowsiness_score, eye_closed_start_time, last_eye_open_time = Calc_Drowsiness_Score(
                avg_ear, eye_closed_start_time, drowsiness_score, last_eye_open_time
            )

    return image, drowsiness_score, eye_closed_start_time, drowsy_detected, alert_start_time, last_eye_open_time

def Display_ALERT(image, drowsiness_score, drowsy_detected, alert_start_time):
    global alert_display_duration
    if drowsiness_score >= 90:  # 졸음 점수가 90 이상일 때 경고
        if not drowsy_detected:
            alert_start_time = time.time()
        drowsy_detected = True

    if drowsy_detected:
        elapsed_alert_time = time.time() - alert_start_time
        if elapsed_alert_time < alert_display_duration:
            # 화면 빨간색 플래시
            overlay = image.copy()
            overlay[:] = (0, 0, 255)
            alpha = 0.6
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
            
            # 경고 메시지 깜박임
            if int(elapsed_alert_time * 2) % 2 == 0:
                cv2.putText(image, "DROWSY DETECTED!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
        else:
            drowsy_detected = False
    return drowsy_detected, alert_start_time

def main():
    global mp_face_mesh, mp_drawing, drawing_spec
    Init_Face_Mesh()
    cap = Init_CAM()
    eye_closed_start_time = None
    drowsiness_score = 0
    drowsy_detected = False
    alert_start_time = 0
    last_eye_open_time = None  # 눈을 뜬 시간을 기록하는 변수

    with mp_face_mesh.FaceMesh(refine_landmarks=True) as face_mesh:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image, drowsiness_score, eye_closed_start_time, drowsy_detected, alert_start_time, last_eye_open_time = Process_Frame(
                frame, face_mesh, eye_closed_start_time, drowsiness_score, drowsy_detected, alert_start_time, last_eye_open_time
            )

            drowsy_detected, alert_start_time = Display_ALERT(image, drowsiness_score, drowsy_detected, alert_start_time)

            # # 화면에 위험도 점수 표시
            # cv2.putText(image, f'Drowsiness Score: {int(drowsiness_score)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # # 얼굴 랜드마크 표시된 화면 출력
            # cv2.imshow('Driver Monitoring', image)

            if cv2.waitKey(5) & 0xFF == 27:  # ESC 키를 누르면 종료
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
