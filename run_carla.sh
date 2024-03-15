#!/bin/bash

docker run --gpus all -it \
    --privileged \
    --network=host \
    --ipc=host \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    --env=DISPLAY \
    --env=QT_X11_NO_MITSHM=1 \
    --device /dev/snd:/dev/snd \
    -v /home/carla/elias/semantic-robot/ros2_ws/src/task_controller:/home/stinky/ros2_ws/src/task_controller \
    -v /home/carla/elias/semantic-robot/ros2_ws/src/nlp_handler:/home/stinky/ros2_ws/src/nlp_handler \
    -v /home/carla/elias/semantic-robot/.vscode:/home/stinky/.vscode \
    -v /home/carla/.Xauthority:/home/stinky/.Xauthority:rw \
    -v /home/carla/elias/semantic-robot/env.sh:/home/stinky/ros2_ws/env.sh \
    -v /home/carla/elias/models:/home/stinky/models \
    stinkyelias/rolling:whisper \
    /bin/bash