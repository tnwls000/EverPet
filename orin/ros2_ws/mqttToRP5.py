# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import subprocess
import rclpy
import json
from rclpy.node import Node
from rcl_interfaces.msg import Log

broker_address = "3.38.101.255"
topic = ""
message = "userIn"

# mosquitto_pub 명령어 구성
command = [
    "mosquitto_pub",
    "-h", broker_address,
    "-t", topic,
    "-m", message
]

def read_allinfo(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_allinfo(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Data has been written to {}".format(file_path))
    except Exception as e:
        print("Error writing to JSON file: {}".format(e))


class LogMonitor(Node):
    global topic, message
    
    def __init__(self):
        super().__init__('log_monitor')
        self.subscription = self.create_subscription(
            Log,
            '/rosout',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        allinfo = read_allinfo("/home/orin/allinfo.json")
        serialNum = allinfo['robot']['serialNumber']
        topic=serialNum+"/raspberry"
        message="userIn"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()

        # 출력 및 에러 출력
        if stdout:
            print("Output:\n", stdout.decode())
        if stderr:
            print("Error:\n", stderr.decode())
        
            

def main(args=None):
    rclpy.init(args=args)
    log_monitor = LogMonitor()
    rclpy.spin(log_monitor)
    log_monitor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()