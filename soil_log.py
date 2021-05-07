"""
Log data from soil moisture sensor and send to Adafruit IO
"""
import time

from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw
from Adafruit_IO import Client

# Separate .py file with Adafruit IO username and key
import io_credentials

aio = Client(io_credentials.username, io_credentials.key)
feed1 = aio.feeds('soil-moisture')
feed2 = aio.feeds('soil-temperature')

i2c_bus = busio.I2C(SCL, SDA)

ss = Seesaw(i2c_bus, addr=0x36)

# read moisture level through capacitive touch pad
touch = ss.moisture_read()

# read temperature from the temperature sensor
temp = ss.get_temp()

aio.send_data(feed1.key, touch)
aio.send_data(feed2.key, touch)
