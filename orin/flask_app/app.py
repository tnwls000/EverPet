import socket
import sys
import os
import time
from threading import Thread
sys.path.append('/usr/lib/python3.8/lib-dynload')
sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/lib/python3.8/dist-packages')

sys.path.append("/home/orin/.local/lib/python3.8/site-packages")

print(sys.path)

import subprocess
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

@app.route('/')
def index():

    return render_template_string(html_form)

@app.route('/wifi_setup', methods=['POST'])
def wifi_setup():
    ssid = request.form['ssid']
    password = request.form['password']
    Thread(target=configure_wifi, args=(ssid,password)).start()
    return 'WiFi configuration received. Connecting to WiFi...'

def check_wifi_connection():
    try:
        print(1,flush=True)
        socket.gethostbyname("www.google.com")
        print(2,flush=True)
        return True
    except socket.error:
        print(3,flush=True)
        return False

def configure_wifi(ssid, password):
    global connect_data
    # AP 모드 중지
    time.sleep(10)
    subprocess.run('sudo systemctl stop hostapd', shell=True)
    subprocess.run('sudo systemctl stop dnsmasq', shell=True)

    # wpa_supplicant.conf 파일에 WiFi 설정 추가
    config_content = f'''
update_config=1
p2p_disabled=1
network={{
    ssid="{ssid}"
    psk="{password}"
    key_mgmt=WPA-PSK
}}
'''
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as config_file:
        config_file.write(config_content)
    
    # 인터페이스를 클라이언트 모드로 전환
    
    subprocess.run('sudo network client',shell=True)
    # WiFi 연결 확인
    if not check_wifi_connection():
        # WiFi 연결 실패 시 AP 모드로 다시 전환
        print("failed connect",flush=True)
        subprocess.run('sudo network ap', shell=True)
    else:
        #connect_data['connect']=True
        #write_allinfo("home/orin/setting.json", connect_data)
        # WiFi 연결 성공 시 플래그 파일 생성
        with open('/tmp/shutdown_signal', 'w') as f:
            f.write('shutdown')

def run_server():
    # 서버를 별도의 스레드에서 실행
    server_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5000, use_reloader=False, threaded=True))
    server_thread.start()

    # 플래그 파일을 주기적으로 확인하여 서버 종료 결정
    while not os.path.exists('/tmp/shutdown_signal'):
        time.sleep(1)
        
    if os.path.exists('/tmp/shutdown_signal'):
        os.remove('/tmp/shutdown_signal')
        
        
    print("Server is shutting down.")
    os._exit(0)
    
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
        
if __name__ == '__main__':

    #connect_data = read_allinfo("/home/orin/setting.json")
    
    subprocess.run('sudo network ap', shell=True)
    
    run_server()


