"""
Data processing functions for Raspberry Pi sensors
"""
import pandas as pd
import numpy as np

from datetime import date,timedelta

def aqi(directory = '/home/pi/Desktop/pm25-data/'):
    """
    Calculate AQI NowCast using last 12 hours of PM 2.5 Data.
    
    Requires data in 10 minute intervals
    """
    day = str(date.today())
    yesterday = str(date.today()-timedelta(days=1))
    

    data2 = pd.read_csv(directory+day+'.csv')
    
    # Check to see if previous data avaiiable
    try:
        data1 = pd.read_csv(directory+yesterday+'.csv')
    except:
        data = data2
    else:
        data = pd.concat([data1,data2])
    
    # Get last row in combined data
    last = len(data.index)
    
    # Get every hour over past 12 hours
    try:
        rows = np.arange(last-72,last+1,6)
        measurements = data.loc[rows,'pm25 standard']
        return(measurements)
    
    except:
        print('Insufficient data available for AQI NowCast')
        print('Measurements Available: ',last)
        return

