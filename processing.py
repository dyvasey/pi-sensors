"""
Data processing functions for Raspberry Pi sensors
"""
import pandas as pd
import numpy as np
import board
import digitalio

import adafruit_character_lcd.character_lcd as characterlcd

from datetime import date,timedelta,datetime

def aqi_nowcast(directory = '/home/pi/Desktop/pm25-data/'):
    """
    Calculate current AQI NowCast using last 12 hours of PM 2.5 Data.
    
    Requires data in 10 minute intervals currently. Based on
    https://usepa.servicenowservices.com/airnow?id=kb_article&sysparm_article=KB0011856
    """
    day = str(date.today())
    yesterday = str(date.today()-timedelta(days=1))
    

    data2 = pd.read_csv(directory+day+'.csv',parse_dates=[0])
    
    # Check to see if previous data avaiiable
    try:
        data1 = pd.read_csv(directory+yesterday+'.csv',parse_dates=[0])
    except:
        data = data2
    else:
        data = pd.concat([data1,data2])
        data.reset_index(inplace=True)
    
    # Get timestamps to nearest 10 minutes
    data.index = data['datetime'].dt.round('10min')
    
    
    # Get last row in combined data
    last = len(data.index)
    
    # Get every hour over past 12 hours
    now = datetime.now()
    nearest_10 = now - timedelta(minutes=now.minute % 10,
                             seconds=now.second,
                             microseconds=now.microsecond)
    
    hrs = []
    for x in range(13):
        t = nearest_10 - timedelta(hours=x)
        hrs.append(t)
    
    try:   
        hour_measurements = data.loc[hrs,'pm25 standard']
    
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
    # If weight factor <0.5, set to 0.5
    if weight_factor<0.5:
        weight_factor = 0.5
    
    hour_measurements.reset_index(inplace=True,drop=True)
    weighted_all = []
    factor_raised_all = []
    for x in range(13):
        factor_raised = weight_factor**x
        weighted = hour_measurements[x]*factor_raised
        weighted_all.append(weighted)
        factor_raised_all.append(factor_raised)
    
    sum_weighted = sum(weighted_all)
    sum_factors = sum(factor_raised_all)
    
    # Truncate pm25 to 1 decimal place
    nowcast_pm25 = round(sum_weighted/sum_factors,1)
    
    aqi,field = calc_aqi(nowcast_pm25)
        
    return(nowcast_pm25,aqi,field)

def calc_aqi(pm25):
    """
    Convert pm25 concentration to aqi
    
    Values from:
    https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf
    
    """
    # Minimum and Maximum AQI and pm25 for each category
    good = (0,50,0,12)
    moderate = (51,100,12.1,35.4)
    sensitive = (101,150,35.5,55.4)
    unhealthy = (151,200,55.5,150.4)
    v_unhealthy = (201,300,150.5,250.4)
    hazardous = (301,500,250.5,500.4)
    
    levels = {'Good':good,'Moderate':moderate,
              'Unhealthy for Sensitive Groups':sensitive,
              'Unhealthy':unhealthy,'Very Unhealthy':v_unhealthy,
              'Hazardous':hazardous}
    
    for key in levels:
        if levels[key][2] <= pm25 <= levels[key][3]:
            field = key
    try:
        values = levels[field]
    except UnboundLocalError:
        print('PM 2.5 Input: ',pm25)
        raise Exception('PM 2.5 value failed to fit into an AQI range')
        
    aqi = (
        (values[1]-values[0])/(values[3]-values[2])*(pm25-values[2])
        + values[0]
        )
    aqi_integer = round(aqi,0)
    
    return(aqi_integer,field)

def disp_aqi(pm25,aqi):
    """
    Display PM 2.5 and AQI Nowcast on LCD display
    """
    
    lcd_rs = digitalio.DigitalInOut(board.D26)
    lcd_en = digitalio.DigitalInOut(board.D19)
    lcd_d7 = digitalio.DigitalInOut(board.D27)
    lcd_d6 = digitalio.DigitalInOut(board.D22)
    lcd_d5 = digitalio.DigitalInOut(board.D24)
    lcd_d4 = digitalio.DigitalInOut(board.D25)
    lcd_backlight = digitalio.DigitalInOut(board.D4)

    lcd_columns = 16
    lcd_rows = 2
    
    lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5,
                                          lcd_d6,lcd_d7, lcd_columns,
                                          lcd_rows,lcd_backlight)
    
    # LCD on from 9 AM to 10 PM
    now = datetime.now()
    if 9<=now.hour<22:
        lcd.backlight = True
    else:
        lcd.backlight = False
    
    
    lcd.message = "PM2.5: " +str(pm25) + "\nAQI: " + str(aqi)
    return
    