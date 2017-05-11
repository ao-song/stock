#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Some calculation about Chinese stock market'''

__author__ = 'Ao Song'
__email__  = 'ao.song@outlook.com'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    float(m2.loc[m2['month']==date]['m2'].item())


def turnover_regression():
	m2 = ts.get_money_supply()
	m2 = m2[m2.month >= '2005.1']
	# write_to_file(M2_FILE, m2["m2"].tolist())

	hs300 = ts.get_h_data(
		HS300_INDEX, 
		index=True, 
		start='2005-01-04', 
		end='2017-05-10')
	# write_to_file(HS300_AMOUNT_FILE, hs300["amount"].tolist())

	for index, row in hs300.iterrows():
		currentM2 = get_m2_by_date(m2, (str(index.year)+'.'+str(index.month)))


if __name__ == '__main__':
	turnover_regression()