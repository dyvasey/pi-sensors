#!/bin/bash
cd /home/pi/Desktop/pi-sensors
sudo python3 pm25_log.py >> logs/pm25_log.log 2>&1
sudo python3 nowcast.py >> logs/nowcast.log 2>&1

echo "Logged PM2.5 data and AQI Nowcast."


