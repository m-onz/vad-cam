#!/bin/bash
echo "Starting Python 3.5 with OpenCV 3.4.1 bindings..."
cd /home/pi/Desktop/vad-cam/
/home/pi/.virtualenvs/py3cv3/bin/python ./camera.py >> /home/pi/Desktop/log.txt 2>&1

