#!/bin/bash

# Check if a container name was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <container_name>"
    exit 1
fi

# Assign the first argument to a variable
container_name=$1

# Execute the Docker command
docker exec -it $container_name bash
