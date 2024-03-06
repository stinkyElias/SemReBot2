#!/bin/bash

docker run -it \
    --privileged \
    --network=host \
    --ipc=host \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    --env=DISPLAY \
    --env=QT_X11_NO_MITSHM=1 \
    -v /home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot:/home/stinky/ros2_ws/src/bt_plansys_turtlebot \
    -v /home/stinky/Documents/semantic-robot/ros2_ws/.vscode:/home/stinky/ros2_ws/.vscode \
    -v /home/stinky/.Xauthority:/home/stinky/.Xauthority:rw \
    -v /home/stinky/Documents/semantic-robot/env.sh:/home/stinky/ros2_ws/env.sh \
    plansys:full \
    /bin/bash