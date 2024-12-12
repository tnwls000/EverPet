# 🐶 EverPet
**감정인식이 가능한 대화형 반려로봇, EverPet**

<img src="https://github.com/user-attachments/assets/db934777-8535-48df-95ca-c085d243cc63"  width="400"/>

## 💡 기획 배경
인구 주택 총조사에 따르면 1인 가구의 비중이 2017년에 비해 2022년, 5.9%가 증가했습니다.

<img src="https://github.com/user-attachments/assets/77b50e25-0f5a-454b-88ae-e59d1a36a164"  width="400"/>

이렇게 늘어가고 있는 1인 가구가 겪는 가장 큰 어려움은, 외로움입니다.

<img src="https://github.com/user-attachments/assets/f88d71a9-f647-4eb1-8f5f-17b899302e1b"  width="400"/>

이러한 1인 가구의 외로움을 해소하고자 EverPet이 탄생했습니다!

## 참여 인원
|홍예원|박수진|송제강|장윤석|하성표|허지윤|
|------|---|---|---|---|---|
|PM/EM|BE/INFRA|EM|EM|EM|FE/DESIGN|
|센서 및 통신|백엔드 총괄 및 서버 배포|로봇 프론트엔드 및 통신|음성인식|자율주행|프론트엔드 총괄 및 디자인, 3D 모델링|

## Architecture
<img src="https://github.com/user-attachments/assets/b124a76a-1c09-4d4f-87e4-c87f312f9cd3"  width="400"/>

## ERD
<img src="https://github.com/user-attachments/assets/97ef5a69-2826-486b-a992-6ea2efc0a881"  width="400"/>

## 😙 Stack
### Embedded

![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)
![ROS](https://img.shields.io/badge/ros-%230A0FF9.svg?style=for-the-badge&logo=ros&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/-Raspberry_Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
- jetson orin nano

### Backend

![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring](https://img.shields.io/badge/spring-%236DB33F.svg?style=for-the-badge&logo=spring&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

### Frontend

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

### DB

![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

### CI/CD

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Jenkins](https://img.shields.io/badge/jenkins-%232C5263.svg?style=for-the-badge&logo=jenkins&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

### Communication

![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Jira](https://img.shields.io/badge/jira-%230A0FFF.svg?style=for-the-badge&logo=jira&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)
![Framer](https://img.shields.io/badge/Framer-black?style=for-the-badge&logo=framer&logoColor=blue)

## 🎥 영상 포트폴리오
**AIoT 프로젝트인 만큼 문서보다는 영상을 통해 더욱 EverPet을 이해하실 수 있을 거에요!**

[🎥 영상 포트폴리오 보러가기](https://youtu.be/AGWXRUQXOBA)

## ✨ 핵심 기능
### 대화
음성인식과 TTS를 활용해 에버펫과 주인이 자연스러운 대화를 할 수 있도록 구현했어요!

### 공감
주인의 음성을 텍스트로 변환 후 감정을 분석하여 에버펫이 주인에게 공감할 수 있도록 했어요!

다양한 눈표정을 통해 공감할 수 있어요!

### 이동
ROS2, LiDAR, SLAM를 활용해 에버펫이 집안 내부를 이동하고, 주인이 귀가 시 문 앞으로 이동해 문안 인사를 할 수 있도록 했어요!

### 다이어리
음성을 통한 하루 회고로 에버펫이 주인 대신 하루를 되돌아보는 다이어리를 작성할 수 있도록 했어요!

## 🖥️ 웹 화면
### 메인화면
<img src="https://github.com/user-attachments/assets/ab38dc80-678b-42df-8d5a-822ea3833432"  width="400"/>
<img src="https://github.com/user-attachments/assets/d2d637c3-d7a0-424a-8a6e-73bafc52d642"  width="100"/>

### 회원가입
<img src="https://github.com/user-attachments/assets/0469f800-acd9-46c1-b278-8449e419dde4"  width="400"/>
<img src="https://github.com/user-attachments/assets/a072970d-897d-4b22-a176-b868b4f395d1"  width="400"/>
<img src="https://github.com/user-attachments/assets/21547e8e-de2d-438e-9869-16885f761d97"  width="400"/>

### 아이디 및 비밀번호 찾기
<img src="https://github.com/user-attachments/assets/72361f5c-1a24-482f-a8f5-5f80f473f8fb"  width="400"/>
<img src="https://github.com/user-attachments/assets/995d9d62-c1cc-40cf-b071-c12ea84daaf8"  width="400"/>
<img src="https://github.com/user-attachments/assets/cd16843a-2491-4b52-95b9-2111e9aed1c9"  width="400"/>

### 로그인
<img src="https://github.com/user-attachments/assets/5bd2f574-c0da-4593-832b-f9327ebea769"  width="400"/>

### 회원 및 로봇 정보 수정
<img src="https://github.com/user-attachments/assets/69e533b3-d178-4d1d-9009-f90fba6b64d9"  width="400"/>

### 출입 기록 조회
<img src="https://github.com/user-attachments/assets/b693863f-ea81-4c31-9a5e-431dfe34424a"  width="400"/>

### 다이어리
<img src="https://github.com/user-attachments/assets/6f9f9bb8-9f8d-42e6-93d5-c2f35ac71f91"  width="100"/>
<img src="https://github.com/user-attachments/assets/879326be-a8c0-4420-ad64-fac0078084af"  width="400"/>
<img src="https://github.com/user-attachments/assets/41edcc72-9021-4bd2-a09b-2764ac923906"  width="100"/>
