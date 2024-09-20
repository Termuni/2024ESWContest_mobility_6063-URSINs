import cv2
import mediapipe as mp
import time
import numpy as np
from scipy.spatial import distance

#==================CUSTOM IMPORT==================
import BPM as bpm
import UART_Communication as wcom
#==================CUSTOM IMPORT==================

# MediaPipe Face Mesh 및 Pose 초기화
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# 위험도 계산 관련 변수
SLEEPY_THRESHOLD_EAR = 0.1  # EAR이 이 값 이하일 때 눈이 감겼다고 간주
MAX_SCORE = 100  # 최대 점수
SCORE_INCREMENT_RATE = 4  # 눈이 감긴 시간에 따라 점수가 증가하는 비율 (초당 50점)
SCORE_DECREMENT_RATE = 2  # 눈을 뜰 때 점수가 감소하는 비율 (초당 20점)

# 타이머 설정
alert_display_duration = 3  # 경고 메시지 표시 시간 (초)

# 얼굴 기울기와 거리 계산에 필요한 상수
HEAD_TILT_THRESHOLD = 1.5  # 얼굴 기울기 임계값 (라디안 단위)
SHOULDER_FACE_DISTANCE_THRESHOLD = 0.4  # 어깨와 얼굴 사이의 거리 임계값 (얼굴이 어깨에 가까울 때)

#region FUNCTION
def initialize_camera():
    cap = cv2.VideoCapture(0)
    return cap

def calculate_ear(eye_landmarks):
    # 눈의 EAR 계산
    A = distance.euclidean(eye_landmarks[1], eye_landmarks[5])
    B = distance.euclidean(eye_landmarks[2], eye_landmarks[4])
    C = distance.euclidean(eye_landmarks[0], eye_landmarks[3])

    ear = (A + B) / (2.0 * C)
    return ear

def get_eye_landmarks(face_landmarks, eye_indices):
    return [(face_landmarks.landmark[idx].x, face_landmarks.landmark[idx].y) for idx in eye_indices]

# 각 조건별로 점수를 계산하는 함수
def calculate_ear_score(ear, eye_closed_start_time, ear_score, last_eye_open_time):
    current_time = time.time()

    # EAR (눈 감김) 체크
    if ear < SLEEPY_THRESHOLD_EAR:
        if eye_closed_start_time is None:
            eye_closed_start_time = current_time
        elapsed_time = current_time - eye_closed_start_time
        ear_score = min(MAX_SCORE, ear_score + elapsed_time * SCORE_INCREMENT_RATE)
        last_eye_open_time = None  # 눈이 감긴 상태
    else:
        if last_eye_open_time is None:
            last_eye_open_time = current_time
        elapsed_open_time = current_time - last_eye_open_time
        ear_score = max(0, ear_score - elapsed_open_time * SCORE_DECREMENT_RATE)
        eye_closed_start_time = None  # 눈이 열린 상태

    return ear_score, eye_closed_start_time, last_eye_open_time

def calculate_head_tilt_score(head_tilt, head_tilt_score):
    # 얼굴 기울기 체크
    if abs(head_tilt) > HEAD_TILT_THRESHOLD + 0.5 or abs(head_tilt) < HEAD_TILT_THRESHOLD - 0.5:
        head_tilt_score += 2  # 얼굴이 기울어졌을 때 점수 증가
    else:
        head_tilt_score -= 1.5  # 얼굴이 정상 범위로 돌아왔을 때 점수 감소

    head_tilt_score = max(0, min(head_tilt_score, MAX_SCORE))
    return head_tilt_score

def calculate_face_shoulder_distance_score(face_shoulder_distance, face_shoulder_score):
    # 얼굴과 어깨 사이 거리 체크
    if face_shoulder_distance < SHOULDER_FACE_DISTANCE_THRESHOLD:
        face_shoulder_score += 2  # 얼굴이 어깨에 너무 가까울 때 점수 증가
    else:
        face_shoulder_score -= 1.5  # 얼굴이 정상 범위로 돌아왔을 때 점수 감소

    face_shoulder_score = max(0, min(face_shoulder_score, MAX_SCORE))
    return face_shoulder_score

