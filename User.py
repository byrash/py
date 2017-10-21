#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 16:14:43 2017

@author: Shivaji
"""

def milesToKm(miles):
    km=miles*1.60934
    print(km)

m=input("Please enter miles:")
m=float(m)
milesToKm(m)