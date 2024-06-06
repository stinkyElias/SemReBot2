# ROS 2 Semantic Reasoning in Robots

## Requirements
- Dedicated GPU with min. 9 GB memory
- ~30 GB storage
- CUDA version 11.8+
- Docker
- Python3.8+

## Setup (Ubuntu)
1. Install `pytorch` for `Python 3.8+`
    
    CUDA 11.8
    ```bash
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```
    or CUDA 12.1
    ```bash
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    ```
2. Install `transformers`
    ```bash
    pip install transformers
    ```

3. Clone repo to home directory (ssh)
    ```bash
    git clone git@github.com:stinkyElias/SemReBot2.git
    ```

4. Download Whisper large with flash attention and Mistral 7B Instruct in 4-bit precision by running the `download_models.py` script. The default location is `~/semrebot2_models`, but this can be set by adding a user-specific path as command line argument. _The models take up ~18 GB of storage_

    Default location:
    ```bash
    python3 download_models.py
    ```
    User-specified location:
    ```bash
    python3 download_models.py "relative/path/to/location"
    ```

5. Pull Docker image from Docker Hub
    ```bash
    docker pull stinkyelias/rolling:whisper
    ```

6. To start the container, run `run.sh` bash script in terminal 1
    
    Terminal 1:
    ```bash
    ./run.sh
    ```

7. Build the ROS2 packages inside the container. Remember to source the workspace aftrwards
    Terminal 1:
    ```bash
    ./env.sh
    ```
    ```bash
    source install/setup.bash
    ```

This setup of SemReBot2 requires four terminal windows. After step 7, start three new terminals. You can easily attach to the running container by first retrieving the container name.

Terminal 2:
```bash
docker container list
```
`>>> some_container_name`

8. Attach three terminals to the running container
    
    Terminal 2:
    ```bash
    ./terminal some_container_name
    ```
    Terminal 3:
    ```bash
    ./terminal some_container_name
    ```
    Terminal 4:
    ```bash
    ./terminal some_container_name
    ```
    If Terminal 1 has finished building the ROS2 packages, remember to source each terminal!
    ```bash
    source install/setup.bash
    ```
## Test run
1. With all four terminals running, bring up SemReBot2, Task controller node and Nav2 sim node
   
    Terminal 1:
    ```bash
    ros2 launch semrebot2_bringup bringup.launch.py
    ```
    Terminal 2:
    ```bash
    ros2 run semrebot2_task_controller task_controller_node
    ```
    Terminal 3:
    ```bash
    ros2 run semrebot2_task_controller nav2_sim_node
    ```
3. To use one of the four audio samples, publish to the `/speech` topic the audio file you wish to test. Audio file 3 contain logical inconsistencies not possible to solve!
4. 
    Terminal 4:
    ```bash
    ros2 topic pub --once /speech std_msgs/msg/Int8 "{data: x}"
    ```
    where 1 <= x <= 4

