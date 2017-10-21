#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 07:21:02 2017

@author: Shivaji
"""

import pandas
import numpy

def pivot(infile="/Users/Shivaji/tmp/extracted/Concatednated_merged.csv", outfile="/Users/Shivaji/tmp/extracted/Pivoted.csv"):
    df = pandas.read_csv(infile)
    df= df.replace(-9999, numpy.nan)
    df["Temp"]= df["Temp"]/10.0
    table= pandas.pivot_table(df,index=["ID"],columns="Year",values="Temp")
    table.to_csv(outfile)