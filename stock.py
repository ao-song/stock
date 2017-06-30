#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Some calculation about Chinese stock market'''

__author__ = 'Ao Song'
__email__  = 'ao.song@outlook.com'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdt

import datetime
import tushare as ts

CODE_LIST_FILE = './data/code_list.txt'
HS300_AMOUNT_FILE = './data/hs300_amount.txt'
M2_FILE = './data/m2.txt'

HS300_INDEX = '000300'
SZZS_INDEX  = '000001'
SZCZ_INDEX  = '399001'

def write_to_file(file, list):
    with open(file, 'w') as f:
        for element in list:
            f.write("%s\n" % element)

def update_stock_code():
    ic = ts.get_industry_classified()
    write_to_file(CODE_LIST_FILE, ic["code"].tolist())

'''
m2Table: m2 data of every month with index like '2017.5'
date: format like '2017.5'
'''
def get_m2_by_date(m2Table, date):  
    if (not any(m2Table['month']==date)):
        print(float(m2Table.loc[0, 'm2']))
        return float(m2Table.loc[0, 'm2'])
    return float(m2Table.loc[m2Table['month']==date]['m2'].item())


def calc_pos(n, maxN, minN):
    p = (maxN-n)/(maxN-minN)
    q = (n-minN)/(maxN-minN)
    b = (maxN-n)/(n-minN)

    return (b*p-q)/b


def turnover_regression():
    m2 = ts.get_money_supply()
    m2 = m2[m2.month >= '2005.1']
    m2.to_csv('./data/m2', encoding='utf-8')

    hs300 = ts.get_h_data(
        HS300_INDEX, 
        index=True, 
        start='2005-01-04')
    hs300.to_csv('./data/hs300', encoding='utf-8')

    regressionList = []
    latestMark = 0

    for index, row in hs300.iterrows():
        currentM2 = get_m2_by_date(m2, (str(index.year)+'.'+str(index.month)))
        mark = float(row['amount'])/currentM2
        if latestMark == 0:
            latestMark = mark
        regressionList.insert(0, mark)

    pos = calc_pos(latestMark, max(regressionList), min(regressionList))
    
    x = range(len(regressionList))
    xt = pd.read_csv('./data/hs300')['date'].tolist()
    plt.xticks(x, xt)

    plt.plot(x, regressionList)
    plt.xlabel('Position: '+str(pos))

    plt.show()


if __name__ == '__main__':
    turnover_regression()