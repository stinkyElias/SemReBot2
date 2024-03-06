#!/bin/bash

docker run -it \
    --privileged \
    --network=host \
    --ipc=host \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    --env=DISPLAY \
    --env=QT_X11_NO_MITSHM=1 \
    -v /home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot:/home/stinky/ros2_ws/src/bt_plansys_turtlebot \
    -v /home/stinky/Documents/semantic-robot/.vscode:/home/stinky/.vscode \
    -v /home/stinky/.Xauthority:/home/stinky/.Xauthority:rw \
    -v /home/stinky/Documents/semantic-robot/env.sh:/home/stinky/ros2_ws/env.sh \
    -v /home/stinky/Documents/semantic-robot/llm:/home/stinky/llm \
    -v /home/stinky/Documents/semantic-robot/stt:/home/stinky/stt \
    plansys:full \
    /bin/bash