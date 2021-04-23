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
        hour_measurements = data.loc[rows,'pm25 standard']
    
    except:
        print('Insufficient data available for AQI NowCast')
        print('Measurements Available: ',last)
        return   
    
    all_measurements = data['pm25 standard']
        
    # Get max and min measurements
    pm_max = all_measurements.max()
    pm_min = all_measurements.min()
    pm_range = pm_max-pm_min
    # Scaled rate of change
    scaled_roc = pm_range/pm_max
    # Weight factor
    weight_factor = 1-scaled_roc
    
    hour_measurements.reset_index()    
        
    return