def calculate_head_tilt(face_landmarks):
    nose_tip = np.array([face_landmarks.landmark[1].x, face_landmarks.landmark[1].y])
    chin = np.array([face_landmarks.landmark[152].x, face_landmarks.landmark[152].y])
    
    # 코 끝과 턱 끝을 기준으로 얼굴 기울기 계산 (단위: 라디안)
    head_tilt_angle = np.arctan2(nose_tip[1] - chin[1], nose_tip[0] - chin[0])
    return head_tilt_angle

def calculate_face_shoulder_distance(face_landmarks, pose_landmarks):
    nose_tip = np.array([face_landmarks.landmark[1].x, face_landmarks.landmark[1].y])
    left_shoulder = np.array([pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                              pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y])
    right_shoulder = np.array([pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                               pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y])
    
    # 얼굴과 두 어깨 중 더 가까운 어깨와의 거리 계산
    left_distance = distance.euclidean(nose_tip, left_shoulder)
    right_distance = distance.euclidean(nose_tip, right_shoulder)
    
    # 더 가까운 어깨와의 거리를 반환
    return min(left_distance, right_distance)

def draw_landmarks(image, face_landmarks, pose_landmarks):
    # 얼굴의 코 끝 좌표
    nose_tip = face_landmarks.landmark[1]
    
    # 왼쪽 및 오른쪽 어깨 좌표
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    
    # 코 끝 좌표 시각화
    nose_tip_coords = (int(nose_tip.x * image.shape[1]), int(nose_tip.y * image.shape[0]))
    #cv2.circle(image, nose_tip_coords, 5, (0, 255, 0), -1)  # 코 끝은 초록색 원으로 표시

    # 어깨 좌표 시각화
    left_shoulder_coords = (int(left_shoulder.x * image.shape[1]), int(left_shoulder.y * image.shape[0]))
    right_shoulder_coords = (int(right_shoulder.x * image.shape[1]), int(right_shoulder.y * image.shape[0]))
    #cv2.circle(image, left_shoulder_coords, 5, (255, 0, 0), -1)  # 왼쪽 어깨는 파란색 원으로 표시
    #cv2.circle(image, right_shoulder_coords, 5, (255, 0, 0), -1)  # 오른쪽 어깨는 파란색 원으로 표시

    # 어깨 사이에 선 그리기
    #cv2.line(image, left_shoulder_coords, right_shoulder_coords, (255, 255, 255), 2)  # 어깨 사이에 흰색 선

    # 얼굴과 왼쪽 어깨를 연결하는 선
    #cv2.line(image, nose_tip_coords, left_shoulder_coords, (0, 255, 255), 2)  # 노란색 선
    # 얼굴과 오른쪽 어깨를 연결하는 선
    #cv2.line(image, nose_tip_coords, right_shoulder_coords, (0, 255, 255), 2)  # 노란색 선

def process_frame(frame, face_mesh, pose, eye_closed_start_time, drowsiness_scores, last_eye_open_time):
    # BGR 이미지를 RGB로 변환
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # 얼굴 및 자세 랜드마크 감지
    face_results = face_mesh.process(image)
    pose_results = pose.process(image)

    # BGR로 변환 (OpenCV용)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if face_results.multi_face_landmarks and pose_results.pose_landmarks:
        face_landmarks = face_results.multi_face_landmarks[0]
        pose_landmarks = pose_results.pose_landmarks

        # 얼굴 랜드마크 그리기
        #mp_drawing.draw_landmarks(
        #    image, 
        #    face_landmarks, 
        #    mp_face_mesh.FACEMESH_TESSELATION,
        #    landmark_drawing_spec=drawing_spec,
        #    connection_drawing_spec=drawing_spec
        #)

        # 얼굴과 어깨 좌표를 화면에 표시
        #draw_landmarks(image, face_landmarks, pose_landmarks)

        # 눈의 랜드마크 좌표 계산 (왼쪽 및 오른쪽 눈)
        left_eye_indices = [362, 385, 387, 263, 373, 380]
        right_eye_indices = [33, 160, 158, 133, 153, 144]

        left_eye_landmarks = get_eye_landmarks(face_landmarks, left_eye_indices)
        right_eye_landmarks = get_eye_landmarks(face_landmarks, right_eye_indices)

        # 왼쪽 및 오른쪽 눈의 EAR 계산
        left_ear = calculate_ear(left_eye_landmarks)
        right_ear = calculate_ear(right_eye_landmarks)
        avg_ear = (left_ear + right_ear) / 2.0

        # 얼굴 기울기 계산
        head_tilt = calculate_head_tilt(face_landmarks)

        # 얼굴과 어깨 사이의 거리 계산
        face_shoulder_distance = calculate_face_shoulder_distance(face_landmarks, pose_landmarks)

        # 각 조건별로 점수 계산
        drowsiness_scores['ear_score'], eye_closed_start_time, last_eye_open_time = calculate_ear_score(
            avg_ear, eye_closed_start_time, drowsiness_scores['ear_score'], last_eye_open_time
        )
        drowsiness_scores['head_tilt_score'] = calculate_head_tilt_score(head_tilt, drowsiness_scores['head_tilt_score'])
        drowsiness_scores['face_shoulder_score'] = calculate_face_shoulder_distance_score(
            face_shoulder_distance, drowsiness_scores['face_shoulder_score']
        )

    # 최종 졸음 점수 = 각 점수의 합
    total_drowsiness_score = sum(drowsiness_scores.values())
    
    return image, drowsiness_scores, total_drowsiness_score, eye_closed_start_time, last_eye_open_time

