#!/bin/bash

source /home/orin/.bashrc
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/lib:/usr/lib/aarch64-linux-gnu

export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
source /opt/ros/galactic/setup.bash		# source galactic
source ~/ros2_ws/install/setup.bash

sudo python3 /home/orin/flask_app/app.py > /home/orin/server.log 2>&1
FLASK_PID=$!

wait $FLASK_PID
sleep 30

sudo python3 /home/orin/mqttsub3.py > /home/orin/locfile.log 2>&1



