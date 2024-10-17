from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtQuick import *
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtQuickWidgets import *

from mainUI5 import Ui_MainWindow
import subprocess
from functools import partial
import os
import requests
import sys
import signal
import sys

sys.path.append('/home/pi/.local/lib/python3.11/site-packages')

import openai
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

import webbrowser
import urllib.request
import time
import requests
import json
import digitalio

koreanToEnglish = dict()
EnglishToKorean = dict()
KoToEn = { '활발' : "energetic", '친근' : "friendly", '소심' : "timid", '도도' : "uppity", '남' : "M", "여" : "F",'수컷' : "M", "암컷" : "F" }
EnToko = { 'energetic' : "활발", 'friendly' : "친근", 'timid심' : "소심", 'uppity' : "도도", "M" : "남", "F" : "여" }

def read_allinfo(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_allinfo(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data has been written to {file_path}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

def text_to_speech(text, lang='ko'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")

def play_audio(file_path, speed=1.3):
    audio = AudioSegment.from_file(file_path, format="mp3")
    new_audio = audio.speedup(playback_speed=speed)
    play(new_audio)

model = "gpt-4o"
humanName=""
petName=""
intimacy=0
personality=""
lastAnswer=""

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

#시간을 업데이트 하기 위한 쓰레드
class TimeUpdateThread(QThread):
    global settings_data
    time_signal = Signal(str)  # 시간을 업데이트하기 위한 신호 정의
    
    def run(self):
        flag=False # 전원을 켰을 때, 처음엔 바로 업데이트
        while True:
            current_time = QTime.currentTime()
            hour = current_time.hour()
            second = current_time.second()
            if(flag and second != 0): continue; #이 후 0초일 때 업데이트
            if hour < 12:
                if settings_data["language"]=="English":
                    period="AM"
                else:
                    period = "\uC624\uC804"  # "오전"의 유니코드
            else:
                if settings_data["language"]=="English":
                    period="PM"
                else:
                    period = "\uC624\uD6C4"  # "오후"의 유니코드

            hour_12 = hour % 12
            if hour_12 == 0:
                hour_12 = 12

            time_str = f"{period} {hour_12}:{current_time.toString('mm')}"
            current_date_time = QDate.currentDate().toString("yyyy-MM-dd/") + time_str
            self.time_signal.emit(current_date_time)  # 시간을 메인 스레드로 전달
            time.sleep(60)  # 1분마다 갱신
            flag=True
            
#음성인식 쓰레드
class SpeechRecognitionThread(QThread):

    result_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_listening = None
        
    # 음성인식을 background로 실행할 수 있도록 쓰레드로 실행
    def run(self):
        with self.microphone as source: 
            self.recognizer.adjust_for_ambient_noise(source) 
        self.recognizer.dynamic_energy_threshold = True  
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_adjustment_ratio = 1.5
        self.stop_listening = self.recognizer.listen_in_background(self.microphone, self.callback)
        pass
        
    def stop(self):
    #음성인식 종료
        if self.stop_listening:
            self.stop_listening()
            self.stop_listening = None
        
    #음성이 인식될 때 마다 불리는 콜백함수
    def callback(self, recognizer, audio):
        global humanName, petName, intimacy, personality, lastAnswer, serialNum
        try:
            # 생각 중임을 display에 표현
            subprocess.run(["python3", "/home/pi/mqtt/display.py", "hard"])
            
            #텍스트로 변환            
            text = recognizer.recognize_google(audio, language="ko-KR")
                 
            #openai API 프롬프트
            transcription="너는 반려동물이고, 이름은 "+petName+"이야. 그리고 너의 주인의 이름은 "+humanName+"이야. 너는 주인에게 "+str(intimacy)+"/10000 친밀도를 가지고 있어. 너는 4가지 성격을 가질 수 있어 : 활발, 친근, 도도, 소심. 활발한 성격을 가지면 너는 주인에게 반말을 해. 그리고 주인의 이야기보다 너의 이야기를 하는 것을 좋아하지. 그래서 주인이 말해도 그 얘기에 공감하고 주제를 이어가기 보다는 네가 하고 싶은 얘기를 해. 친근한 성격을 가지면 너는 주인에게 반말을 해. 그리고 주인의 말에 살갑게 대답하고 공감을 잘해주는 착한 반려동물이 돼. 도도한 성격을 가지면 주인에게 반말을 해. 그리고 주인을 자신의 집사처럼 여겨. 주인에게 관심은 없지만, 너의 삶을 이어가기 위해 최소한의 반응만 해줘. 사실 주인이 하는 얘기가 너랑 별로 상관이 없다고 생각해. 소심한 성격을 가지면 너는 주인에게 존댓말을 해. 그리고 멀리서 주인을 바라보고, 주인이 말하면 쭈볏거리며 다가와서 말을 들어줘. 하지만 너의 의견은 잘 표출하지는 못해. 물론 말을 하기는 해. 너의 성격은 활발, 친근, 도도, 소심 중에 "+personality+"이야. 너의 감정은 기본과 특별로 나뉘어.[기본 감정 : joy, sad, tired, angry, curious, realize, sleep],[특별 감정 : happy, exciting, hard, more_realize] 따옴표 없이 네 입장에서의 대답 적어줘. 주인에 대한 너의 친밀도가 8000 보다 작으면 너의 감정을 기본 감정 중에 하나로 골라서 적어주고, 8000보다 크거나 같으면 너의 감정을 너의 감정을 기본 감정과 특별 감정 중에 하나로 골라서 적어줘. " + " 다음 양식으로 적어줘 -> 감정/대답. 이전 너의 대답은 "+lastAnswer+"이야. 다음 얘기를 주인이 너에게 했어:" + text
            
            messages = [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": transcription }]
            
            response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    max_tokens=400,
            )
            
            answer = response['choices'][0]['message']['content']
            
            mood, answer_text = answer.split('/', 1)
            #감정에 따라 display에 표현
            subprocess.run(["python3", "/home/pi/mqtt/display.py", mood.strip()])

            text_to_speech(answer_text)
            
            #꼬리 움직이게 감정 jetson으로 보내는 코드
            subprocess.run(["mosquitto_pub", "-h", serverIP, "-t", serialNum+"/jetson/tail", "-m", mood])
            play_audio("output.mp3")
            
            lastAnswer=answer_text

            daytalking["talkingNum"]+=1
            
        except sr.UnknownValueError:
            #인식이 안되었다면 display에 표현
            subprocess.run(["python3", "/home/pi/mqtt/display.py", "curious"])
            self.result_signal.emit("인식할 수 없음")
        except sr.RequestError as e:
            subprocess.Popen(["bash", "-l", "-c", "sudo resolvconf -u"])
                    
            self.result_signal.emit(f"API 요청 오류: {e}")

class MyApp(QMainWindow, Ui_MainWindow):
    global wifiSsid , wifiPwd, lan, sound, signInFlag
    global gender, humanName, petName, intimacy, personality
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main()
        self.setFocus()
        #self.showFullScreen()
        # 이벤트 필터 추가
        self.installEventFilter(self)
        if(lan == "English"):
            self.setLabels(lan)
        self.soundSlider.setValue(sound)
        #wifi 개수에 따라 생성될 버튼들을 담아놓는 List
        self.buttons=[]
        
        # 다이어리 작성 중 현재 인식된 텍스트 개수 
        self.diaryTextnum=0
        self.diaryTexts=[]
        self.jetsonflag=False
        self.espflag=False
        # 날짜와 시간에 따라 text를 적용하기 위한 Label들을 담아 놓는 List
        self.timeLabels=[self.timeText_3,self.timeText_4,self.timeText_5,self.timeText_6,self.timeText_7,self.timeText_8,self.timeText_9]
        self.dateLabels=[self.dateText_3,self.dateText_4,self.dateText_5,self.dateText_6,self.dateText_7,self.dateText_8,self.dateText_9]
        self.date_part = ""
        self.time_part = ""
        
        # 처음 켜졌을 때는 시간을 업데이트 해준다.
        current_time = QTime.currentTime()
        hour = current_time.hour()
        second = current_time.second()
        
        if hour < 12:
            if lan=="English":
                period="AM"
            else:
                period = "\uC624\uC804"  # "오전"의 유니코드
        else:
            if lan=="English":
                period="PM"
            else:
                period = "\uC624\uD6C4"  # "오후"의 유니코드
        
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12

        time_str = f"{period} {hour_12}:{current_time.toString('mm')}"
        current_date_time = QDate.currentDate().toString("yyyy-MM-dd/") + time_str
        
        self.date_part, self.time_part = current_date_time.split('/')
        
        self.time_thread = TimeUpdateThread()
        self.time_thread.time_signal.connect(self.update_time)
        self.time_thread.start()
            
        # 가상키보드가 필요한 widget을 설정
        self.page = self.stackedWidget.widget(1).children()[0]
        self.qml_widget = QQuickWidget( self.page)
        self.qml_widget.setSource(QUrl('/home/pi/GUI/rev.qml'))
        
        width = self.qml_widget.width()
        height = self.qml_widget.height()
        self.qml_widget.setGeometry(0, 250, width, height)
        self.qml_widget.setStyleSheet("background:transparent;")
        self.pwdInput.installEventFilter(self)
        #키보드를 눌러도 Line Text에 있는 focus를 변경하지 않도록 설정
        self.qml_widget.setFocusPolicy(Qt.NoFocus)
        #Line Text에 focus가 있을 때만 키보드가 보이도록 함.
        self.qml_widget.setVisible(False)
        
        # MQTT Process 설정 및 실행
        self.mqttProcess = QProcess(self)
        self.mqttProcess.readyReadStandardOutput.connect(self.handle_mqtt_stdout)
        self.mqttProcess.started.connect(self.handle_mqtt_started)
        self.mqttProcess.finished.connect(self.handle_mqtt_finished)
        
        # touch Process 설정 및 실행
        self.touchProcess = QProcess(self)
        self.touchProcess.readyReadStandardOutput.connect(self.handle_touch_stdout)
        self.touchProcess.started.connect(self.handle_touch_started)
        self.touchProcess.finished.connect(self.handle_touch_finished)
        self.touchProcess.readyReadStandardError.connect(self.handle_stderr)
        
        
        #self.mqttProcess.start("python", ["-u", "/home/pi/mqtt/test3.py"]) #디버깅용
        #self.touchProcess.start("python", ["-u", "/home/pi/touchex/touchex2.py"]) #디버깅용
        
        #음성인식 쓰레드 선언
        self.speech_thread = SpeechRecognitionThread()
        #self.speech_thread.result_signal.connect(self.update_label)
        
        #Diary Process 설정 및 실행
        self.diaryProcess = QProcess(self)
        self.diaryProcess.readyReadStandardOutput.connect(self.handle_diary_stdout)
        self.diaryProcess.started.connect(self.handle_diary_started)
        self.diaryProcess.finished.connect(self.handle_diary_finished)
        #self.diaryProcess.readyReadStandardError.connect(self.handle_diary_stderr)
        
        #self.stackedWidget.setCurrentIndex(9)
        
        #이미 회원가입을 했다면, MainPage에서 시작하고,
        if(signInFlag==True):
            self.goToMainPage()
            #self.stackedWidget.setCurrentIndex(9)
            self.touchProcess.start("python", ["-u", "/home/pi/touchex/touchex2.py"]) 
            self.mqttProcess.start("python", ["-u", "/home/pi/mqtt/test3.py"]) 
            
            self.nameValue.setText(QCoreApplication.translate("MainWindow", petName , None))
           
            if(lan=="English"):
                self.genderValue.setText(QCoreApplication.translate("MainWindow", KoToEn[gender], None))
            else:
              self.genderValue.setText(QCoreApplication.translate("MainWindow", gender, None))

            if(lan=="English"):
                self.typeValue.setText(QCoreApplication.translate("MainWindow", KoToEn[personality], None))
            else:
              self.typeValue.setText(QCoreApplication.translate("MainWindow", personality, None))
            
            QApplication.processEvents()
            
        self.reLoadWifi()
        
    def update_time(self,current_date_time):
        
        self.date_part, self.time_part = current_date_time.split('/')
        
        index = self.stackedWidget.currentIndex()
        if(index >=3 and index <=9):
            self.timeLabels[index-3].setText(self.time_part) 
            self.dateLabels[index-3].setText(self.date_part) 
    
    def handle_diary_stderr(self):
        error_output = self.diaryProcess.readAllStandardError().data().decode()
        print(f"Error output: {error_output}")
        
    def handle_stderr(self):
        error_output = self.touchProcess.readAllStandardError().data().decode()
        print(f"Error output: {error_output}")
        
    def handle_diary_stdout(self): 
        #print("handle_diary_stdout called")  # 디버깅용 출력
        data = self.diaryProcess.readAllStandardOutput().data().decode()
        if data.strip() == "complete":
            self.diaryButton_9.setVisible(True)
            QApplication.processEvents()
        elif len(data.strip()) != 0:
            print(data.strip())
            
            diarytext = QLabel(self.scrollAreaWidgetContents)
            diarytext.setObjectName(u"diarytext{self.diaryTextnum}")
            diarytext.setMinimumSize(QSize(730, 50))
            diarytext.setMaximumSize(QSize(1024, 600))
            diarytext.setFont(QFont("Arial",10))
            diarytext.setWordWrap(True) 
            diarytext.setStyleSheet(u"border-radius:5px;\n"
"background-color : rgb(254, 252, 247);")
            diarytext.setAlignment(Qt.AlignmentFlag.AlignCenter)
            diarytext.setText(QCoreApplication.translate("MainWindow", data.strip() , None))
            
            self.verticalLayout_4.addWidget(diarytext)
            self.diaryTexts.append(diarytext)
            self.diaryTextnum+=1
    def handle_mqtt_stdout(self):
        
        global humanName, petName, intimacy, personality, lastAnswer, gender
        global signInFlag, lan, settings_data
        
        print("handle_mqtt_stdout called")  # 디버깅용 출력
        data = self.mqttProcess.readAllStandardOutput().data().decode()
        print(data) #디버깅용 출력
        
        # mqtt process 에서 complete 시그널이 오면,
        # 회원가입 완료 했다는 시그널
        #  # json 파일 업데이트
        if data.strip() == "complete":
            signInFlag=True
            settings_data["signIn"] = True
            write_allinfo("/home/pi/settings.json", settings_data)
            
            allinfo_data = read_allinfo("/home/pi/allinfo.json")
            
            gender=allinfo_data['robot']['gender']
            humanName=allinfo_data['user']['userName']
            petName=allinfo_data['robot']['name']
            intimacy=allinfo_data['friendship']['current']
            personality=allinfo_data['robot']['personality']
            
            daytalking=read_allinfo("/home/pi/talkingNum.json")
            
            self.nameValue.setText(QCoreApplication.translate("MainWindow", petName , None))
           
            if(lan=="English"):
                self.genderValue.setText(QCoreApplication.translate("MainWindow", KoToEn[gender], None))
            else:
              self.genderValue.setText(QCoreApplication.translate("MainWindow", gender, None))

            if(lan=="English"):
                self.typeValue.setText(QCoreApplication.translate("MainWindow", KoToEn[personality], None))
            else:
              self.typeValue.setText(QCoreApplication.translate("MainWindow", personality, None))
            
            QApplication.processEvents()
            
            json_data = json.dumps(allinfo_data['user']['userID'])
            subprocess.run(["mosquitto_pub", "-h", serverIP, "-t", serialNum+"/jetson/userID", "-m", json_data])
            
            self.goToMainPage()
            QApplication.processEvents()
            
        # 로봇 정보 수정 시그널이 오면,
        # json 파일 업데이트
        elif data.strip() == "modify_robot":
            allinfo_data = read_allinfo("/home/pi/allinfo.json")
            gender=allinfo_data['robot']['gender']
            petName=allinfo_data['robot']['name']
            personality=allinfo_data['robot']['personality']
            
            if(lan=="English"):
                self.genderValue.setText(QCoreApplication.translate("MainWindow", KoToEn[gender], None))
            else:
              self.genderValue.setText(QCoreApplication.translate("MainWindow", gender, None))

            if(lan=="English"):
                self.typeValue.setText(QCoreApplication.translate("MainWindow", KoToEn[personality], None))
            else:
              self.typeValue.setText(QCoreApplication.translate("MainWindow", personality, None))
            
            QApplication.processEvents()
            
        # 현관에서 주인이 왔을 때의 시그널
        elif data.strip()=="userIn":
        
            QApplication.processEvents()
            
            self.mqttProcess.write(b'pause\n')
            if self.speech_thread.stop_listening:
                self.speech_thread.stop()
            
            allinfo_data = read_allinfo("/home/pi/allinfo.json")
            humanName=allinfo_data['user']['userName']
            petName=allinfo_data['robot']['name']
            intimacy=allinfo_data['friendship']['current']
            personality=allinfo_data['robot']['personality']
            messages = [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "너는 반려동물이고, 이름은 "+petName+"이야. 그리고 너의 주인의 이름은 "+humanName+"이야. 너는 주인에게 "+str(intimacy)+"/10000 친밀도를 가지고 있어. 너는 4가지 성격을 가질 수 있어 : 활발, 친근, 도도, 소심. 활발한 성격을 가지면 너는 주인에게 반말을 해. 그리고 주인의 이야기보다 너의 이야기를 하는 것을 좋아하지. 그래서 주인이 말해도 그 얘기에 공감하고 주제를 이어가기 보다는 네가 하고 싶은 얘기를 해. 친근한 성격을 가지면 너는 주인에게 반말을 해. 그리고 주인의 말에 살갑게 대답하고 공감을 잘해주는 착한 반려동물이 돼. 도도한 성격을 가지면 주인에게 반말을 해. 그리고 주인을 자신의 집사처럼 여겨. 주인에게 관심은 없지만, 너의 삶을 이어가기 위해 최소한의 반응만 해줘. 사실 주인이 하는 얘기가 너랑 별로 상관이 없다고 생각해. 소심한 성격을 가지면 너는 주인에게 존댓말을 해. 그리고 멀리서 주인을 바라보고, 주인이 말하면 쭈볏거리며 다가와서 말을 들어줘. 하지만 너의 의견은 잘 표출하지는 못해. 물론 말을 하기는 해. 너의 성격은 활발, 친근, 도도, 소심 중에 "+personality+"이야. 주인이 막 외출 후 귀가했어. 그래서 넌 현관으로 주인을 마중나왔어. 주인에게 인사해줘. 1-2 문장으로 해줘." }]
            response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    max_tokens=400,
            )
            answer = response['choices'][0]['message']['content']
            print(f"ChatGPT 응답: {answer}")
            text_to_speech(f"{answer}")
            play_audio("output.mp3", speed=1.3)
            
            self.mqttProcess.write(b'resume\n')
            self.speech_thread.start() 
            
    def handle_touch_stdout(self): 
        print("handle_touch_stdout called")  # 디버깅용 출력
        data = self.touchProcess.readAllStandardOutput().data().decode()
        print(data)
    #Diary Process 시작
    def handle_diary_started(self):
        print(f"Diary Process started with PID: {self.diaryProcess.pid()}")
    #Diary Process 종료
    def handle_diary_finished(self):
        print("Diary Process ended.")
    #MQTT Process 시작
    def handle_mqtt_started(self):
        print(f"MQTT Process started with PID: {self.mqttProcess.pid()}")
    #MQTT Process 종료
    def handle_mqtt_finished(self):
        print("MQTT Process ended.")
    #Touch Process 시작
    def handle_touch_started(self):
        print(f"Touch Process started with PID: {self.touchProcess.pid()}")
    #Touch Process 종료
    def handle_touch_finished(self):
        print("Touch Process ended.")
        
    #창이 닫힐 때의 Event
    def closeEvent(self, event):
        if(self.diaryProcess.state() == QProcess.Running):
            self.diaryProcess.write(b'stop\n')
        event.accept()  # 또는 event.ignore()로 창 닫기를 무시할 수 있습니다.
        
    #마우스 이벤트 처리 (가상키보드 처리)
    def mousePressEvent(self, event):
        # 키보드가 켜져있을 때, 배경 클릭 이벤트
        if self.pwdInput.hasFocus() and not self.qml_widget.underMouse():
            self.qml_widget.setVisible(False)
            self.setFocus()
        super().mousePressEvent(event)
    
    #특정 이벤트 처리
    def eventFilter(self, source, event):
        #F11을 눌렀을 때, 전체화면
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
            return True
        #pwdInput의 focus가 설정되면 키보드가 보이게 함
        if event.type() == QEvent.FocusIn and source == self.pwdInput:
            self.qml_widget.setVisible(True)
        elif event.type() == QEvent.FocusOut and source == self.pwdInput:
            # FocusOut이 발생한 후의 새로운 포커스가 pwdInput 내부가 아닌 경우에만 가상 키보드를 숨김
             if not self.qml_widget.underMouse():
                self.qml_widget.setVisible(False)
            
        return super().eventFilter(source, event)
        
    # WifiPage로 가는 함수
    def goToWifiPage(self):
    
        if(signInFlag==True):
            self.BackButton_2.setVisible(True)
            
        self.stackedWidget.setCurrentIndex(0)
    
    # Wifi를 선택할 수 있는 Page로 가는 함수
    def goToWifiSelectPage(self):
        self.stackedWidget.setCurrentIndex(1)
        self.setFocus()
    
    # Wifi에 연결 시도 하는 함수
    def connectToWifi(self, ssid, password):
        """주어진 SSID와 비밀번호를 사용하여 WiFi 네트워크에 연결"""
        """cmd_list_connections = [
            "sudo", "nmcli", "-t", "-f", "NAME,TYPE", "connection", "show", "--active"
            ]

        # 명령어 실행
        result = subprocess.run(cmd_list_connections, capture_output=True, text=True)

        # 필터링된 네트워크 이름을 저장할 리스트
        wifi_names = [
            line.split(':')[0]
            for line in result.stdout.splitlines()
            if "wireless" in line
        ]
        
        try:
            # 각 Wi-Fi 네트워크를 비활성화합니다.
            for name in wifi_names:
                cmd_down = [
                   "sudo",  "nmcli", "connection", "delete", "id", name
                ]
                # 명령어 실행
                subprocess.run(cmd_down,timeout=10)
    
                print(f"Disconnected from: {name}")
        except subprocess.TimeoutExpired:
            
            pass"""
            
        # WiFi 연결 명령어
        try:
            cmd = [
                'sudo', 'nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
            output = result.stdout
            error = result.stderr
            print(type(result.returncode),flush=True)
            
        except subprocess.TimeoutExpired:
            print("Connection attempt timed out.")
            
            return False
            
        except:
        
            return False    
        if result.returncode == 0:
        
            return True
        else:
            
            return False
    #ESP32의 AP 접속 및 wifi 연결 시도        
    def setESPWifi(self,ssid, pwd):
        
        if(not self.connectToWifi(ap_ssid,ap_password)):
            return False
        
        data = {
            'ssid': ssid,          # SSID 값
            'password': pwd   # 비밀번호 값
        }
        url = f'{ap_url}/submit'
        
        response = requests.post(url, data=data)
        print(response.text,flush=True)
        # 응답 상태 코드 출력
        if(response.status_code==200):
        
            cmd_down = [
                   "sudo",  "nmcli", "connection", "delete", "id", ap_ssid
            ]
                # 명령어 실행
            subprocess.run(cmd_down,timeout=10)
            return True
        else:
            return False
            
    #Jetson의 AP 접속 및 wifi 연결 시도
    def setJetsonWifi(self,ssid, pwd):
        
        if(not self.connectToWifi(jetson_ssid,jetson_password)):
            return False

        data = {
            'ssid': ssid,          # SSID 값
            'password': pwd   # 비밀번호 값
        }
        url = f'{jetson_url}/wifi_setup'
        response = requests.post(url, data=data)
        # 응답 상태 코드 출력
        cmd_down = [
                   "sudo",  "nmcli", "connection", "delete", "id", jetson_ssid
        ]
                # 명령어 실행
        subprocess.run(cmd_down,timeout=10)
        return True 

    # QR Page에 가기 위한 함수
    def goToQRPage(self):
        
        
        #만약 pwdInput에 아무것도 입력하지 않았으면 오류 메시지 출력
        if(len(self.pwdInput.text())==0):
            self.WarningText.setVisible(True)
            return
        else:
            self.WarningText.setVisible(False)
        
        # 만약 이미 회원가입을 했다면 라즈베리파이의 wifi만 연결 시도 
        if(signInFlag):
        
            while(self.connectToWifi(self.networkName.text(),self.pwdInput.text())):
                self.stackedWidget.setCurrentIndex(3)
                return
            
            # 연결 불가 시 재시도 요청
            self.stackedWidget.setCurrentIndex(1)
            self.WarningText_2.setVisible(True)
            return
        
        self.yesButton_1.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));\n"
