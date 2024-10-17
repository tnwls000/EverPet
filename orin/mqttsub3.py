# -*- coding: utf-8 -*-
import sys
sys.path.append("/home/orin/.local/lib/python3.8/site-packages")
import socket
from threading import Thread
sys.path.append('/usr/lib/python3.8/lib-dynload')
sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/lib/python3.8/dist-packages')

sys.path.append("/home/orin/.local/lib/python3.8/site-packages")

from flask import Flask, request, render_template_string

app = Flask(__name__)

html_form = '''
<!doctype html>
<title>WiFi Setup</title>
<h1>Enter WiFi Credentials</h1>
<form method=post action="/wifi_setup">
  SSID: <input type=text name=ssid><br>
  Password: <input type=password name=password><br>
  <input type=submit value=Submit>
</form>
'''
import requests
import paho.mqtt.client as mqtt
import subprocess
import os
import concurrent.futures
import json
import threading
import time
import signal
from multiprocessing import Process
serialNum=""
paused = False
userID = ""
thread=None
stop_server = threading.Event()

# 콜백 함수 정의
def read_allinfo(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
    
def write_allinfo(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        #print(f"Data has been written to {file_path}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

def on_connect(client, userdata, flags, reason_code, properties):
    global serialNum
    allinfo=read_allinfo("/home/orin/allinfo.json")
    serialNum=allinfo['serialNumber']
    print("Connected with result code " + str(reason_code))
    client.subscribe(serialNum+"/jetson/#")

def on_message(client, userdata, msg):
    global serialNum
    global paused
    global userID
    if paused:
        return
    topic = msg.topic
    temp=topic.split('/',1)
    topic=temp[1]
    message = msg.payload.decode()
    with open("received_messages.txt", "a") as f:
        f.write(message + "\n")
    # 메시지에 해당하는 .py 파일이 있는지 확인하고 실행
    script_path = f"{message}.py"
    
    if topic == "jetson/userID":
        try:
            tempinfo=read_allinfo("/home/orin/allinfo.json")
            tempinfo['userId']=message
            write_allinfo("/home/orin/allinfo.json",tempinfo)
            
            print("JSON data saved to allinfo.json")
            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        return
    
    elif topic=="jetson/map":
        subprocess.Popen(["bash","-l", "-c", "source /opt/ros/galactic/setup.bash && source /home/orin/ros2_ws/install/setup.bash && ros2 launch main mapping.launch.py"])
        time.sleep(18)
        subprocess.Popen(["bash","-l", "-c", "source /opt/ros/galactic/setup.bash && source /home/orin/ros2_ws/install/setup.bash && python3 /home/orin/savingMap.py"])
        return

        
    elif topic=="jetson/mapDone":
        subprocess.run(["bash","-l", "-c", "source /opt/ros/galactic/setup.bash && source /home/orin/ros2_ws/install/setup.bash && ros2 run nav2_map_server map_saver_cli -f my_map"])
        time.sleep(1)
        subprocess.run(["./killProcess"])
        subprocess.Popen(["bash","-l", "-c", "source /opt/ros/galactic/setup.bash && source /home/orin/ros2_ws/install/setup.bash && ros2 launch main real_navigation2.launch.py"])
        return
        
    elif topic=="jetson/location":
        json_data = json.loads(message)
        tempdata=read_allinfo("/home/orin/location.json")
        nowLoc=json_data['location']
        tempdata[nowLoc]['position']=json_data['position']
        tempdata[nowLoc]['orientation']=json_data['orientation']
        write_allinfo("/home/orin/location.json",tempdata)
        return
    elif topic=="jetson/tail":
    
        result = subprocess.run(['pgrep', '-f', 'servo.py'], stdout=subprocess.PIPE)
        pids = result.stdout.decode().split()

        # 실행 중인 프로세스가 있으면 종료합니다.
        for pid in pids:
            os.kill(int(pid), signal.SIGTERM)
            
        if message=="joy" or message=="happy" or message=="exciting":
            subprocess.Popen(["bash","-l", "-c", "source /opt/ros/galactic/setup.bash && source /home/orin/ros2_ws/install/setup.bash && sudo python3 servo.py 10 0.1"])
        """elif message=="curious" or message=="realize" or message=="more_realize":
            #일반단계 2단계
            subprocess.Popen(["bash","-l", "-c", "source /opt/ros/galactic/setup.bash && source /home/orin/ros2_ws/install/setup.bash && sudo python3 servo.py 15 0.2"])
        else:
        #가장 느린 1단계
            subprocess.Popen(["bash","-l", "-c", "source /opt/ros/galactic/setup.bash && source /home/orin/ros2_ws/install/setup.bash && sudo python3 servo.py 20 0.5"])"""
        return
    
    if message=="userIn":
        subprocess.Popen(["python3", "/home/orin/ros2_ws/test.py"])
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
        command = sys.stdin.readline().strip()
        if command == 'pause':
            paused = True
        elif command == 'resume':
            paused = False
            
def run_script(script_path):
    try:
        result = subprocess.run(["python3", script_path], check=True)
        print(f"{script_path} finished execution with return code {result.returncode}.", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}", flush=True)
        
              
sys.stdout.flush()
#subprocess.run(["sudo", "network", "client"])
subprocess.run(["bash", '-c', "source /home/orin/.bashrc"])
# MQTT 클라이언트 설정
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# 브로커에 연결
client.connect("3.38.101.255", 1883, 60)

subprocess.run(["mosquitto_pub", "-h", "3.38.101.255", "-t", serialNum+"/jetson", "-m", "Turnon jetson MQTT"])
stdin_thread = threading.Thread(target=handle_stdin_input)
stdin_thread.daemon = True
stdin_thread.start()


# 메시지 루프 시작
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
client.loop_forever()

stdin_thread.join()
client.loop_stop()

