# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:40:57 2018

@author: MattPetraites
"""

''' Trailing annual earnings-to-price Factor construction.
    
    Assumes variables 'EPS' in the input dataframe containing EPS data and
    'PRC' the share price of the stock.
    
    Assumes Monthly returns data so that 'last four reportings of EPS' correspond
    to a 3, 6, 9, and 12 shift in the dataframe. Note that missing data must have
    been filled in order to compute these factors! Cannot compute factor using below
    code if EPS data has not been filled. 
    
    Concstructs an 'ETOP' variable in the dataframe for the last n entries.
'''

def constructETOP(df,n = len(df)):
    data = df.tail(n)
    data["ETOP"] = (data.EPS.shift(3)+data.EPS.shift(6)+data.EPS.shift(9)+data.EPS.shift(12))/data.PRC
    return data

''' Share Turnover per Month

    Assumes variables 'VOL' and 'SHROUT' in the input dataframe containing
    monthly share volume and the number of shares outstanding.
    
    Also assumes monthly returns data. 
'''

def constructSTOM(df, n = len(df)):
    data = df.tail(n)
    data["STOM"] = data.VOL / data.SHROUT.shift(1)
    return data
    