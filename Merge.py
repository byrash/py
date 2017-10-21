#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 15:03:04 2017

@author: Shivaji
"""
import pandas

def merge(left="/Users/Shivaji/tmp/extracted/Concatednated.csv",right="/Users/Shivaji/tmp/extracted/station-info.txt", output="/Users/Shivaji/tmp/extracted/Concatednated_merged.csv"):
    leftDf = pandas.read_csv(left)
    rightDf = pandas.read_fwf(right, converters={"USAF":str,"WBAN":str})
    rightDf["USAF_WBAN"]= rightDf["USAF"]+'-'+rightDf["WBAN"]
    mergedDf = pandas.merge(leftDf,rightDf.ix[:,["USAF_WBAN","STATION NAME","LAT","LON"]], left_on="ID",right_on="USAF_WBAN")
    mergedDf.to_csv(output)