def display_alert(image, total_drowsiness_score, drowsy_detected, alert_start_time):
    if total_drowsiness_score >= 150:  # 졸음 점수가 90 이상일 때 경고
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
                cv2.putText(image, "DROWSY DETECTED!", (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
        else:
            drowsy_detected = False
    return drowsy_detected, alert_start_time

def get_drowsiness_level(total_drowsiness_score):
    if total_drowsiness_score < 40:
        return 0  # 레벨 0
    elif total_drowsiness_score < 80:
        return 1  # 레벨 1
    elif total_drowsiness_score < 120:
        return 2  # 레벨 2
    else:
        return 3  # 레벨 3
#endregion FUNCTION

def main():
    #region INIT
    #INIT_BPM
    ppg_lv = 0
    ecg_lv = 0
    bpm.Init_BPM()
    bpm.Init_Get_BPM_Data()
    
    #INIT_UART
    dTc_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ DMU Serial
    data_to_CCU = "0,0,0"
    
    #INIT_CAM
    cap = initialize_camera()
    eye_closed_start_time = None
    drowsiness_scores = {'ear_score': 0, 'head_tilt_score': 0, 'face_shoulder_score': 0}  # 개별 점수
    total_drowsiness_score = 0
    drowsiness_level = 0
    drowsy_detected = False
    alert_start_time = 0
    last_eye_open_time = None  # 눈을 뜬 시간을 기록하는 변수
    #endregion INIT
    
    with mp_face_mesh.FaceMesh(refine_landmarks=True) as face_mesh, mp_pose.Pose() as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image, drowsiness_scores, total_drowsiness_score, eye_closed_start_time, last_eye_open_time = process_frame(
                frame, face_mesh, pose, eye_closed_start_time, drowsiness_scores, last_eye_open_time
            )

            drowsy_detected, alert_start_time = display_alert(image, total_drowsiness_score, drowsy_detected, alert_start_time)

            # 레벨 계산 및 전송
            ppg_lv = bpm.Get_PPG_BPM_Data()
            ecg_lv = bpm.Get_ECG_BPM_Data()
            drowsiness_level = get_drowsiness_level(total_drowsiness_score)
            data_to_CCU = f'{ppg_lv},{ecg_lv},{drowsiness_level}'
            wcom.Send_Data(dTc_Ser, data_to_CCU)

            # 화면에 위험도 점수 및 레벨 표시
            cv2.putText(image, f'Drowsiness Level: {drowsiness_level}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'Drowsiness Score 1 (EAR): {int(drowsiness_scores["ear_score"])}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'Drowsiness Score 2 (Tilt): {int(drowsiness_scores["head_tilt_score"])}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'Drowsiness Score 3 (Shoulder): {int(drowsiness_scores["face_shoulder_score"])}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'Total Drowsiness Score: {int(total_drowsiness_score)}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

            # 얼굴 랜드마크 표시된 화면 출력
            cv2.imshow('Driver Monitoring', image)

            if cv2.waitKey(5) & 0xFF == 27:  # ESC 키를 누르면 종료
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

