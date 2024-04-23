#!/bin/bash

docker run --gpus all -it \
    --privileged \
    --network=host \
    --ipc=host \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    --env=DISPLAY \
    --env=QT_X11_NO_MITSHM=1 \
    --device /dev/snd:/dev/snd \
    -v /home/stinky/Documents/semantic-robot/ros2_ws/src/semrebot2:/home/stinky/ros2_ws/src/semrebot2 \
    -v /home/stinky/Documents/semantic-robot/ros2_ws/results:/home/stinky/ros2_ws/results \
    -v /home/stinky/Documents/semantic-robot/.vscode:/home/stinky/.vscode \
    -v /home/stinky/.Xauthority:/home/stinky/.Xauthority:rw \
    -v /home/stinky/Documents/semantic-robot/env.sh:/home/stinky/ros2_ws/env.sh \
    -v /home/stinky/Documents/semantic-robot/package_tests.sh:/home/stinky/ros2_ws/package_tests.sh \
    -v /home/stinky/Documents/semantic-robot/tests.sh:/home/stinky/ros2_ws/tests.sh \
    -v /home/stinky/models:/home/stinky/models \
    stinkyelias/rolling:whisper \
    /bin/bash