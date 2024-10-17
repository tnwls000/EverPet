import sys
sys.path.append('/usr/lib/python3/dist-packages')
import openai
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import subprocess
import webbrowser
import urllib.request
import time
import requests
import writingDiary
import json
# �߱޹��� API Ű ����
OPENAI_API_KEY = ""

# openai API Ű ����
openai.api_key = OPENAI_API_KEY

model = "gpt-4o"
humanName=""
petName=""
intimacy=0
personality=""
lastAnswer=""

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
    
def recognize_speech_from_mic():
    """����ũ�κ��� ������ �޾� �ؽ�Ʈ�� ��ȯ�ϴ� �Լ�"""

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    with microphone as source:
        print("������ �ּ���!!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language="ko-KR")
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API ��û ����"
    except sr.UnknownValueError:
        response["success"] = False
        response["error"] = "������ �ν��� �� �����ϴ�"

    return response

def text_to_speech(text, lang='ko'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")

def play_audio(file_path, speed=1.5):
    audio = AudioSegment.from_file(file_path, format="mp3")
    new_audio = audio.speedup(playback_speed=speed)
    play(new_audio)
    #os.remove(file_path)

def main():
    allinfo_data = read_allinfo("/home/pi/allinfo.json")
    global humanName, petName, intimacy, personality, lastAnswer
    gender=allinfo_data['robot']['gender']
    humanName=allinfo_data['user']['userName']
    petName=allinfo_data['robot']['name']
    intimacy=allinfo_data['friendship']['current']
    personality=allinfo_data['robot']['personality']
    daytalking=read_allinfo("/home/pi/talkingNum.json")
    print(daytalking["talkingNum"])
    print(personality)

    while True:
        response = recognize_speech_from_mic()
        if response["success"]:
            transcription = response["transcription"]
            print(f"�νĵ� ����: {transcription}")
            
            transcription="�ʴ� �ݷ������̰�, �̸��� "+petName+"�̾�. �׸��� ���� ������ �̸��� "+humanName+"�̾�. �ʴ� ���ο��� "+str(intimacy)+"/10000 ģ�е��� ������ �־�. �ʴ� 4���� ������ ���� �� �־� : Ȱ��, ģ��, ����, �ҽ�. Ȱ���� ������ ������ �ʴ� ���ο��� �ݸ��� ��. �׸��� ������ �̾߱⺸�� ���� �̾߱⸦ �ϴ� ���� ��������. �׷��� ������ ���ص� �� ��⿡ �����ϰ� ������ �̾�� ���ٴ� �װ� �ϰ� ���� ��⸦ ��. ģ���� ������ ������ �ʴ� ���ο��� �ݸ��� ��. �׸��� ������ ���� �착�� ����ϰ� ������ �����ִ� ���� �ݷ������� ��. ������ ������ ������ ���ο��� �ݸ��� ��. �׸��� ������ �ڽ��� ����ó�� ����. ���ο��� ������ ������, ���� ���� �̾�� ���� �ּ����� ������ ����. ��� ������ �ϴ� ��Ⱑ �ʶ� ���� ����� ���ٰ� ������. �ҽ��� ������ ������ �ʴ� ���ο��� ������ ��. �׸��� �ָ��� ������ �ٶ󺸰�, ������ ���ϸ� �޺��Ÿ��� �ٰ��ͼ� ���� �����. ������ ���� �ǰ��� �� ǥ�������� ����. ���� ���� �ϱ�� ��. ���� ������ Ȱ��, ģ��, ����, �ҽ� �߿� "+personality+"�̾�. ������ �� ���� �� �Ͱ��߾�. �׷��� �� �������� ������ ���߳��Ծ�. ���ο��� �λ�����. 1-2 �������� ����."
            messages = [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": transcription }]
            if "�ϱ�" in transcription:
                writingDiary.write_diary()
                daytalking["talkingNum"]=daytalking["talkingNum"]+1
            elif transcription == "����":
                text_to_speech("�ǽ��� �����մϴ�.")
                play_audio("output.mp3")
                break
            else:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    max_tokens=400,
                )
                answer = response['choices'][0]['message']['content']
                print(f"ChatGPT ����: {answer}")
                text_to_speech(f"{answer}")
                lastAnswer=answer
                play_audio("output.mp3", speed=1.5)
                daytalking["talkingNum"]=daytalking["talkingNum"]+1
            write_allinfo("/home/pi/talkingNum.json",daytalking)
            
        else:
            print(f"����: {response['error']}")

if __name__ == "__main__":
    main()

