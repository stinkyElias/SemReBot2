#!/bin/bash

for i in {0..9}
do
   python3 mistral_first.py $i
   python3 mistral_second.py $i
done

for i in {0..9}
do
   python3 mistral_labeled_first.py $i
   python3 mistral_labeled_second.py $i
done