#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd

from pathlib import Path
import time

''' About HS300 '''

#------------------------------------------------------------------------------

__author__ = 'Ao Song'
__email__  = 'ao.song@outlook.com'


START_DATE    = '2005-01-04'
FILE_LOCATION = './data/hs300'
HS300_INDEX   = '000300'

class hs300:
    def __init__(self):
        hs300File = Path(FILE_LOCATION)
        if not hs300File.is_file():
            print("HS300 file created!\n")
            self.download_hs300()
        else:
            hs300T = pd.read_csv(
                FILE_LOCATION, 

                parse_dates=True)
            currentDate = time.strftime("%Y-%m-%d")
            latestDate = hs300T.loc[0, 'date']
            if  currentDate == latestDate:
                print("HS300 file already exists!\n")
                self.__hs300 = hs300T
            else:
                print("Updating HS300 file!\n")
                self.download_hs300()

    def get_data(self):
        return self.__hs300

    def download_hs300(self):
        self.__hs300 = ts.get_h_data(
            HS300_INDEX, 
            index=True, 
            start=START_DATE)
        self.__hs300.to_csv(FILE_LOCATION, encoding='utf-8')

if __name__ == '__main__':
    h = hs300().get_data()
    print(h.head())