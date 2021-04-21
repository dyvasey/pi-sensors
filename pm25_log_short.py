"""
Script to log data from Adafruit PM 2.5 Sensor - test version for short time 
"""

import time
import serial
import pandas as pd
from datetime import datetime
from datetime import date

# datetime object containing current date and time
now = datetime.now()
from adafruit_pm25.uart import PM25_UART

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
pm25 = PM25_UART(uart)

data_fields = ['pm10 standard','pm25 standard','pm100 standard',
                   'pm10 env','pm25 env','pm100 env','particles 03um',
                   'particles 05um','particles 10um','particles 25um',
                   'particles 50um','particles 100um']

columns = ['datetime'] + data_fields
dataframe = pd.DataFrame(columns=columns)

day = date.today()

# Run 10 times
n = 0
while n<10:
    # Run every 10 seconds
    time.sleep(10)

    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Sensor reading failed")
        continue
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data=[dt]
    for field in data_fields:
        value = aqdata[field]
        data.append(value)
    print(data)
    row = pd.Series(data,index=columns)
    dataframe = dataframe.append(row,ignore_index=True)
    n=n+1

day = date.today()
dataframe.to_csv(str(day)+'.csv',index=False)
    

