# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 14:55:52 2018

@author: Eric Wang
"""

import numpy as np
from scipy.stats import norm

# calculate historical volatility
def hist_vol(data, window):
    data['lag_close'] = data['Close'].shift(1)
    data['log_return'] = np.log(data['Close']/data['lag_close'])
    data['vol'] = data['log_return'].rolling(window).std()*np.sqrt(252)
    

def bs_call(spot, r, q, vol, expiry, strike):
    d1 = (np.log(spot/strike)+(r-q+0.5*vol*vol)*expiry)/vol/np.sqrt(expiry)
    d2 = d1 - vol*np.sqrt(expiry)
    call_price = norm.cdf(d1)*spot*np.exp(-q*expiry)-norm.cdf(d2)*strike*np.exp(-r*expiry)
    return call_price
    
def bs_put(spot, r, q, vol, expiry, strike):
    d1 = (np.log(spot/strike)+(r-q+0.5*vol*vol)*expiry)/vol/np.sqrt(expiry)
    d2 = d1 - vol*np.sqrt(expiry)
    put_price = strike*np.exp(-r*expiry)*norm.cdf(-d2)-norm.cdf(-d1)*spot*np.exp(-q*expiry)
    return put_price
    
def bs_straddle(spot, r, q, vol, expiry, strike):
    return bs_call(spot, r, q, vol, expiry, strike) + bs_put(spot, r, q, vol, expiry, strike)

