#!/bin/bash

env="local"

for precision in "4bit" "8bit" "half" "full"
do
   for prompt in {0..2}
   do   
      for i in {0..9}   
      do
         python3 mistral_first.py $i $precision $env $prompt
         python3 mistral_second.py $i $precision $env $prompt 6 10
         python3 mistral_second.py $i $precision $env $prompt 11 15
         python3 mistral_second.py $i $precision $env $prompt 16 20
         python3 mistral_second.py $i $precision $env $prompt 21 25
         python3 mistral_second.py $i $precision $env $prompt 26 30
         python3 mistral_second.py $i $precision $env $prompt 31 32
      done

      for i in {0..9}
      do
         python3 mistral_labeled_first.py $i $precision $env $prompt
         python3 mistral_labeled_second.py $i $precision $env $prompt 6 10
         python3 mistral_labeled_second.py $i $precision $env $prompt 11 15
         python3 mistral_labeled_second.py $i $precision $env $prompt 16 20
         python3 mistral_labeled_second.py $i $precision $env $prompt 21 25
         python3 mistral_labeled_second.py $i $precision $env $prompt 26 30
         python3 mistral_labeled_second.py $i $precision $env $prompt 31 32
      done
   done
done