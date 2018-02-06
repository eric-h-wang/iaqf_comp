# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 08:30:23 2018

@author: Eric Wang, Duoxiao Change, Yipeng Zhu
"""

import pandas_datareader.data as web
import datetime
import pandas as pd

def get_data():
    start = datetime.datetime(2008, 6, 4)
    end = datetime.datetime(2018,1,25)
    data = web.DataReader('^GSPC', 'yahoo', start, end)
    data.to_csv('../Data/sp500_10yr.csv')

def match_data():
    data = pd.read_csv("..\Data\sp500_10yr.csv")
    data['Date'] = pd.to_datetime(data['Date'], infer_datetime_format=True)
    r = pd.read_csv("..\Data\T-Bill.csv")
    r['Date'] = pd.to_datetime(r['Date'], infer_datetime_format=True)
    data = data.merge(r, on='Date', how='left')
    data.loc[data['r'].isnull(), 'r'] = ((data['Date']-data['Date'].shift(1))*data['r'].shift(-1)
                                        +(data['Date'].shift(-1)-data['Date'])*data['r'].shift(1))\
                                        /(data['Date'].shift(-1)-data['Date'].shift(1))
    data['year'] = data['Date'].dt.year
    q = pd.read_csv('../Data/Dividend_yield.csv')
    q['year'] = pd.to_datetime(q['Date'], infer_datetime_format=True).dt.year
    q.drop('Date', axis=1, inplace=True)
    data = data.merge(q, on='year', how='left')
    data.drop('year', axis=1, inplace=True)
    
    return data

if __name__ == '__main__':
    data = match_data()
    data.plot(y=['r', 'q'])