"image: url(:/icon/icon/loading.png);")
        self.yesButton_1.setText("")
        QApplication.processEvents()
        
        attemps=0
        
        # 회원가입을 하지 않았을 경우 선택한 와이파이에 대한 연결 시도
        while(self.connectToWifi(self.networkName.text(),self.pwdInput.text()) and attemps<=3 ):
            attemps+=1
            self.WarningText_2.setVisible(False)
            self.stackedWidget.setCurrentIndex(10)
            QApplication.processEvents()
            
            # 적절한 와이파이임이 확인되면, jetson AP 연결 및 wifi 연결 시도
            if(not self.jetsonflag):
                if(not self.setJetsonWifi(self.networkName.text(),self.pwdInput.text())):
                    continue
                else:
                    self.jetsonflag=True
            
            # 적절한 와이파이임이 확인되면, esp32 AP 연결 및 wifi 연결 시도    
            if(not self.espflag):
                if(not self.setESPWifi(self.networkName.text(),self.pwdInput.text())):
                    continue
                else:
                    self.espflag=True
            
            # 모두 연결되고, 라즈베리파이까지 마지막에 연결이 되면, QR 페이지로 
            if(self.connectToWifi(self.networkName.text(),self.pwdInput.text())):
            
                self.stackedWidget.setCurrentIndex(2)
                self.yesButton_1.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
                self.yesButton_1.setText(QCoreApplication.translate("MainWindow", u"\ud655\uc778", None))
                QApplication.processEvents()
                self.setFocus()
                
                # mqtt Process와 touch Process를 실행
                self.mqttProcess.start("python", ["-u", "/home/pi/mqtt/test3.py"])
                self.touchProcess.start("python", ["-u", "/home/pi/touchex/touchex2.py"]) 
                return
        
        self.stackedWidget.setCurrentIndex(1)
        self.WarningText_2.setVisible(True)
        

        self.yesButton_1.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.yesButton_1.setText(QCoreApplication.translate("MainWindow", u"\ud655\uc778", None))
        QApplication.processEvents()
        self.setFocus()
        

    # 회원가입 전 초기페이지 
    def goToWelcomePage(self):
        self.stackedWidget.setCurrentIndex(12)
        self.setFocus()
    
    # wifi를 선택할 수 있는 페이지
    def goToNetworkPage(self):
        if(not signInFlag and (not self.WelcomeText_3.isVisible())):
            self.WelcomeText_3.setVisible(True)
            return
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.setFocus()
        
    # Main Page
    def goToMainPage(self):
        global petName, signInFlag, personality
        
        subprocess.run(["python3", "/home/pi/mqtt/display.py", personality])
        
        if(not signInFlag):
            self.QRText3.setVisible(True)
            return
        else:
            self.QRText3.setVisible(False)
            
        if(lan == "Korean"):
            name = f"안녕하세요 {petName}'s 가방이에요!"
        else:
            name = f"Welcome {petName}'s Bag!"
        #encodinddddg=name.encode('unicode_escape').decode('latin-1')
        #unicode_str = encoding.encode('latin-1').decode('unicode_escape')
        #unicode_str = name.encode('unicode_escape')
        self.greetings.setText(QCoreApplication.translate("MainWindow", name, None))
        self.dateText_3.setText(self.date_part)  # 날짜 부분 업데이트
        self.timeText_3.setText(self.time_part)  # 시간 부분 업데이트
        QApplication.processEvents()
        
        
        self.stackedWidget.setCurrentIndex(3)
        self.setFocus()
        if(not (self.touchProcess.state() == QProcess.Running)):
            self.touchProcess.start("python", ["-u", "/home/pi/touchex/touchex2.py"])
        # 음성인식이 꺼져있다면 키기 
        if(not self.speech_thread.stop_listening):
            self.speech_thread.start()
        
    # 일기 작성 페이지
    def goToDiaryPage(self):
        self.dateText_7.setText(self.date_part)  # 날짜 부분 업데이트
        self.timeText_7.setText(self.time_part)  # 시간 부분 업데이트
        self.stackedWidget.setCurrentIndex(7)
        self.setFocus()
        
    # 일기 작성 중 페이지
    def goToDiaryIngPage(self):
        self.deleteAllDiaryText()
        self.diaryTextnum=0
        self.mqttProcess.write(b'pause\n') # MQTT 프로세스를 잠시 정지
        
        # 음성인식 쓰레드를 중지
        if self.speech_thread.stop_listening:
            self.speech_thread.stop()
        
        # 일기 작성 Process를 시작
        self.diaryProcess.start("python", ["-u", "/home/pi/mqtt/writingDiary2.py"])
        
        self.dateText_8.setText(self.date_part)  # 날짜 부분 업데이트
        self.timeText_8.setText(self.time_part)  # 시간 부분 업데이트
        
        self.stackedWidget.setCurrentIndex(8)
        self.setFocus()
        
    # 일기 작성 완료 페이지
    def goToCompletePage(self):
        self.dateText_9.setText(self.date_part)  # 날짜 부분 업데이트
        self.timeText_9.setText(self.time_part)  # 시간 부분 업데이트
        
        self.diaryProcess.write(b'complete\n')
        self.mqttProcess.write(b'resume\n')
        self.stackedWidget.setCurrentIndex(9)
        self.setFocus()
    
    # 메인 페이지로 다시 돌아가기 위한 함수
    def diaryComplete(self):
        if(self.diaryProcess.state() == QProcess.Running):
            self.diaryProcess.write(b'stop\n')
        self.goToMainPage()
              
    # 시스템 설정 페이지
    def goToSystemPage(self):
        self.dateText_5.setText(self.date_part)  # 날짜 부분 업데이트
        self.timeText_5.setText(self.time_part)  # 시간 부분 업데이트
        
        self.stackedWidget.setCurrentIndex(5)
        self.setFocus()
        
    # 에버펫 정보 페이지
    def goToInfoPage(self):
    
        global lan
    
        if(lan=="English"):
            self.genderValue.setText(QCoreApplication.translate("MainWindow", KoToEn[gender], None))
        else:
            self.genderValue.setText(QCoreApplication.translate("MainWindow", gender, None))

        if(lan=="English"):
            self.typeValue.setText(QCoreApplication.translate("MainWindow", KoToEn[personality], None))
        else:
            self.typeValue.setText(QCoreApplication.translate("MainWindow", personality, None))
        self.dateText_6.setText(self.date_part)  # 날짜 부분 업데이트
        self.timeText_6.setText(self.time_part)  # 시간 부분 업데이트
        
        self.stackedWidget.setCurrentIndex(6)
        self.setFocus()
        
    # 설정 페이지
    def goToSettingPage(self):
    
        self.dateText_4.setText(self.date_part)  # 날짜 부분 업데이트
        self.timeText_4.setText(self.time_part)  # 시간 부분 업데이트
        
        self.stackedWidget.setCurrentIndex(4)
        
        self.setFocus()
    
    # wifi 비밀번호 입력 시 토글버튼
    def secretToggle(self, *arg, **kwargs):
        self.pwdVisible=not(self.pwdVisible)
        
        if(not self.pwdVisible):
          self.pwdInput.setEchoMode(QLineEdit.EchoMode.Password)
          self.pwdImage.setStyleSheet(u"border:0px;\n"
"color:rgb(121, 121, 121);\n"
"background-color:transparent;\n"
"image: url(:/icon/icon/eye_close.png);")
        else:
          self.pwdInput.setEchoMode(QLineEdit.EchoMode.Normal)
          self.pwdImage.setStyleSheet(u"border:0px;\n"
"color:rgb(121, 121, 121);\n"
"background-color:transparent;\n"
"image: url(:/icon/icon/eye_open.png);")   
        pass
        
    # wifi 버튼을 누르면 와이파이이름을 고려한 선택 페이지로 
    def connectTry(self,name):
        
        self.goToWifiSelectPage()
        self.networkName.setText(name)
        
    # wifi를 다시 스캔하는 함수
    def reLoadWifi(self):
    
        # 스캔중 이라는 문구 보이도록 함
        self.scanText.setVisible(True)
        QApplication.processEvents()
        self.deleteAllWifiButton()
        
        
        self.wifi_list = self.scanWifiNetworks()
        font = QFont()
        font.setPointSize(15)
        
        #만약 스캔 된 와이파이가 없으면 문구 출력
        if(len(self.wifi_list)==0):
          self.nonNetwork.setVisible(True)   
         
        else:
          self.nonNetwork.setVisible(False)
          
          i=0
          
          # 와이파이 리스트에 해당하는 버튼들을 생성 
          for wifi_name in self.wifi_list:
            button = QPushButton(self.scrollAreaWidgetContents_3)
            button.setObjectName(u"WIFIButton{i}")
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
            
            button.setSizePolicy(sizePolicy)
            button.setMinimumSize(QSize(611, 27))
            button.setMaximumSize(QSize(611, 131))
            button.setFont(font)
            button.setStyleSheet(u"image: url(:/icon/icon/wifi_lock.png);\n"
"image-position:left;\n"
"background-color : rgb(254, 252, 247);")
            self.buttons.append(button)
            #encoding=wifi_name.encode('unicode_escape').decode('latin-1')
            #unicode_str = encoding.encode('latin-1').decode('unicode_escape')
            button.setText(QCoreApplication.translate("MainWindow", wifi_name , None))
            self.verticalLayout_6.addWidget(button)
            button.clicked.connect(partial(self.connectTry, wifi_name))
            
            i+=1
            
        self.scanText.setVisible(False)
        
    #WiFi 네트워크를 스캔하여 이름 목록을 반환
    def scanWifiNetworks(self):
        
        try:
            # 'sudo nmcli dev wifi list' 명령어를 사용하여 WiFi 목록 가져오기
            result = subprocess.run(['sudo', 'nmcli', '-t', '-f', 'SSID,ACTIVE', 'dev', 'wifi'], 
                                    stdout=subprocess.PIPE, text=True)
            output = result.stdout
            
            # WiFi 이름 목록 반환
            wifi_names = set()  # 중복 제거를 위해 set 사용
            for line in output.split('\n'):
                if line.strip():
                    ssid, active = line.split(':')
                    if(len(ssid)==0):
                        continue
                    wifi_names.add(ssid.strip())
            return list(wifi_names)
            
        except Exception as e:
            print(f"Error scanning WiFi networks: {e}",flush=True)
            return []
    def cancelSettings(self):
    
        global lan, sound
        
        language = lan
        setting_sound = sound
        
        if(language=="영어"):
            language="English"
        elif(language=="한국어"):
            language="Korean"
        
        
        self.comboBox.setCurrentText(language)
        self.soundSlider.setValue(setting_sound)
        self.soundValue.setNum(setting_sound)
        
        self.goToSettingPage()
        
    def setSettings(self):
    
        global settings_data, lan, sound
        
        settings_data = read_allinfo("/home/pi/settings.json")
        
        lang = settings_data["language"]
        
        language = self.comboBox.currentText()
        
        if(language=="영어"):
            language="English"
        elif(language=="한국어"):
            language="Korean"
        
        if(lang != language):
            settings_data["language"]=language
            write_allinfo("/home/pi/settings.json",settings_data)
            self.setLabels(language)
            lan=language
            QApplication.processEvents()
            
            current_time = QTime.currentTime()
            hour = current_time.hour()
            second = current_time.second()
            
            if hour < 12:
                if language=="English":
                    period="AM"
                else:
                    period = "\uC624\uC804"  # "오전"의 유니코드
            else:
                if language=="English":
                    period="PM"
                else:
                    period = "\uC624\uD6C4"  # "오후"의 유니코드
            
            hour_12 = hour % 12
            if hour_12 == 0:
                hour_12 = 12
            

            time_str = f"{period} {hour_12}:{current_time.toString('mm')}"
            current_date_time = QDate.currentDate().toString("yyyy-MM-dd/") + time_str
        
            self.date_part, self.time_part = current_date_time.split('/')
        
        setting_sound = settings_data["sound"]
        
        if(setting_sound!=self.soundSlider.value()):
            sound = self.soundSlider.value()
            settings_data["sound"]=self.soundSlider.value()
            write_allinfo("/home/pi/settings.json",settings_data)
            subprocess.run(["amixer", "set", "Master", f"{self.soundSlider.value()}%"])
    
        self.goToSettingPage()
            
            
    def deleteAllDiaryText(self):
        self.diaryTexts.clear()
        while self.verticalLayout_4.count():
            item = self.verticalLayout_4.takeAt(0)
            widget = item.widget()

            widget.deleteLater()
        
        
    # 모든 wifi button을 삭제 하는 함수 (새로 스캔하기 위함)
    def deleteAllWifiButton(self):
        self.buttons.clear()
        while self.verticalLayout_6.count():
            item = self.verticalLayout_6.takeAt(0)
            widget = item.widget()

            widget.deleteLater()
        
    def main(self):
        pass
    def setLabels(self,language):
        
        if(language=="English"):
            
            self.networkText1.setText(QCoreApplication.translate("MainWindow", u"Network", None))
            self.scanText.setText(QCoreApplication.translate("MainWindow", u"Scanning!", None))
            self.networkText.setText(QCoreApplication.translate("MainWindow", u"Network Setting", None))
            self.nonNetwork.setText(QCoreApplication.translate("MainWindow", u"Network not found!", None))
            self.pwdText.setText(QCoreApplication.translate("MainWindow", u"Password", None))
            self.yesButton_1.setText(QCoreApplication.translate("MainWindow", u"OK", None))
            self.pwdInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Click here and enter your password", None))
            self.WarningText.setText(QCoreApplication.translate("MainWindow", u"Please enter your password!", None))
            self.WarningText_2.setText(QCoreApplication.translate("MainWindow", u"Connection failed. Please try again!", None))
            self.connectText_2.setText(QCoreApplication.translate("MainWindow", u"This may take 5-10 minutes!", None))
            self.connectText.setText(QCoreApplication.translate("MainWindow", u"Setting up your EverPet!!", None))
            self.nextButton_2.setText(QCoreApplication.translate("MainWindow", u"Next", None))
    
            self.QRText2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "hr { height: 1px; border-width: 0; }\n"
    "li.unchecked::marker { content: \"\\2610\"; }\n"
    "li.checked::marker { content: \"\\2612\"; }\n"
    "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Once Sign Up is completed, the Screen will automatically change.</span></p>\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">if the screen not change, press the [Next] Button.</span></p></body></html>", None))
    
            self.QRText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "hr { height: 1px; border-width: 0; }\n"
    "li.unchecked::marker { content: \"\\2610\"; }\n"
    "li.checked::marker { content: \"\\2612\"; }\n"
    "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text\"></a><span style=\" font-family:'inherit'; font-size:28px; font-weight:700; color:#1f1f1f;\">B</span><span style=\" font-family:'inherit'; font-size:28px; font-weight:700; color:#1f1f1f;\">y recognizing QR</span></p>\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font"
                            "-family:'inherit'; font-size:28px; font-weight:700; color:#1f1f1f;\">Please sign up!</span></p></body></html>", None))
    
            self.logoImage_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><a href=\"123\"><span style=\" text-decoration: underline; color:#0078d7;\">.</span></a></p></body></html>", None))
    
            self.QRText3.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "hr { height: 1px; border-width: 0; }\n"
    "li.unchecked::marker { content: \"\\2610\"; }\n"
    "li.checked::marker { content: \"\\2612\"; }\n"
    "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
    "<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700; color:#ff0000;\">Not yet registered</span></p>\n"
    "<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700; color:#ff0000;\">Not completed</span></p></body></html>", None))
    
            self.greetings.setText(QCoreApplication.translate("MainWindow", u"\uc548\ub155\ud558\uc138\uc694 \uc9f1\uc6a9\uc774 \uac00\ubc29\uc774\uc5d0\uc694", None))
    
            """self.weatherText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "hr { height: 1px; border-width: 0; }\n"
    "li.unchecked::marker { content: \"\\2610\"; }\n"
    "li.checked::marker { content: \"\\2612\"; }\n"
    "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:25pt; font-weight:400; font-style:normal;\">\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt;\">H : 29\u2103</span></p>\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt;\">L : 23\u2103</span></p></body></html>", None))"""
    
            self.diaryText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:33pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Writing</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Diaries</p></body></html>", None))
    
            self.settingText.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
            self.settingPageText.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
    
            self.infoText.setText(QCoreApplication.translate("MainWindow", u"EverPet", None))
            self.systemText.setText(QCoreApplication.translate("MainWindow", u"System", None))
            self.cancelButton_4.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
            self.networkText_2.setText(QCoreApplication.translate("MainWindow", u"Network", None))
            self.systemPageText.setText(QCoreApplication.translate("MainWindow", u"System Setting", None))
    
            self.soundValue.setText(QCoreApplication.translate("MainWindow", u"0", None))
            self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Korean", None))
            self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"English", None))
            self.comboBox.setCurrentIndex(1)
    
            self.cancelButton_5.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
            self.yesButton_5.setText(QCoreApplication.translate("MainWindow", u"OK", None))
            
            self.infoPageText.setText(QCoreApplication.translate("MainWindow", u"EverPet Info", None))
    
            self.nameText.setText(QCoreApplication.translate("MainWindow", u"Name", None))
    
            self.genderText.setText(QCoreApplication.translate("MainWindow", u"Gender", None))
    
            self.typeText.setText(QCoreApplication.translate("MainWindow", u"Personality", None))
    
            self.cancelButton_6.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
    
            self.diaryText_7.setText(QCoreApplication.translate("MainWindow", u"Writing Diaries", None))
    
            self.diaryText_7_1.setText(QCoreApplication.translate("MainWindow", u"Would you like to keep a diary?", None))
            self.diaryButton_7.setText(QCoreApplication.translate("MainWindow", u"Start writing", None))
            self.cancelButton_7.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
    
    
            self.diaryText_8.setText(QCoreApplication.translate("MainWindow", u"Writing Diaries", None))
    
            self.diaryText_8_1.setText(QCoreApplication.translate("MainWindow", u"Writing a diary....", None))
            self.diaryButton_8.setText(QCoreApplication.translate("MainWindow", u"Stop writing", None))
    
            self.diaryText_9.setText(QCoreApplication.translate("MainWindow", u"Writing Diaries", None))
    
            self.diaryText_9_1.setText(QCoreApplication.translate("MainWindow", u"The diary writing has been completed.", None))
            self.diaryButton_9.setText(QCoreApplication.translate("MainWindow", u"Home", None))
    
            self.WelcomeText.setText(QCoreApplication.translate("MainWindow", u"Welcome to EverPet!", None))
            self.nextButton_11.setText(QCoreApplication.translate("MainWindow", u"Next", None))
    
            self.WelcomeText_2.setText(QCoreApplication.translate("MainWindow", u"Please turn on the enclosed sensor!!", None))
            self.nextButton_12.setText(QCoreApplication.translate("MainWindow", u"Next", None))
            self.WelcomeText_3.setText(QCoreApplication.translate("MainWindow", u"Are you sure you turned on the sensor?", None))
        else:
            self.networkText1.setText(QCoreApplication.translate("MainWindow", u"\ub124\ud2b8\uc6cc\ud06c", None))
            self.WarningText.setText(QCoreApplication.translate("MainWindow", u"\ube44\ubc00\ubc88\ud638\ub97c \uc785\ub825\ud574\uc8fc\uc138\uc694!", None))
            self.WarningText_2.setText(QCoreApplication.translate("MainWindow", u"\uc5f0\uacb0\uc5d0 \uc2e4\ud328\ud588\uc2b5\ub2c8\ub2e4. \ub2e4\uc2dc \uc2dc\ub3c4\ud574\uc8fc\uc138\uc694!", None))
            self.scanText.setText(QCoreApplication.translate("MainWindow", u"\uc2a4\uce94\uc911!", None))
            self.nonNetwork.setText(QCoreApplication.translate("MainWindow",u"\uc874\uc7ac\ud558\ub294\u0020\u0057\u0049\u0046\u0049\uac00\u0020\uc5c6\uc2b5\ub2c8\ub2e4\u0021\u0021",None))
        
            self.networkText.setText(QCoreApplication.translate("MainWindow", u"\ub124\ud2b8\uc6cc\ud06c \uc124\uc815", None))
            self.connectText_2.setText(QCoreApplication.translate("MainWindow", u"5~10\ubd84 \uc815\ub3c4 \uc18c\uc694\ub420 \uc218 \uc788\uc2b5\ub2c8\ub2e4!", None))
            self.connectText.setText(QCoreApplication.translate("MainWindow", u"EverPet\uc744 \uc138\ud305\ud558\ub294 \uc911\uc785\ub2c8\ub2e4!", None))
            
            self.pwdText.setText(QCoreApplication.translate("MainWindow", u"\ube44\ubc00\ubc88\ud638", None))
            self.yesButton_1.setText(QCoreApplication.translate("MainWindow", u"\ud655\uc778", None))
           
            self.pwdInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\uc774 \ubd80\ubd84\uc744 \ud074\ub9ad\ud558\uace0 \ube44\ubc00\ubc88\ud638\ub97c \uc785\ub825\ud558\uc138\uc694", None))
          
            self.nextButton_2.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc74c", None))
            self.QRText2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "hr { height: 1px; border-width: 0; }\n"
    "li.unchecked::marker { content: \"\\2610\"; }\n"
    "li.checked::marker { content: \"\\2612\"; }\n"
    "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">\ud68c\uc6d0\uac00\uc785\uc774 \uc644\ub8cc\ub418\uba74 \uc790\ub3d9\uc73c\ub85c \ud654\uba74\uc774 \ubc14\ub01d\ub2c8\ub2e4.</span></p>\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">\ud654\uba74\uc774 \ubc14\ub00c\uc9c0 \uc54a\uc744 \uacbd\uc6b0"
                            " [\ub2e4\uc74c] \ubc84\ud2bc\uc744 \ub20c\ub7ec\uc8fc\uc138\uc694.</span></p></body></html>", None))
            self.QRText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "hr { height: 1px; border-width: 0; }\n"
    "li.unchecked::marker { content: \"\\2610\"; }\n"
    "li.checked::marker { content: \"\\2612\"; }\n"
    "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:700;\">QR\uc744 \uc778\uc2dd\ud558\uc5ec</span></p>\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:700;\">\ud68c\uc6d0\uac00\uc785\uc744 \ud574\uc8fc\uc138\uc694!</span></p></body></html>", None))
            
            self.QRText3.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "hr { height: 1px; border-width: 0; }\n"
    "li.unchecked::marker { content: \"\\2610\"; }\n"
    "li.checked::marker { content: \"\\2612\"; }\n"
    "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
    "<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700; color:#ff0000;\">\uc544\uc9c1 \ud68c\uc6d0\uac00\uc785\uc774</span></p>\n"
    "<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700; color:#ff0000;\">\uc644\ub8cc\ub418\uc9c0 \uc54a\uc558\uc2b5\ub2c8"
                            "\ub2e4</span></p></body></html>", None))
            self.settingText.setText(QCoreApplication.translate("MainWindow",u"\uc124\uc815", None))
            self.greetings.setText(QCoreApplication.translate("MainWindow", u"\uc548\ub155\ud558\uc138\uc694 \uc9f1\uc6a9\uc774 \uac00\ubc29\uc774\uc5d0\uc694", None))
            self.logoImage_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><a href=\"123\"><span style=\" text-decoration: underline; color:#0078d7;\">.</span></a></p></body></html>", None))
            """self.weatherText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "hr { height: 1px; border-width: 0; }\n"
    "li.unchecked::marker { content: \"\\2610\"; }\n"
    "li.checked::marker { content: \"\\2612\"; }\n"
    "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:25pt; font-weight:400; font-style:normal;\">\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt;\">H : 29\u2103</span></p>\n"
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt;\">L : 23\u2103</span></p></body></html>", None))"""

            self.diaryText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "hr { height: 1px; border-width: 0; }\n"
    "li.unchecked::marker { content: \"\\2610\"; }\n"
    "li.checked::marker { content: \"\\2612\"; }\n"
    "</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:33pt; font-weight:400; font-style:normal;\">\n"
    "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">\ub2e4\uc774\uc5b4\ub9ac</span></p>\n"
    "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">\uc791\uc131</span></p></body></html>", None))
            
            self.settingPageText.setText(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
            self.networkText_2.setText(QCoreApplication.translate("MainWindow", u"\ub124\ud2b8\uc6cc\ud06c", None))
          
            self.infoText.setText(QCoreApplication.translate("MainWindow", u"\uc5d0\ubc84\ud3ab", None))
            self.systemText.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc2a4\ud15c", None))
            self.cancelButton_4.setText(QCoreApplication.translate("MainWindow", u"\ucde8\uc18c", None))
           
            self.systemPageText.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc2a4\ud15c \uc124\uc815", None))
            self.soundValue.setText(QCoreApplication.translate("MainWindow", u"0", None))
            self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\ud55c\uad6d\uc5b4", None))
            self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\uc601\uc5b4", None))
            self.comboBox.setCurrentIndex(0)
            
            self.cancelButton_5.setText(QCoreApplication.translate("MainWindow", u"\ucde8\uc18c", None))
            self.yesButton_5.setText(QCoreApplication.translate("MainWindow", u"\ud655\uc778", None))
            
           
            self.infoPageText.setText(QCoreApplication.translate("MainWindow", u"\uc5d0\ubc84\ud3ab \uc815\ubcf4", None))
           
            self.nameText.setText(QCoreApplication.translate("MainWindow", u"\uc774\ub984", None))
            
            self.genderText.setText(QCoreApplication.translate("MainWindow", u"\uc131\ubcc4", None))
        
            self.typeText.setText(QCoreApplication.translate("MainWindow", u"\uc131\uaca9", None))
            
            self.cancelButton_6.setText(QCoreApplication.translate("MainWindow", u"\ucde8\uc18c", None))
         
            self.diaryText_7.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131", None))
            
            self.diaryText_7_1.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac\ub97c \uc791\uc131 \ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", None))
            self.diaryButton_7.setText(QCoreApplication.translate("MainWindow", u"\uc791\uc131 \uc2dc\uc791", None))
            self.cancelButton_7.setText(QCoreApplication.translate("MainWindow", u"\ucde8\uc18c", None))
            
            self.diaryText_8.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131", None))

            self.diaryText_8_1.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131 \uc911....", None))
            self.diaryButton_8.setText(QCoreApplication.translate("MainWindow", u"\uc791\uc131 \uc885\ub8cc", None))
           
            self.diaryText_9.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131", None))
          
            self.diaryText_9_1.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131 \uc911 \uc785\ub2c8\ub2e4.", None))
            self.diaryButton_9.setText(QCoreApplication.translate("MainWindow", u"\ud648", None))
            self.logoImage_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><a href=\"123\"><span style=\" text-decoration: underline; color:#0078d7;\">.</span></a></p></body></html>", None))

            self.WelcomeText.setText(QCoreApplication.translate("MainWindow", u"EverPet\uc5d0 \uc624\uc2e0 \uac83\uc744 \ud658\uc601\ud569\ub2c8\ub2e4", None))
            self.nextButton_11.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc74c", None))
            self.logoImage_12.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><a href=\"123\"><span style=\" text-decoration: underline; color:#0078d7;\">.</span></a></p></body></html>", None))
            self.WelcomeText_2.setText(QCoreApplication.translate("MainWindow", u"\ub3d9\ubd09\ub41c \uc13c\uc11c\uc758 \uc804\uc6d0\uc744 \ucf1c\uc8fc\uc138\uc694!!", None))
            self.nextButton_12.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc74c", None))
            self.WelcomeText_3.setText(QCoreApplication.translate("MainWindow", u"\ud655\uc2e4\ud558\uac8c \ud0a4\uc168\ub098\uc694?", None))
        

