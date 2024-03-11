##############################################
# Adapted Dockerfile from athackst/ros2-rolling-gazebo
##############################################

# Base image
FROM ubuntu:22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive

# Install language
RUN apt-get update && apt-get install -y \
  locales \
  && locale-gen en_US.UTF-8 \
  && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
  && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8

# Install timezone
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime \
  && export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install -y tzdata \
  && dpkg-reconfigure --frontend noninteractive tzdata \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

# Install common programs
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
    sudo \
    software-properties-common \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install ROS2
RUN sudo add-apt-repository universe \
  && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null \
  && apt-get update && apt-get install -y --no-install-recommends \
    ros-rolling-ros-base \
    python3-argcomplete \
  && rm -rf /var/lib/apt/lists/*

ENV ROS_DISTRO=rolling
ENV AMENT_PREFIX_PATH=/opt/ros/rolling
ENV COLCON_PREFIX_PATH=/opt/ros/rolling
ENV LD_LIBRARY_PATH=/opt/ros/rolling/lib
ENV PATH=/opt/ros/rolling/bin:$PATH
ENV PYTHONPATH=/opt/ros/rolling/lib/python3.10/site-packages
ENV ROS_PYTHON_VERSION=3
ENV ROS_VERSION=2
ENV DEBIAN_FRONTEND=

# Develop image
FROM base AS dev

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
  bash-completion \
  build-essential \
  cmake \
  gdb \
  git \
  openssh-client \
  python3-argcomplete \
  python3-pip \
  ros-dev-tools \
  ros-rolling-ament-* \
  vim \
  && rm -rf /var/lib/apt/lists/*

RUN rosdep init || echo "rosdep already initialized"

ARG USERNAME=stinky
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  # Add sudo support for the non-root user
  && apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  && rm -rf /var/lib/apt/lists/*

# Set up autocompletion for user
RUN apt-get update && apt-get install -y git-core bash-completion \
  && echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc \
  && echo "if [ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ]; then source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash; fi" >> /home/$USERNAME/.bashrc \
  && rm -rf /var/lib/apt/lists/* 

ENV DEBIAN_FRONTEND=
ENV AMENT_CPPCHECK_ALLOW_SLOW_VERSIONS=1

# Full image
FROM dev AS full

ENV DEBIAN_FRONTEND=noninteractive
# Install the full release
RUN apt-get update && apt-get install -y --no-install-recommends \
  ros-rolling-desktop \
  && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=

# Gazebo image
FROM full AS gazebo

ENV DEBIAN_FRONTEND=noninteractive
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
  && apt-get update && apt-get install -q -y --no-install-recommends \
    ros-rolling-gazebo* \
  && rm -rf /var/lib/apt/lists/*

ENV TURTLEBOT3_MODEL=waffle
ENV GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/rolling/share/turtlebot3_gazebo/models

ENV DEBIAN_FRONTEND=

# Navigation2 image
FROM gazebo AS plansys2-depends

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /home/stinky/ros2_ws
RUN mkdir -p /home/stinky/ros2_ws/src \
    # && git clone https://github.com/ros-planning/navigation2.git --branch main ./src/navigation2 \
    && git clone https://github.com/fmrico/navigation2.git --branch nav2_msgs_only ./src/navigation2 \
    && git clone https://github.com/ros-geographic-info/geographic_info.git --branch ros2 ./src/geographic_info \
    && git clone https://github.com/BehaviorTree/BehaviorTree.CPP.git --branch master ./src/behaviortree_cpp \
    && apt-get update && apt-get upgrade -y --no-install-recommends \
    && rosdep update \
    && rosdep install -y --ignore-src --from-paths src -r \
    && . /opt/ros/rolling/setup.sh \
    && colcon build --symlink-install

ENV DEBIAN_FRONTEND=

#  Plansys2 image
FROM plansys2-depends AS plansys2

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /home/stinky/ros2_ws
RUN git clone https://github.com/PlanSys2/ros2_planning_system.git -b rolling ./src/plansys2 \
    # && git clone https://github.com/PlanSys2/ros2_planning_system_examples.git -b rolling ./src/plansys2_examples \
    && git clone https://github.com/fmrico/cascade_lifecycle.git -b rolling ./src/cascade_lifecycle \
    && git clone https://github.com/fmrico/popf.git -b rolling-devel ./src/popf \
    # testing dependencies
    && git clone https://github.com/ros2/rcl_interfaces.git -b rolling ./src/rcl_interfaces \
    && git clone https://github.com/ros2/test_interface_files.git -b rolling ./src/test_interface_files \
    && apt-get update && apt-get upgrade -y --no-install-recommends \
    && rosdep update \
    && rosdep install -y --ignore-src --from-paths src --rosdistro rolling -r \
    && . /opt/ros/rolling/setup.sh \
    && colcon build --symlink-install

ENV DEBIAN_FRONTEND=

# Gazebo+Nvidia image
FROM plansys2 AS gazebo-nvidia

# Expose the nvidia driver to allow opengl 
# Dependencies for glvnd and X11.
RUN apt-get update \
 && apt-get install -y -qq --no-install-recommends \
  libglvnd0 \
  libgl1 \
  libglx0 \
  libegl1 \
  libxext6 \
  libx11-6 \
  && rm -rf /var/lib/apt/lists/*

# Env vars for the nvidia-container-runtime.
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENV QT_X11_NO_MITSHM 1

# NVIDIA container toolkit
FROM gazebo-nvidia AS cuda

ENV DEBIAN_FRONTEND=noninteractive
RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    nvidia-container-toolkit \
    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=

# Python and NLP image
FROM cuda AS nlp-ros2

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /home/stinky/ros2_ws
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    portaudio19-dev \
    && pip3 install torch torchvision torchaudio \
    && pip install transformers \
    && pip install PyAudio \
    && pip install accelerate \
    && pip install bitsandbytes \
    && pip install keyboard \
    && rm -rf /var/lib/apt/lists/*
  
ENV DEBIAN_FRONTEND=

RUN chown -R stinky:stinky /home/stinky
USER stinky
