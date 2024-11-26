# URSINs
### Urgent Response System In-Need Senior drivers
<img width="372" alt="URSINs" src="https://github.com/user-attachments/assets/dc4a3741-f795-4625-9f0d-32911cd180b7">

고령 운전자를 위한 응급상황 대응 시스템

## 개요
<img width="851" alt="개발 배경" src="https://github.com/user-attachments/assets/56534866-785e-4a13-8424-6804683e36c8">

최근 초고령화사회로 인한 고령운전자 증가 및 사고가 증가하고 있습니다.

국내 현재 고령 운전자 500만명이며, 2040년에는 1300명으로 증가를 예상하고 있습니다.

최근 5년 고령운전자의 추돌 사고는 연 평균 15% 증가하였으며, 치사율은 전체 연령대 평균의 2배입니다.


### 해결 타겟
<img width="866" alt="해결 타겟" src="https://github.com/user-attachments/assets/27b086fb-a20d-4db9-b1d0-ed6491696387">

이러한 사고의 원인을 저희는 심정지, 뇌경색, 페달 오조작으로 판단하였습니다.

따라서 신체 이상과 페달 오조작을 방지하기 위해 솔루션을 준비하였습니다.

## 시스템 소개
### 운전자 모니터링 시스템
<img width="852" alt="운전자 모니터링 시스템" src="https://github.com/user-attachments/assets/91b38eac-f657-4646-aea7-b8307dd89e9f">

저희는 운전자 모니터링 시스템을 개발하였습니다.

운전자의 눈, 어깨 각도 / 심박 상태 / 기절 여부 / 운전 부주의 와 같은 상태를 확인하였습니다.

이 상태의 심각성에 따라 가중치를 두어, 응급 단계를 계산하도록 시스템을 구축하였습니다.


### 응급 단계별 동작도
<img width="917" alt="응급 단계별 동작도" src="https://github.com/user-attachments/assets/b2d2273e-cdcb-4536-ba5a-027fe22925c7">

**0단계**(정상 운전 상태)

정상적으로 운전자가 이상 없이 운전하고 있는 상태로, 별도 가중치가 없는 경우입니다.

**1단계**(차량 내부 자체 경고)

운전자의 부주의 또는 졸음, 경미한 위험 등에 따라 위험 안내를 합니다. 

가중치가 일부 있는 상태에서 동작합니다.

**2단계**(원격 센터 육안 확인)

운전자가 1단계의 경고에 대해 응답하지 못하고, 계속해서 위험에 있는 경우입니다.

이 경우 원격 센터에서 운전자의 상태를 모니터링 합니다.

모니터링 결과 운전자 이상이 확실한 경우, 3단계인 **원격 운전**으로 전환을 시도합니다.

**3단계**(원격 센터 원격 운전)

운전자가 위험하다고 판단 된 경우, 원격 운전을 시행합니다. 

### 시연 영상
https://youtu.be/tdjMa8HQYMU
[![Video Label](http://img.youtube.com/vi/tdjMa8HQYMU/0.jpg)](https://youtu.be/tdjMa8HQYMU)

## 작품 소개
### HW 구성도
<img width="890" alt="HW 구성도" src="https://github.com/user-attachments/assets/33d2dfee-3c63-4c39-8aa2-6bdba6b4a7cd">

저희의 HW 구성도입니다. 

**DMU (Driver Monitoring Unit)**

차량 내부 **운전자의 상태를 확인**하고, 상태를 정보화 시켜 처리하는 유닛입니다.

**카메라, 심박센서, 안전벨트**를 통해 정보를 획득하고, 이를 CCU에게 전달합니다.


**CCU (Central Command Unit)**

차량의 **중앙 제어기**로서, 다음과 같은 동작을 처리합니다.


1. 초음파 센서를 통해 운전자의 페달 오조작 및 운전 부주의 여부를 감지합니다.

2. DMU, TCU로부터 받는 정보를 활용하여 운전자의 응급 단계를 계산합니다.


이러한 정보를 바탕으로, 운전자의 응급 정도를 계산하고, 해당 응급 정도에 따라 동작을 지시합니다.

1. 원격 모니터링 지시 명령

2. 운전자 상태 점검을 위한 스피커 출력 및 모니터 화면 출력


**TCU (Telemetrics Control Unti)**

차량의 **통신 제어기**로서, 원격 센터로 정보를 보내는 역할을 합니다.

운전자 응급 단계, 위치 정보(GPS), 그리고 내/외부 상황에 대해 스트리밍을 진행합니다.


**RmtCenter (Remote Center)**

차량의 **원격 운전을 위한 센터**로, TCU에서 정보를 받아옵니다.

운전자 응급 단계, 위치 정보(GPS), 그리고 내/외부 상황에 대해 판단하고 처리합니다.

### 응급 단계 계산 로직
<img width="900" alt="응급단계 계산 로직" src="https://github.com/user-attachments/assets/1898bb15-5526-4d5e-99b2-d3d3426e06d4">

<img width="900" alt="1단계" src="https://github.com/user-attachments/assets/c97ec418-70c6-46ef-89c6-6b3f6ae5841f">

<img width="900" alt="2단계" src="https://github.com/user-attachments/assets/a009db92-183d-4c86-9d4b-5739b86df99a">

<img width="900" alt="3단계" src="https://github.com/user-attachments/assets/1525267d-d12f-4cc0-8573-280fac8baf2d">


## 가능성
### 실제 적용 방안
<img width="478" alt="활용가능성" src="https://github.com/user-attachments/assets/645948e8-b729-4cd4-b18f-cafe3a458c6b">

위에서 소개한 시스템들은 모두 신규 차량에 이미 있는 시스템으로, **SW 중심 개발**이 가능합니다.
즉, **HW 설계 비용이 낮습니다**.

### 국내 원격 운전
<img width="154" alt="경찰청" src="https://github.com/user-attachments/assets/5682cbfd-acba-42bd-9a27-85a1874741d8">

**경찰청** '24.06 <**원격운전 통행 안정성 제고**를 위한 용역> 시작

<img width="154" alt="쏘카" src="https://github.com/user-attachments/assets/a44f71c0-0180-4c8f-8dd7-e2372505c13d">

쏘카 "25년 상반기 원격운전 도입" (렌터카 원격 배달/회수)

### 기대 효과
**직접적 효과** : 사고 피해 대폭 절감
**간접적 효과** : 고령자 이동권 보장, 차량 수요자 감소 방지 및 고령사회 자동차 산업 지속 가능

## 기타 정보
### 개발 일정
<img width="849" alt="개발일정" src="https://github.com/user-attachments/assets/07fd5ba8-a157-4ead-861b-69f99ab3788a">

### GIT 정보
이 Git은 임베디드 SW 공모전을 위해 생성된 것으로 구성은 다음과 같습니다.

COMPLETE -> 각각의 MCU들에 들어갈 코드가 들어가있는 폴더
- CCU : Center Control Unit
- TCU : Telemetrics Control Unit
- DMU : Driver Monitoring Unit
- RmtCenter : 원격 센터

총 4개의 MCU에 들어갈 각각의 폴더이며, RmtCenter를 제외한 나머지는 전부 1개의 차량 안에 들어갈 MCU들에 속합니다.
