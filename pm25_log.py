"""
Script to log data from Adafruit PM 2.5 Sensor
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

# Continue running until next day
while day==date.today():
    # Run every 10 minutes
    time.sleep(600)

    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Sensor reading failed")
        continue
    dt = datetime.now()
    data = aqdata[data_fields]
    row = pd.Series([dt,data])
    dataframe.append(row)

day = date.today()
dataframe.to_csv(str(day)+'.csv')
    

