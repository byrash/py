#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 14:10:27 2017

@author: Shivaji
"""

import os
import glob
import pandas

def concatenate(indir="/Users/Shivaji/tmp/extracted",outfile="/Users/Shivaji/tmp/extracted/Concatednated.csv"):
    os.chdir(indir)
    fileList = glob.glob("*.csv")
    colnames=['Year','Month','Day','Hour','Temp','DewTemp','Pressure','WinDir','WinSpeed','Sky','Precip1','Precip6','ID']
    dfList=[]
    for filename in fileList:
        df = pandas.read_csv(filename,header=None)
        dfList.append(df)
    concatedDf = pandas.concat(dfList,axis=0)
    concatedDf.columns = colnames
    concatedDf.to_csv(outfile,index=None)