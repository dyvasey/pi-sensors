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
    
    data1 = pd.read_csv(directory+yesterday+'.csv')
    data2 = pd.read_csv(directory+day+'.csv')
    
    data = pd.concat([data1,data2])
    
    # Get last row in combined data
    last = len(data.index)
    # Get every hour over past 12 hours
    rows = np.arange(last-72,last+1,6)
    measurements = data.loc[rows,'pm25 standard']
    
    return(measurements)
