import paho.mqtt.client as mqtt
import subprocess
import os
import concurrent.futures
import sys
import json
import threading

serialNum=""
paused = False
userID = ""


# JSON 파일을 읽어오는 함수
def read_allinfo(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Json 파일에 data를 작성하는 함수
def write_allinfo(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        #print(f"Data has been written to {file_path}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

# MQTT가 connect 되었을 때, 불리는 Callback 함수
def on_connect(client, userdata, flags, reason_code, properties):
    global serialNum, userID
    allinfo=read_allinfo("/home/pi/allinfo.json")
    serialNum=allinfo['robot']['serialNumber']
    userID=allinfo['user']['userID']
    print("Connected with result code " + str(reason_code))
    client.subscribe(serialNum+"/#")

# MQTT 브로커 서버에서 메시지가 올 때 불리는 Callback 함수
def on_message(client, userdata, msg):
    # 저장된 로봇의 serialNumber, 저장된 유저의 ID, MQTT 멈춤 여부
    global serialNum, userID, paused, serverIP
    
    # paused 상태라면 바로 리턴
    if paused:
        return
    
    #topic 분리
    topic = msg.topic
    temp=topic.split('/',1)
    topic=temp[1]
    
    # 메시지만 추출
    message = msg.payload.decode()
    
    # 회원가입 토픽이 왔을 때
    if topic == "raspberry/allinfo":
        try:
            json_data = json.loads(message)
            with open("/home/pi/allinfo.json", "w", encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            #print("JSON data saved to allinfo.json")

            personality = json_data['robot']['personality']
            
            # 기본 성격에 따른 눈모양 표시
            subprocess.run(["python3", "/home/pi/mqtt/display.py", personality])
            # GUI Process에게 json 파일을 저장 signal을 전해줌
            print("complete")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        return
    
    # 출입로그 - 들어왔을 때
    elif topic=="raspberry/doorEnter/In":
        # userID를 추가해 서버에서 받을 수 있도록 다시 Publish
        subprocess.run(["mosquitto_pub", "-h", serverIP, "-t", serialNum+"/web/doorEnter/In", "-m", userID+"/"+message])
        return
    # 출입로그 - 나갔을 때
    elif topic=="raspberry/doorEnter/Out":
        # userID를 추가해 서버에서 받을 수 있도록 다시 Publish
        subprocess.run(["mosquitto_pub", "-h", serverIP, "-t", serialNum+"/web/doorEnter/Out", "-m", userID+"/"+message])
        return
    # 유저의 정보를 수정한 토픽이 왔을 때
    elif topic=="raspberry/modify/user":
        
        json_data = json.loads(message)
        allinfo_data = read_allinfo("/home/pi/allinfo.json")
        allinfo_data['user']['userName']=json_data['user']['userName']
        allinfo_data['user']['userID']=json_data['user']['userID']
        allinfo_data['user']['userGender']=json_data['user']['userGender']
        allinfo_data['user']['userAge']=json_data['user']['userAge']
        write_allinfo("/home/pi/allinfo.json",allinfo_data)
        
        return
    # 로봇의 정보를 수정한 토픽이 왔을 때
    elif topic=="raspberry/modify/robot":
        json_data = json.loads(message)
        allinfo_data = read_allinfo("/home/pi/allinfo.json")
        allinfo_data['robot']['name']=json_data['robot']['name']
        allinfo_data['robot']['personality']=json_data['robot']['personality']
        allinfo_data['robot']['gender']=json_data['robot']['gender']
        allinfo_data['robot']['serialNumber']=json_data['robot']['serialNumber']
        write_allinfo("/home/pi/allinfo.json",allinfo_data)
        print("modify_robot")
        return
    script_path = f"{message}.py"
    if message=="userIn":
        print("userIn")
    elif os.path.exists(script_path):
        try:
            executor.submit(run_script, script_path)
        except Exception as e:
            print(f"Error submitting {script_path} for execution: {e}")
    else:
        print(f"No script found for message: {message}")

def handle_stdin_input():
    global paused
    while True:
        #GUI 프로세스에서 pause 입력이 오면, MQTT를 잠시 멈추도록 설정
        command = sys.stdin.readline().strip()
        if command == 'pause':
            paused = True
        #GUI 프로세스에서 resume 입력이 오면, MQTT를 다시 실행
        elif command == 'resume':
            paused = False

# 지정한 py 파일을 실행하도록 하는 함수 
def run_script(script_path):
    try:
        result = subprocess.run(["python3", script_path], check=True)
        print(f"{script_path} finished execution with return code {result.returncode}.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")
        
if __name__ == "__main__":
    
    sys.stdout.flush()
    # MQTT 클라이언트 설정
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    
    settings_data = read_allinfo("/home/pi/private.json")
    serverIP = settings_data["server"]["ip"]
    # 브로커에 연결
    client.connect(serverIP, 1883, 60)

    # 입력에 따라 처리하도록 Thread 생성
    stdin_thread = threading.Thread(target=handle_stdin_input)
    stdin_thread.daemon = True
    stdin_thread.start()

    # 메시지 루프 시작
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    client.loop_forever()

    # Thread가 종료 될 때 까지 실행
    stdin_thread.join()
    client.loop_stop()
