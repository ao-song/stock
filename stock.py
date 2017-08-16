#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Some calculation about Chinese stock market'''

__author__ = 'Ao Song'
__email__  = 'ao.song@outlook.com'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdt
import time

import tushare as ts

from hs300 import hs300
from m2 import m2

'''
CODE_LIST_FILE = './data/code_list.txt'

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

def calc_pos(n, maxN, minN):
    p = (maxN-n)/(maxN-minN)
    q = (n-minN)/(maxN-minN)
    b = (maxN-n)/(n-minN)

    return (b*p-q)/b


def turnover_regression():
    m = m2()
    h = hs300()

    regressionList = []
    latestMark = 0

    for index, row in h.get_data().iterrows():
        t = time.strptime(row['date'], '%Y-%m-%d')
        currentM2 = m.get_monthly_m2((str(t.tm_year)+'.'+str(t.tm_mon)))
        mark = float(row['amount'])/currentM2
        if latestMark == 0:
            latestMark = mark
        regressionList.insert(0, mark)

    pos = calc_pos(latestMark, max(regressionList), min(regressionList))
    
    '''
    x = range(len(regressionList))
    xt = pd.read_csv('./data/hs300')['date'].tolist()
    plt.xticks(x, xt)

    plt.plot(x, regressionList)
    plt.xlabel('Position: '+str(pos))
    '''
    plt.plot(regressionList)
    plt.xlabel('Position: '+str(pos))

    plt.show()


if __name__ == '__main__':
    turnover_regression()
