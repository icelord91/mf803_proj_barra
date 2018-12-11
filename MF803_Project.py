# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 21:11:49 2018

@author: MattPetraites
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from itertools import chain, combinations


if __name__=="__main__":
    
    ## Pre-processing of data into "data" Dataframe
    
    priceData = pd.read_csv("MF803_PriceData.csv")
    epsData = pd.read_csv("MF803_EPSData.csv")
    
    # Create a list of all tickers common to both datasets
    
    pt = priceData["TICKER"].unique()
    et = epsData["TICKER"].unique()
    
    ticks = pt[np.in1d(pt,et)]
    
    # Make a master a Dataframe for only tickers common to both datasets
    
    pData = priceData.loc[priceData["TICKER"].isin(ticks)]
    eData = epsData.loc[epsData["TICKER"].isin(ticks)]
    
    # eData dataset is built as a number of entries for just EPS, followed
    # by the same number of entries for DPS. Our goal is to create one dataframe
    # with EPS and DPS data in the same row observation
    
    df1 = eData[eData.MEASURE == "EPS"]
    df2 = eData[eData.MEASURE == "DPS"]
    
    df1 = df1.rename(index=str,columns={"VALUE": "EPS"})
    df2 = df2.rename(index=str,columns={"VALUE": "DPS"})
    
    eData = pd.merge(df1,df2,how="inner",on=["TICKER","PENDS"])
    
    # Now merge eData and pData to make a utility dataframe that will be sculpted
    # into our master dataframe. Utilize a left join since the pData dataset is monthly
    # whereas the eData dataset is quarterly. 
    
    AA = pd.merge(pData,eData,how="left",left_on=["TICKER","date"],
                  right_on=["TICKER","PENDS"])
    
    # Now will fill NA values for EPS and DPS. For simplicity, assume that the EPS
    # and DPS holds constant for the two months following a quarterly report
    
    for t in ticks:
        AA.loc[AA.TICKER==t] = AA[AA["TICKER"] == t].fillna(method="ffill")
    
    # Master dataset only cares about the following variables, so construct it as such
    
    data = AA[['PERMNO','date','TICKER','PRC','RET','VOL','SHROUT','EPS','DPS']]
    
    # Convert the datatype of relevant variables, and clean anomalous values
    
    data["PRC"] = data.PRC.astype(float)
    
    data["RET"] = data.RET.replace({"B":"-100","C":"-200"})
    data["RET"] = data.RET.astype(float)
    data.loc[data[data["RET"]<-99].index,"RET"] = np.nan
    
    data["EPS"] = data.EPS.astype(float)
    data["DPS"] = data.DPS.astype(float)
    data["SHROUT"] = data.SHROUT.astype(float)*1000
    
    # Getting 1-Mo Risk-Free rate from Ken French's data
    
    kfData = pd.read_csv("KFData_3Factor.csv",header=3)
    kfData = kfData.rename(index=str,columns={"Unnamed: 0": "date"})
    beg = int(kfData.index[kfData["date"] == str(data.date.iloc[0])[:6]][0])
    end = int(kfData.index[kfData["date"] == str(data.date.iloc[-1])[:6]][0])+1
    rf = kfData[beg:end][["date","RF"]]
    rf = rf.astype(float)
    rf["RF"] = rf.RF / 100
    rf["date"] = data.date.unique()
    data = pd.merge(data,rf,how="left",on="date")
    
    ## Construction of ETOP and STOM factors
    
    
    
    ## Add Control Size and Momentum
    
    data["LSIZE"] = np.log(data.SHROUT * data.PRC)
    
    for t in ticks:
        data.loc[data.TICKER==t,"RSTR"] = (np.log(data[data["TICKER"]==t].RET + 1) - np.log(data[data["TICKER"]==t].RF + 1)).rolling(12).sum()
        data["ETOP"] = (data.EPS.shift(3)+data.EPS.shift(6)+data.EPS.shift(9)+data.EPS.shift(12))/data.PRC
        data["STOM"] = data.VOL / data.SHROUT.shift(1)
        
    data = data.dropna()
      
    def powerset(seq):
        if len(seq) <= 1:
            yield seq
            yield []
        else:
            for item in powerset(seq[1:]):
                yield [seq[0]]+item
                yield item
            
    Y = data["RET"]
    X = []
    regs = powerset(["LSIZE","RSTR","ETOP","STOM"])
    for i in range(16):
        r = regs.__next__()
        if r != []:
            X = data[r]
            model = sm.OLS(Y,X).fit()
            print(model.summary())   
    
    