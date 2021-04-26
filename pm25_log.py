"""
Script to log data from Adafruit PM 2.5 Sensor
"""

import serial
import pandas as pd
from datetime import datetime
from datetime import date
from os import path

from adafruit_pm25.uart import PM25_UART
from Adafruit_IO import Client

# Separate .py file with Adafruit IO username and key
import io_credentials

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
pm25 = PM25_UART(uart)

aio = Client(io_credentials.username, io_credentials.key)
feed = aio.feeds('pm-2-dot-5')

data_fields = ['pm10 standard','pm25 standard','pm100 standard',
                   'pm10 env','pm25 env','pm100 env','particles 03um',
                   'particles 05um','particles 10um','particles 25um',
                   'particles 50um','particles 100um']

columns = ['datetime'] + data_fields

# Get current date
day = date.today()
pth = '/home/pi/Desktop/pm25-data/' + str(day) + '.csv'

# Get existing dataframe if it exists
if path.exists(pth):
    dataframe = pd.read_csv(pth)
else:
    # Start empty dataframe
    dataframe = pd.DataFrame(columns=columns)

# Have sensor attempt the reading 5 times
n = 0
while n<5:
    try:
        # Read data from the sensor
        aqdata = pm25.read()
        break
    
    except RuntimeError:
        print("Sensor reading failed")
        n = n+1
        continue
    
    except serial.SerialException:
        print("Sensor failed to connect")
        n = n+1
        continue
else:
    print('Sensor reading failed after 5 attempts')

# Send the PM 2.5 data to Adafruit IO
aio.send_data(feed.key, aqdata['pm25 standard'])

# Organize and store data
dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
data=[dt]
for field in data_fields:
    value = aqdata[field]
    data.append(value)
print(data)
row = pd.Series(data,index=columns)
dataframe = dataframe.append(row,ignore_index=True)

dataframe.to_csv(pth,index=False)
    

    

