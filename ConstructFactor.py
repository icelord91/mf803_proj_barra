# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 11:20:54 2018

@author: yyang
"""

import numpy as np
import pandas as pd

# import indicators and fill the nan
data = pd.read_csv(r"C:\Users\yyang\OneDrive\Documents\Documents\BU\Courses\MF803\Assignments\project\data\data.csv", 
                   dtype=dict(zip(["permno","public_date","bm","capital_ratio","debt_invcap","equity_invcap","curr_debt","lt_debt","debt_at"], 
                                  [int, int, float, float, float, float, float, float, float])))

datalist = data.set_index(['permno', 'public_date'], drop = False)
datalist = datalist.sort_index().fillna(method = 'ffill')

# Construct leverage 
def constructLeverage(df,n):
    data = df.tail(n)
    BLEV = 1/data['capital_ratio'] * data['debt_invcap'] * 1/data['equity_invcap']
    DTOA = (data['curr_debt'] + data['lt_debt']) * data['debt_at']
    data['Leverage'] = 1/2 * BLEV + 1/2 * DTOA
    return data

def constructValue(df, n):
    data = df.tail(n)
    data['Value'] = data['bm']
    return data

datalist = constructLeverage(datalist, 5)
datalist = constructValue(datalist, 5)