"""
Nowcast using most recent data
"""

import processing
import time

from Adafruit_IO import Client, RequestError, Feed

# Separate .py file with Adafruit IO username and key
import io_credentials

aio = Client(io_credentials.username, io_credentials.key)
feed = aio.feeds('aqi-nowcast')

while True:
    # Run every 10 minutes
    time.sleep(600)

    try:
        # Try to calculate AQI
        pm25,aqi,level = processing.aqi_nowcast()  

    except:
        print("Can't Calculate AQI")
        continue
    
    # Send the AQI to Adafruit IO
    aio.send_data(feed.key, aqi)
    