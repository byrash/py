#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 11:27:09 2017

@author: Shivaji
"""

import os
import glob
import patoolib

def setExtractDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def extractFiles(indir="/Users/Shivaji/tmp",outdir="/Users/Shivaji/tmp/extracted"):
    os.chdir(indir)
    archives = glob.glob("*.gz")
    setExtractDir(outdir)
    files=os.listdir(outdir)
    for archive in archives:
        if archive[:-3] not in files:
            patoolib.extract_archive(archive,outdir=outdir)
        else:
            print("Archive file %s exists"%archive[:-3])