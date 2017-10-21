#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 13:12:34 2017

@author: Shivaji
"""

import os
import glob
import pandas

def addField(indir="/Users/Shivaji/tmp/extracted"):
    os.chdir(indir)
    fileList=glob.glob("*")
    for fileName in fileList:
        df = pandas.read_csv(fileName, sep='\s+',header=None)
        df["Station"]=[fileName.rsplit("-",1)[0]]*df.shape[0]
        df.to_csv(fileName+".csv",index=None,header=None)
