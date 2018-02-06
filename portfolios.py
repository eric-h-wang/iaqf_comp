# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 23:49:16 2018

@author: Eric Wang, Duoxiao Chang, Yipeng Zhu
"""

from option_pricing import bs_call, bs_put, bs_straddle
import numpy as np

def Port1(data):
    data['ma60'] = data['Close'].rolling(60).mean()
    data['ma120'] = data['Close'].rolling(120).mean()
    data['position'] = 0
    data.loc[data['ma60']>=data['ma120'], 'position']=1
    data.loc[data['ma60']<data['ma120'], 'position']=-1
    data['lag_pos'] = data['position'].shift(1)
    data['lag_close'] = data['Close'].shift(1)
    data['P1_daily_return'] = (data['Close']-data['lag_close'])*data['lag_pos']
    data['P1_value'] = data['P1_daily_return'].cumsum()
    data['P1_daily_yield'] = data['P1_daily_return']/data['Close'].shift(1)
    
    
def Port2(data):
    expiry1 = 90/365
    expiry2 = 89/365
    
    data['P2_sell'] = 0
    data['P2_buy'] = 0
    
    data.loc[data['lag_pos']==1,'P2_sell'] = bs_call(data['Close'], data['r']/100, 
                                data['q']/100, data['vol'], 
                                expiry2, data['Close'].shift(1))
    data.loc[data['position']==1, 'P2_buy'] = bs_call(data['Close'], data['r']/100, 
                                data['q']/100, data['vol'], 
                                expiry1, data['Close'])
    data.loc[data['lag_pos']==-1, 'P2_sell'] = bs_put(data['Close'], data['r']/100, 
                            data['q']/100, data['vol'], 
                            expiry2, data['Close'].shift(1))
    data.loc[data['position']==-1, 'P2_buy'] = bs_put(data['Close'], data['r']/100, 
                            data['q']/100, data['vol'], 
                            expiry1, data['Close'])
    
    data['P2_daily_return'] = data['P2_sell'] - data['P2_buy'].shift(1)
    data['P2_value'] = data['P2_daily_return'].cumsum()
    data['P2_daily_yield'] = data['P2_daily_return']/data['Close'].shift(1)
    
def Port3(data):
    expiry1 = 90/365
    expiry2 = 89/365
    data['straddle3_buy'] = bs_straddle(data['Close'], data['r']/100, data['q']/100,
                                        data['vol'], expiry1, data['Close'])
    data['straddle3_sell'] = bs_straddle(data['Close'],data['r']/100, data['q']/100,
                                        data['vol'], expiry2, data['Close'].shift(1))
    
    data['P3_daily_return'] = data['straddle3_sell']-data['straddle3_buy'].shift(1)
    data.loc[data['lag_pos']==0, 'P3_daily_return'] = 0
    data['P3_value'] = data['P3_daily_return'].cumsum()
    data['P3_daily_yield'] = data['P3_daily_return']/data['Close'].shift(1)
    
def Port4(data):
    
    overhead = (data['position']==0).sum()
    start = data['Date'][overhead]
    data['day_from_start'] = (data['Date']-start).dt.days
    data['expiry'] = (90-(data['day_from_start']%90))/365
    data['straddle4_buy'] = bs_straddle(data['Close'], data['r']/100, data['q']/100,
                                        data['vol'], data['expiry'], data['Close'])
    data['straddle4_sell'] = bs_straddle(data['Close'], data['r']/100, data['q']/100,
                                        data['vol'], data['expiry'].shift(1)-1/365, data['Close'].shift(1))
    
    data['P4_daily_return'] = data['straddle4_sell'] - data['straddle4_buy'].shift(1)
    data.loc[data['lag_pos']==0, 'P4_daily_return'] = 0
    data['P4_value'] = data['P4_daily_return'].cumsum()
    data['P4_daily_yield'] = data['P4_daily_return']/data['Close'].shift(1)

if __name__ == '__main__':
    from data_handling import match_data
    from option_pricing import hist_vol
    data = match_data()
    hist_vol(data, 30)
    Port1(data)
    Port4(data)
    data.plot(y=['P1_value', 'P4_value'])