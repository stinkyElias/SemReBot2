#!/bin/bash

source install/setup.bash

# Loop over each audio file number
for i in {1..4}
do
    # Repeat tests for each file
    for j in {1..10}
    do
        ./package_tests.sh $i
        sleep 10
    done
done
