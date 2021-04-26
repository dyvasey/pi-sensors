"""
Nowcast using most recent data
"""
from Adafruit_IO import Client

import processing

# Separate .py file with Adafruit IO username and key
import io_credentials

aio = Client(io_credentials.username, io_credentials.key)
feed = aio.feeds('aqi-nowcast')

try:
    # Try to calculate AQI
    pm25,aqi,level = processing.aqi_nowcast()  

except:
    print("Can't Calculate AQI")

# Send the AQI to Adafruit IO
aio.send_data(feed.key, aqi)
    