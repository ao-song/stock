#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd

from pathlib import Path
import time

''' About M2 '''

#------------------------------------------------------------------------------

__author__ = 'Ao Song'
__email__  = 'ao.song@outlook.com'


START_MONTH   = '2005.1'
FILE_LOCATION = './data/m2'

class m2:
    def __init__(self):
        m2File = Path(FILE_LOCATION)
        if not m2File.is_file():
            print("M2 file created!\n")
            self.download_m2()
        else:
            m2T = pd.read_csv(FILE_LOCATION)
            '''
            lstrip()?
            '''
            currentMonth = time.strftime("%Y") + \
                           '.' + \
                           str(int(time.strftime("%m")))
            latestMonth = m2T.iloc[0,1]
            if  currentMonth == latestMonth:
                print("M2 file already exists!\n")
                self.__m2 = m2T
            else:
                print("Updating M2 file!\n")
                self.download_m2()

    def get_monthly_m2(self, month):
        if (not any(self.__m2['month']==month)):
            print(float(self.__m2.loc[0, 'm2']))
            return float(self.__m2.loc[0, 'm2'])
        return float(self.__m2.loc[self.__m2['month']==month]['m2'].item())

    def download_m2(self):
        m2T = ts.get_money_supply()
        self.__m2 = m2T[m2T.month >= START_MONTH]
        self.__m2.to_csv(FILE_LOCATION, encoding='utf-8')

if __name__ == '__main__':
    m = m2()
    print(m.get_monthly_m2("2015.9"))

