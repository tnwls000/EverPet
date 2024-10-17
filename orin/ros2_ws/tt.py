import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
import paho.mqtt.client as mqtt
import json
import os

class MapMQTTClientNode(Node):
    def __init__(self):
        super().__init__('map_mqtt_client_node')

        self.user_id, self.serial_number = self.load_user_info()

        self.subscription = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            10
        )

        self.mqtt_client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv311)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.connect("3.38.101.255", 1883, 60)
        self.mqtt_client.loop_start()

    def load_user_info(self):
        json_file_path = "allinfo.json"
        
        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as file:
                data = json.load(file)
                user_id = data.get("userId", "defaultUser") 
                serial_number = data.get("serialNumber", "defaultSerial")  
                return user_id, serial_number
        else:
            self.get_logger().error(f"{json_file_path} No!")
            return "defaultUser", "defaultSerial"

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.get_logger().info("Connected to MQTT Broker!")
        else:
            self.get_logger().info(f"Failed to connect, return code {rc}")

    def map_callback(self, msg):
        
        map_data = {
            "info": {
                "width": msg.info.width,
                "height": msg.info.height,
                "resolution": msg.info.resolution,
                "origin": {
                    "position": {
                        "x": msg.info.origin.position.x,
                        "y": msg.info.origin.position.y,
                        "z": msg.info.origin.position.z
                    },
                    "orientation": {
                        "x": msg.info.origin.orientation.x,
                        "y": msg.info.origin.orientation.y,
                        "z": msg.info.origin.orientation.z,
                        "w": msg.info.origin.orientation.w
                    }
                }
            },
            "data": list(msg.data)  
        }

        payload = f"tnwlssla20/{json.dumps(map_data)}"

        mqtt_topic = f"B2KA992ABFES0/web/mapConfirm"
        self.mqtt_client.publish(mqtt_topic, payload)
        self.get_logger().info(f"Map data sent to MQTT topic {mqtt_topic} with user ID: tnwlssla20")

def main(args=None):
    rclpy.init(args=args)
    map_mqtt_client_node = MapMQTTClientNode()
    rclpy.spin(map_mqtt_client_node)
    map_mqtt_client_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

