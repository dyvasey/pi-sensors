#!/bin/bash

nohup sudo -b python3 pm25_log.py >> logs/pm25_log.log 2>&1
nohup sudo -b python3 nowcasting.py >> logs/nowcasting.log 2>&1

echo "Initiated data logging and AQI Nowcasting."


