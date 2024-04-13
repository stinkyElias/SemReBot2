#!/bin/bash

# precision=$1
# env=$2

# for i in {0..9}
# do
#    python3 mistral_first.py $i $precision $env
#    python3 mistral_second.py $i $precision $env
# done

# for i in {0..9}
# do
#    python3 mistral_labeled_first.py $i $precision $env
#    python3 mistral_labeled_second.py $i $precision $env
# done

env="idun"

for precision in "4bit" "8bit" "half" "full"
do   
   for i in {0..9}   
   do
      python3 mistral_first.py $i $precision $env
      python3 mistral_second.py $i $precision $env
   done

   for i in {0..9}
   do
      python3 mistral_labeled_first.py $i $precision $env
      python3 mistral_labeled_second.py $i $precision $env
   done
done