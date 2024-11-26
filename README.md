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

### 응급 단계별 동작도
<img width="917" alt="응급 단계별 동작도" src="https://github.com/user-attachments/assets/b2d2273e-cdcb-4536-ba5a-027fe22925c7">

### 시연 영상
[![Video Label](http://img.youtube.com/vi/'유튜브주소의id'/0.jpg)](https://youtu.be/'유튜브주소의id')

## 작품 소개
### HW 구성도
<img width="890" alt="HW 구성도" src="https://github.com/user-attachments/assets/33d2dfee-3c63-4c39-8aa2-6bdba6b4a7cd">

### 응급 단계 계산 로직
<img width="898" alt="응급단계 계산 로직" src="https://github.com/user-attachments/assets/1898bb15-5526-4d5e-99b2-d3d3426e06d4">

<img width="666" alt="1단계" src="https://github.com/user-attachments/assets/c97ec418-70c6-46ef-89c6-6b3f6ae5841f">

<img width="871" alt="2단계" src="https://github.com/user-attachments/assets/a009db92-183d-4c86-9d4b-5739b86df99a">

<img width="932" alt="3단계" src="https://github.com/user-attachments/assets/1525267d-d12f-4cc0-8573-280fac8baf2d">


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
