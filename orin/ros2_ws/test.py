# -*- coding: utf-8 -*-
import sys
sys.path.append("/home/orin/.local/lib/python3.8/site-packages")
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatus
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
import paho.mqtt.client as mqtt
import subprocess
import json


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


class NavigateToPoseClient(Node):

    def __init__(self):
        super().__init__('navigate_to_pose_client')
        self._client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self._goals = [
            (-0.5142202866575927, -1.389881332850327, -0.346012191662497, 0.9382300161585726),  # waypoint 1
            (-0.5142202866575927, -3.089881332850327, -0.346012191662497, 0.9382300161585726),
            #(-0.6701976876705454, -2.8656786026067786, -0.5170875142984993, 0.8559325338813798),
            (2.194992445615058, -3.3912771098445553, -0.4733086278446747, 0.8808966697676812),  # waypoint 2
            (3.8324560378287775, -5.0062894671769795, -0.46762850732174893, 0.8839250981503088)
        ]
        self._current_goal_index = 0

    def send_goal(self):
        if self._current_goal_index >= len(self._goals):
            self.get_logger().info('All goals succeeded!')
            allinfo = read_allinfo("/home/orin/allinfo.json")
            serialNum = allinfo['robot']['serialNumber']
            subprocess.run(["mosquitto_pub", "-h", "3.38.101.255", "-t", serialNum+"/raspberry", "-m", "userIn"])
            
            return

        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = self._goals[self._current_goal_index][0]
        pose.pose.position.y = self._goals[self._current_goal_index][1]
        pose.pose.orientation.z = self._goals[self._current_goal_index][2]
        pose.pose.orientation.w = self._goals[self._current_goal_index][3]

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose

        self._client.wait_for_server()
        self._send_goal_future = self._client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result))
        if future.result().status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded!')
            self._current_goal_index += 1
            self.send_goal()
        else:
            self.get_logger().info('Goal failed with status: {0}'.format(future.result().status))

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback))

def main(args=None):
    rclpy.init(args=args)

    node = NavigateToPoseClient()
    node.send_goal()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
