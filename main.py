# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 23:54:51 2018

@author: Eric Wang, Duoxiao Chang, Yipeng Zhu
"""

import matplotlib.pyplot as plt
#import analysis as ANA
from option_pricing import hist_vol
from portfolios import Port1, Port2, Port3, Port4
from data_handling import match_data, get_data

get_data()
data = match_data()
hist_vol(data, 30)

Port1(data)
Port2(data)
Port3(data)
Port4(data)

data = data.loc[121:,]
data.to_csv('../Results/result.csv')

plt.hist(data[["P1_daily_return", "P2_daily_return", "P2_daily_return", "P4_daily_return"]],\
         label = ['P1', 'P2', 'P3', 'P4'])

plt.legend(loc='upper left')
plt.savefig('../Results/hist.png')
data.plot(y=['P1_value', 'P2_value', 'P3_value', 'P4_value'])
plt.savefig('../Results/value.png')
data.plot(y=['P1_daily_return', 'P2_daily_return', 'P3_daily_return', 'P4_daily_return'])
plt.savefig('../Results/daily_return.png')