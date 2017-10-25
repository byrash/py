#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:21:06 2017

@author: Shivaji
"""

import pandas

thefts = pandas.read_excel("thefts-and-pop.xls",sheetname=0)
population = pandas.read_excel("thefts-and-pop.xls",sheetname=1)
thefts["key"]=(thefts["State"]+" - "+thefts["County"]).str.lower()
population["key"]=(population["State"]+" - "+population["County"]).str.lower()
thefts_popu= pandas.merge(left=thefts,right=population, left_on="key", right_on="key", how="outer")
print(thefts_popu.shape)
#print(population.shape)
#print(thefts.shape)