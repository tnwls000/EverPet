from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import os

def generate_launch_description():
    # 각 launch 파일의 절대 경로
    motor_path = '/home/orin/ros2_ws/src/monicar/monicar_control/launch/motor.launch.py'
    sllidar_launch_path = '/home/orin/ros2_ws/src/sllidar_ros2/launch/sllidar_a1_launch.py'
    src_description_launch_path = '/home/orin/ros2_ws/src/src_description/launch/src_description.launch.py'
    rf2o_launch_path = '/home/orin/ros2_ws/src/rf2o_laser_odometry/launch/rf2o_laser_odometry.launch.py'
    online_async_launch_path = '/home/orin/ros2_ws/src/articubot_one/launch/online_async_launch.py'
    joy_path = '/home/orin/ros2_ws/src/monicar/monicar_teleop/launch/teleop_joy.launch.py'
    rviz_path = '/home/orin/ros2_ws/src/main/config/init.rviz'
    
    motor_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(motor_path)
    )
    joy_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(joy_path)
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

    # RViz 실행
    rviz_launch = TimerAction(
        period=2.0,  # 네 번째 launch 실행 후 2초 대기
        actions=[
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                arguments=['-d', rviz_path],
                output='screen',
                parameters=[{'use_sim_time': False}]
            )
        ]
    )

    return LaunchDescription([
        motor_launch,
        sllidar_launch,
        src_description_launch,
        rf2o_launch,
        online_async_launch,
        rviz_launch,
        joy_launch,
    ])
