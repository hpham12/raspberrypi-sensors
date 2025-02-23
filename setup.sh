#!/bin/bash

cd /home/pi/code/raspberrypi-sensors
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
