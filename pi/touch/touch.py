#!/usr/bin/env python
import random
import threading
import time
from gpiozero import Button
from signal import pause
import subprocess
import random

# GPIO 4, 17, 22, 27번핀 활용
GPIO_PIN1 = 4
GPIO_PIN2 = 17
GPIO_PIN3 = 27
GPIO_PIN4 = 22

total_pressed = 0

# 터치 센서가 스위치처럼 반응하는 방식
try:
    button1 = Button(GPIO_PIN1)
    button2 = Button(GPIO_PIN2)
    button3 = Button(GPIO_PIN3)
    button4 = Button(GPIO_PIN4)
except Exception as e:
    print(f"GPIO PIN is busy or not available: {e}")
    exit(1)

# 터치센서에 감지가 됐을 때 발동되는 인터럽트 콜백함수
def button_pressed():
    # 감지 될 때마다 감지된 횟수 증가
    global total_pressed
    total_pressed += 1

# 인터럽트 방식으로 활용
button1.when_pressed = button_pressed
button2.when_pressed = button_pressed
button3.when_pressed = button_pressed
button4.when_pressed = button_pressed

# 세가지 감정을 랜덤으로 표현
emotion = ["happy", "joy", "exciting"]

#구현방식
#매 5초마다 10번이상의 터치가 된다면? "쓰다듬기 성공" print
#매 5초마다 10번 이하의 터치라면? 5초후 timer 재시작
def check_total_pressed():
    global total_pressed
    while True:
        #매 5초를 측정하는 timer
        start_time = time.time()
        while time.time() - start_time < 5:
            # 5초 이내에 10번 정도 만졌다면 쓰다듬었다고 판단
            if total_pressed >= 10:
                idx = random.randrange(0,3) # 감정을 표현하기 위한 랜덤함수
                total_pressed = 0 #터치 횟수 초기화
                start_time = time.time()  # timer reset하는 기능
                try:
                    subprocess.run(['python3', '/home/pi/mqtt/display.py', emotion[idx]])
                except Exception as e:
                    print(f"Error running subprocess: {e}", flush=True)
            time.sleep(0.1)
        # 매 5초가 지나면 자동으로 전체 횟수가 0으로 초기화됨
        if total_pressed < 10:
            total_pressed = 0

# 매번 5초마다 확인해야 하므로 thread로 동작
checking_thread = threading.Thread(target=check_total_pressed)
checking_thread.daemon = True
checking_thread.start()

pause()

