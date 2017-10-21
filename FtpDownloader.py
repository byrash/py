#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 10:17:13 2017

@author: Shivaji
"""

from ftplib import FTP, error_perm
import os

def ftpDownloaderOld(fileName, host="ftp.pyclass.com", userName="student@pyclass.com", password="student123"):
    ftp=FTP(host)
    ftp.login(userName,password)
    ftp.cwd("Data")
    os.chdir("/Users/Shivaji/tmp")
    with open(fileName,"wb") as file:
        ftp.retrbinary("RETR %s" %fileName, file.write)

def ftpLogin(ftpHost="ftp.pyclass.com", ftpUserName="student@pyclass.com", ftpPassword="student123"):
    ftp=FTP(ftpHost)
    ftp.login(ftpUserName,ftpPassword)
    return ftp

def setLocalWorkingDir(workingDir):
    if not os.path.exists(workingDir):
        os.makedirs(workingDir)
    os.chdir(workingDir)

def ftpDownloader(stationIds, startYear, endYear, ftpHost="ftp.pyclass.com", ftpUserName="student@pyclass.com", ftpPassword="student123"):
    ftp = ftpLogin(ftpHost,ftpUserName,ftpPassword)
    setLocalWorkingDir("/Users/Shivaji/tmp")
#    ftp.cwd("/Data") -- Current working directry is not being retained in loop
    for year in range(startYear, endYear+1):
#        file path format is Year/station-id-Year.gz
        for stationId in stationIds:
            serverFilePath= '/Data/%s/%s-%s.gz'%(year,stationId,year)
            localFileName = os.path.basename(serverFilePath)
            try:
                with open(localFileName,'wb') as file:
                    ftp.retrbinary('RETR %s'%serverFilePath,file.write)
                    print("%s successfully downloaded"%serverFilePath)
            except error_perm:
                print('%s is not available'%serverFilePath)
                os.remove(localFileName)
    ftp.close()


