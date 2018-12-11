#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import copy
import time
"""
Created on Thu Dec  6 00:58:33 2018

@author: RobertXu
"""

def AddSTOAFactor(df):
    '''
    Share turnover over last year:
    Trade volume "VOL" and shares outstanding "SHROUT" in df are REQUIRED
    '''
    # Can also consider using volume to variance
    try:
        # Vann = total trade volume over last 12 months
        Vann = df.VOL.rolling(12).sum()
        # Nout = average shares outstanding over last 12 months
        Nout = df.SHROUT.rolling(12).mean() * 1000
        df["TradingActivity"] = Vann / Nout
    except Exception as e:
        print("Failed to Construct TradingActivity for Stock " + df.TICKER.iloc[-1])
        print(str(e))
        
def AddPAYOFactor(df):
    ''' 
        Payout ratio over the last year (Growth factor)
        Assumes variable "EPS" earnings per share is in the input dataframe
        Outstanding shares "SHROUT" and dividend yield "divyield" required
        
    '''
    try:
        # Fill in na values with 0, this means these stocks don't pay dividends
        # Div: aggregate dividend paid 
        Div = df.divyield.fillna(0) * df.PRC * df.SHROUT * 1000
        # Earn: total earnings for common shareholders
        Earn = df.EPS * df.SHROUT * 1000
        df["PAYO"] = Div.rolling(12).mean() / Earn.rolling(12).mean()
    except Exception as e:
        print("Failed to Construct Payout Ratio for Stock " + df.TICKER.iloc[-1])
        print(str(e)) 
    
def AddRecentEarningsChangeFactor(df):
    '''
        Measures recent earning growth
        Assumes variable "EPS" earnings per share is in the input dataframe
        Factor name: DELE
    '''
    try:
        df["DELE"] = 2 * (df.EPS.shift(1) - df.EPS) / (df.EPS.shift(1) + df.EPS)
    except Exception as e:
        print("Failed to Construct DELE for Stock " + df.TICKER.iloc[-1])
        print(str(e))
"""       
Need book value of long term debt and book value prefered equity  
def AddVariabilityCapitalStructure(df):
    '''
        Outstanding shares "SHROUT", price "PRC"
    '''
    abs(df.SHROUT.shift(1) - df.SHROUT) * df.PRC + 

"""

if __name__ == "__main__":
    test = pd.read_csv("./data/test.csv")