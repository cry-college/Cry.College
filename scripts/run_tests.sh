#!/bin/bash

echo "Please enter a week number (1-8):"
read week

if ! [[ "$week" =~ ^[1-8]$ ]]; then
  echo "Invalid week number. Please try again."
  exit 1
fi
echo "Available class names for week $week:"
classes=( $(ls ../CryCollege/week$week) )
for i in "${!classes[@]}"; do
  echo "$((i+1))) ${classes[i]}"
done
echo "Please choose a class number (1-${#classes[@]}):"
read class_num

if ! [[ "$class_num" =~ ^[1-9]+[0-9]*$ ]] || [ "$class_num" -gt "${#classes[@]}" ]; then
  echo "Invalid class number. Please try again."
  exit 1
fi

class_name=${classes[$((class_num-1))]}

# Build the env
python3 -m venv crycollege_env
# Activate the env for the current shell
source ../crycollege_env/bin/activate

# Add dir to Python's search path
export PYTHONPATH=$(pwd)

# Run pytest 
pytest ../CryCollege/week$week/$class_name