if __name__ == '__main__':
    
    allinfo_data = read_allinfo("/home/pi/allinfo.json")
    
    gender=allinfo_data['robot']['gender']
    humanName=allinfo_data['user']['userName']
    petName=allinfo_data['robot']['name']
    intimacy=allinfo_data['friendship']['current']
    personality=allinfo_data['robot']['personality']
    
    daytalking=read_allinfo("/home/pi/talkingNum.json")
    serialNum = allinfo_data['robot']['serialNumber']
    settings_data = read_allinfo("/home/pi/settings.json")
    
    wifiSsid = settings_data['wifi']['ssid']
    wifiPwd = settings_data['wifi']['password']
    lan = settings_data["language"]
    sound = settings_data["sound"]
    signInFlag = settings_data["signIn"]
    
    private_data = read_allinfo("/home/pi/private.json")
    ap_url = private_data["esp32"]["url"]
    jetson_url=private_data["jetson"]["url"]
    
    ap_ssid = private_data["esp32"]["ssid"]
    ap_password = private_data["esp32"]["password"]
    
    jetson_ssid = private_data["jetson"]["ssid"]
    jetson_password = private_data["jetson"]["password"]
    
    serverIP=private_data["server"]["ip"]
    # 폼 데이터 전송 URL
    OPENAI_API_KEY = private_data["openai"]["key"]
    
    # openai API 키 인증
    openai.api_key = OPENAI_API_KEY
    app = QApplication([])
    win = MyApp()
    win.show()

    app.exec_()
