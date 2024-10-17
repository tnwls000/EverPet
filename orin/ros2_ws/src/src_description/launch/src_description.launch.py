import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction
from launch import LaunchDescription
from launch_ros.actions import Node

from launch.substitutions import (
    Command,
    FindExecutable,
    PathJoinSubstitution,
)

def generate_launch_description():

    pkg_path = os.path.join(get_package_share_directory("src_description"))
    #rviz_config_file = os.path.join(pkg_path, "rviz", "description.rviz")
    urdf_file = os.path.join(pkg_path, "urdf", "src_body.urdf")

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=[urdf_file],
    )


    static_transform_publisher = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        arguments=["0.2", "0", "0.20", "0", "3.1415926", "3.1415926", "base_link", "laser"],
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        static_transform_publisher,
    ])