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
COLUMN_NAMES  = ['date','open','high','close','low','volume','amount']

class hs300:
    def __init__(self):
        hs300File = Path(FILE_LOCATION)
        if not hs300File.is_file():
            print("HS300 file created!\n")
            self.download_hs300()
        else:
            hs300T = pd.read_csv(FILE_LOCATION)
            currentDate = time.strftime("%Y-%m-%d")
            latestDate = hs300T.loc[0, 'date']
            if  currentDate == latestDate:
                print("HS300 file already exists!\n")
                self.__hs300 = hs300T
            else:
                print("Updating HS300 file!\n")
                hs300P = ts.get_h_data(
                    HS300_INDEX,
                    index=True,
                    start=latestDate)
                hs300P = hs300P.reset_index()
                hs300P['date'] = hs300P['date'].apply(
                    lambda x: pd.to_datetime(x).date().isoformat())
                self.__hs300 = pd.concat([hs300P, hs300T[1:]])
                self.__hs300.to_csv(
                    FILE_LOCATION, encoding='utf-8', index=False)

    def get_data(self):
        return self.__hs300

    def download_hs300(self, startDate=START_DATE):
        self.__hs300 = ts.get_h_data(
            HS300_INDEX, 
            index=True, 
            start=startDate)
        self.__hs300 = self.__hs300.reset_index()
        self.__hs300['date'] = self.__hs300['date'].apply(
            lambda x: pd.to_datetime(x).date().isoformat())
        self.__hs300.to_csv(
            FILE_LOCATION, encoding='utf-8', index=False)

if __name__ == '__main__':
    h = hs300().get_data()
    #print(h.head())