#!/bin/bash

# Get the current user's home directory
HOME_DIR=$(eval echo ~$USER)

# Set the base directory for the project
BASE_DIR="$HOME_DIR/SemReBot2"

docker run --gpus all -it \
    --privileged \
    --network=host \
    --ipc=host \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    --env=DISPLAY \
    --env=QT_X11_NO_MITSHM=1 \
    --device /dev/snd:/dev/snd \
    -v $BASE_DIR/ros2_ws/src/semrebot2:/home/stinky/ros2_ws/src/semrebot2 \
    -v $BASE_DIR/ros2_ws/results:/home/stinky/ros2_ws/results \
    -v $BASE_DIR/.vscode:/home/stinky/.vscode \
    -v $HOME_DIR/.Xauthority:/home/stinky/.Xauthority:rw \
    -v $BASE_DIR/env.sh:/home/stinky/ros2_ws/env.sh \
    -v $HOME_DIR/models:/home/stinky/models \
    stinkyelias/rolling:whisper \
    /bin/bash