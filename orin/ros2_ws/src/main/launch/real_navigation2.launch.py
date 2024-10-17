# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Darby Lim

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    #####

   # 각 launch 파일의 절대 경로
    motor_path = '/home/orin/ros2_ws/src/monicar/monicar_control/launch/motor.launch.py'
    sllidar_launch_path = '/home/orin/ros2_ws/src/sllidar_ros2/launch/sllidar_a1_launch.py'
    src_description_launch_path = '/home/orin/ros2_ws/src/src_description/launch/src_description.launch.py'
    rf2o_launch_path = '/home/orin/ros2_ws/src/rf2o_laser_odometry/launch/rf2o_laser_odometry.launch.py'
    online_async_launch_path = '/home/orin/ros2_ws/src/main/launch/online_async_launch.py'
    #rviz_path = '/home/orin/ros2_ws/src/main/config/init.rviz'
    
    motor_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(motor_path)
    )

    # 첫 번째 launch 파일: 라이다 센서 실행
    sllidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(sllidar_launch_path)
    )

    # 두 번째 launch 파일: src_description
    src_description_launch = TimerAction(
        period=2.0,  # 첫 번째 launch 실행 후 대기
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(src_description_launch_path)
        )]
    )

    # 세 번째 launch 파일: rf2o_laser_odometry
    rf2o_launch = TimerAction(
        period=5.0,  # 두 번째 launch 실행 후 5초 대기
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rf2o_launch_path)
        )]
    )

     # 네 번째 launch 파일: online_async_launch
    online_async_launch = TimerAction(
         period=2.0,  # 세 번째 launch 실행 후 2초 대기
         actions=[
             DeclareLaunchArgument('use_sim_time', default_value='False'),
             IncludeLaunchDescription(
                 PythonLaunchDescriptionSource(online_async_launch_path)
             )
         ]
     )

    #####
    use_sim_time = LaunchConfiguration('use_sim_time', default='False')
    map_dir = LaunchConfiguration(
        'map',
        default=os.path.join(
            get_package_share_directory('main'),
            'map',
            'test.yaml'))

    param_dir = LaunchConfiguration(
        'params_file',
        default=os.path.join(
            get_package_share_directory('main'),
            'param',
            'nav2.yaml'))

    nav2_launch_file_dir = os.path.join(get_package_share_directory('main'), 'launch')

    rviz_config_dir = os.path.join(
        get_package_share_directory('main'),
        'rviz',
        'tempviz.rviz')

    return LaunchDescription([

        motor_launch,
        sllidar_launch,
        src_description_launch,
        rf2o_launch,
        #online_async_launch,

        DeclareLaunchArgument(
            'map',
            default_value=map_dir,
            description='Full path to map file to load'),

        DeclareLaunchArgument(
            'params_file',
            default_value=param_dir,
            description='Full path to param file to load'),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='False',
            description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/nav2_bringup_launch.py']),
            launch_arguments={
                'map': map_dir,
                'use_sim_time': use_sim_time,
                'params_file': param_dir}.items(),
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
    ])
