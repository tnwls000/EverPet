# -*- coding: utf-8 -*-
import sys
import subprocess
#subprocess.run(["bash","-l", "-c", "source /opt/ros/galactic/setup.bash && source /home/orin/ros2_ws/install/setup.bash"])

sys.path.append("/home/orin/.local/lib/python3.8/site-packages")
print(sys.path)
from adafruit_servokit import ServoKit
import time
import smbus2
import busio
import board
import time

# I2C 버스 설정 (SCL 및 SDA 핀을 사용하여 I2C 버스 초기화)
i2c_bus = busio.I2C(board.SCL, board.SDA)

def i2c_scan(i2c):
    """
    I2C 버스를 스캔하여 연결된 모든 I2C 장치의 주소를 반환합니다.
    """
    while not i2c.try_lock():
        pass
    try:
        devices = i2c.scan()
        return devices
    finally:
        i2c.unlock()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python servo.py <limit> <speed>")
        sys.exit(1)

    lim = int(sys.argv[1])
    spd = float(sys.argv[2])
    
    print("Scanning I2C bus...")
    # I2C 버스를 스캔하여 연결된 장치 목록을 가져옴
    devices = i2c_scan(i2c_bus)
    #print(f"I2C devices found: {[hex(device) for device in devices]}")

    if not devices:
        raise ValueError("No I2C devices found on the bus.")

    # PCA9685 PWM 드라이버 초기화 (서보 모터 제어를 위해 사용)
    try:
        kit = ServoKit(channels=16, i2c=i2c_bus, address=0x60)
        print("PCA9685 initialized at address 0x60.")
    except Exception as e:
        print(f"Error initializing PCA9685: {e}")
        raise

    # 서보 모터 초기 위치 설정
    pan = 90
    kit.servo[1].angle = pan

    print("Servo motors initialized.")
    print("Starting servo control test..."
            )
    for i in range(10):
        kit.servo[1].angle = 90-lim

        time.sleep(spd)

        kit.servo[1].angle = 90+lim
        time.sleep(spd)
    # 서보 모터 제어 테스트
    """
    for i in range(0, 180):
        kit.servo[1].angle = i
        print(f"Servo 0 angle: {i}")
        time.sleep(0.05)  # 서보 모터의 각도 변경 후 잠시 대기
    for i in range(180, 0, -1):
        kit.servo[1].angle = i
        print(f"Servo 0 angle: {i}")
        time.sleep(0.05)  # 서보 모터의 각도 변경 후 잠시 대기

    print("Servo control test completed.")
    """

