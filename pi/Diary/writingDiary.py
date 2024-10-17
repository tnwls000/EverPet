import openai
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import webbrowser
import urllib.request
import time
import requests
import json
import threading
import queue
import sys
import subprocess


model = "gpt-4o"

#음성 데이터를 담을 queue
audio_queue = queue.Queue()
# signal을 담을 queue
signal_queue = queue.Queue()

stop_listening=None
listening_thread=None

# 음성인식을 한 텍스트를 담을 변수
transcription = ""

#JSON 파일을 읽는 함수
def read_allinfo(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data=json.load(f)
    return data
#JSON 파일에 data를 저장하는 함수
def write_allinfo(file_path, data):
    try:
        with open(file_path,'w',encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        #print(f"Data has been written to {file_path}")
    except Exception as e:
        #print(f"Error writing to Json file: {e}")
        pass
        
# Text를 음성파일로 바꾸어주는 함수
# gTTS를 활용 (google Text To Speech)
def text_to_speech(text, lang='ko'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")

# 음성파일을 스피커로 실행하도록 하는 함수
def play_audio(file_path, speed=1.3):
    audio = AudioSegment.from_file(file_path, format="mp3")
    new_audio = audio.speedup(playback_speed=speed)
    play(new_audio)
    #os.remove(file_path)

# DALL-E-3 에게 받은 이미지를 서버에게 HTTP로 전송
def send_image(text, image_path, userID):
    global image_url
    
    with open(image_path, 'rb') as img_file:
        files = {
            'image': ('result.jpg', img_file, 'image/jpeg')
        }
        data = {
            'userId': userID,
            'content': text
        }
        
        response = requests.post(image_url, files=files, data=data)
    
    if response.status_code == 200:
        #print("Image successfully sent!")
        pass
    else:
        #print(f"Failed to send image. Status code: {response.status_code}")
        pass
    
# complete signal로 모든 쓰레드가 종료되었을 때 일기 작성 시작    
def write_diary():
    # 이때 까지 인식된 텍스트
    global transcription
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # 프롬프트와 같이 넘길 로봇과 사용자의 정보 파싱
    allinfo_data = read_allinfo("/home/pi/allinfo.json")
    gender=allinfo_data['robot']['gender']
    humanName=allinfo_data['user']['userName']
    humanGender=allinfo_data['user']['userGender']
    humanAge=allinfo_data['user']['userAge']
    petName=allinfo_data['robot']['name']
    intimacy=allinfo_data['friendship']['current']
    personality=allinfo_data['robot']['personality']
    userID=allinfo_data['user']['userID']
            
    temp_response = {
        "success": True,
        "error": None,
        "transcription" : transcription
    }
    
    # Dall-e-3 모델에게 해당하는 프롬프트에 따라 이미지 생성 요청
    response = openai.Image.create(
        model="dall-e-3",
        prompt="내 이름은 "+humanName+". 내 성별은 "+humanGender+". 내 나이는 "+str(humanAge)+"세. 내가 일기를 썼어. 너는 내 일기 내용을 가지고 크레파스로 그림을 그려주는 7살짜리 꼬마야. 귀여운 느낌으로 그려줘. 너가 그린 그림을 보여줘. 내 일기 내용:"+transcription,
        size="1024x1024",
        n=1,
    )
    
    url = response['data'][0]['url']

    img_dest = "./result.jpg"
    #start = time.time()
    
    # 이미지를 받아옴
    # 이미지를 받아오는데 5~7초 가량 소요 됌
    urllib.request.urlretrieve(url, img_dest)
    
    #end = time.time()
    #print(f"총 소요시간 {end - start}초") 
    
    image_path = "./result.jpg"
    
    send_image(transcription, image_path, userID)
    text_to_speech("일기 작성 완료되었습니다!")
    play_audio("output.mp3")
    
    # 오늘 다이어리를 작성했다는 flag를 저장
    diarydone=read_allinfo("/home/pi/diaryDone.json")
    diarydone["todayDiary"]="True"
    write_allinfo("/home/pi/diaryDone.json",diarydone)
    
    # 다이어리 작성이 끝났음을 GUI 프로세스에게 신호 전달
    print("complete")
    
# 입력 시그널에 따른 쓰레드 함수
def handle_stdin_input():
    global stop_listening
    while True:
        command = sys.stdin.readline().strip()
        # 입력이 complete가 들어오면 신호 큐에 complete 시그널을 삽입 후 종료
        if command == 'complete':
            signal_queue.put("complete")
            break
        # 입력이 complete가 들어오면 신호 큐에 stop 시그널을 삽입 후 종료
        elif command == 'stop':
            signal_queue.put("stop")
            break

# 쓰레드로 작동하고 있는 음성 인식 쓰레드가 마이크로 받은 데이터를 음성파일로 변환했을 때 작동하는 콜백함수
def callback(recognizer, audio):
    try:
        audio_queue.put(audio) #정상적으로 음성으로 인식된 음성 데이터를 큐에 저장
        
    except sr.UnknownValueError:
        #print("인식할 수 없음")
        pass
    except sr.RequestError as e:
        #print(f"API 요청 오류: {e}")
        pass   
         
# 음성인식을 할수 있도록 쓰레드를 생성하고 신호 큐에 따라 핸들링하는 쓰레드
def listen_for_audio():
    global stop_listening
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    global stop_listening
    
    # 음성 인식이 시작되었음을 알림
    text_to_speech("일기 작성을 시작합니다. 지금부터 말씀해주세요!")
    play_audio("output.mp3")
    
    # 음성 인식이 잘 되도록 초기 세팅 (많은 시도 끝에 적절한 조건 세팅)
    with microphone as source: 
        recognizer.adjust_for_ambient_noise(source) 
    recognizer.dynamic_energy_threshold = True  
    recognizer.energy_threshold = 3000
    recognizer.dynamic_energy_adjustment_ratio = 1.5
    
    #recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
    stop_listening = recognizer.listen_in_background(microphone, callback)
    
    while True:
        try:
            if not signal_queue.empty():
                signal = signal_queue.get_nowait()
                if signal == "stop":
                    stop_listening(wait_for_stop=False)  # 음성인식을 중지하는 중지함수
                    signal_queue.put("stop")
                    break
                elif signal == "complete":
                    #print("Received complete signal. Stopping listening.")
                    stop_listening(wait_for_stop=False)  # 음성인식을 중지하는 중지함수
                    signal_queue.put("complete") # main에게 일기 작성을 명령할 수 있게 신호 큐에 complete를 다시 넣어줌
                    break
        except queue.Empty:
            pass

def process_audio():
    global listening_thread
    global transcription
    recognizer1 = sr.Recognizer()
    while True:
        try:
            audio = audio_queue.get(timeout=1)  # 큐에 음성 데이터가 있을 때 까지 대기
            try:
                # 음성데이터가 존재하면 text로 변환하여 시작할 때 까지 지금의 텍스트를 축적
                recog_string = recognizer1.recognize_google(audio, language="ko-KR")
                print(recog_string)
                transcription += recog_string
                transcription += " "
                # 음성데이터를 텍스트로 변환하는데 성공하면 깨달았다는 감정표시
                subprocess.run(["python3", "/home/pi/mqtt/display.py", "more_realize"])
            
            except sr.UnknownValueError:
                # 음성데이터를 텍스트 변환할 수 없다면 모르겠다는 감정표시
                subprocess.run(["python3", "/home/pi/mqtt/display.py", "curious"])
                #print("Google Web Speech could not understand the audio")
            except sr.RequestError as e:
                #print(f"Could not request results from Google Web Speech; {e}")
                pass
        except queue.Empty:
            #audio queue에 아무것도 없고 음성인식 thread가 죽었다면 음성처리 쓰레드도 중지
            if not listening_thread.is_alive():
                break
                
            pass
                
if __name__ == "__main__":
    
    private_data = read_allinfo("/home/pi/private.json")
    
    image_url = private_data["server"]["url"]
    # 발급받은 API 키 설정
    OPENAI_API_KEY = private_data["openai"]["key"]
    
    # openai API 키 인증
    openai.api_key = OPENAI_API_KEY

    try: 
        # 입력 시그널에 따른 처리를 위한 쓰레드
        stdin_thread = threading.Thread(target=handle_stdin_input)
        stdin_thread.daemon = True
        stdin_thread.start()
        
        # 시그널에 따른 음성을 인식하기 위한 쓰레드
        listening_thread = threading.Thread(target=listen_for_audio)
        listening_thread.start()
    
        # 인식을 한 음성데이터를 Text로 변환하는 처리를 위한 쓰레드
        processing_thread = threading.Thread(target=process_audio)
        processing_thread.start()
    
        # Process_thread가 종료될 때 까지 대기
        # (Process_thread가 제일 마지막으로 종료되도록 설계했음)
        processing_thread.join()
        
        # 모든 쓰레드가 종료되었고, 마지막 signal에 complete가 담겨있다면 일기작성
        if not signal_queue.empty() and signal_queue.get_nowait() == "complete":
            write_diary()
            
    # ctrl+c 키에 의해 쓰레드들이 정상적으로 종료될 수 있도록 설계
    except KeyboardInterrupt:
        #print("KeyboardInterrupt received. Stopping threads...")
        signal_queue.put("stop")
        listening_thread.join()
        stdin_thread.join()
        processing_thread.join()
        #print("All threads have been stopped safely.")
