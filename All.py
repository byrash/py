#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:44:35 2017

@author: Shivaji
"""

from ftplib import FTP, error_perm
import os
import glob
import pandas
import patoolib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy
import simplekml

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

#ftpDownloader(['010010-99999','010014-99999','010020-99999','010030-99999'],1950,2014)
def ftpDownloader(stationIds, startYear, endYear, ftpHost="ftp.pyclass.com", ftpUserName="student@pyclass.com", ftpPassword="student123"):
    ftp = ftpLogin(ftpHost,ftpUserName,ftpPassword)
    setLocalWorkingDir("/Users/Shivaji/tmp")
#    ftp.cwd("/Data") -- Current working directry is not being retained in loop
    files=os.listdir('.')
    for year in range(startYear, endYear+1):
#        file path format is Year/station-id-Year.gz
        for stationId in stationIds:
            serverFilePath= '/Data/%s/%s-%s.gz'%(year,stationId,year)
            localFileName = os.path.basename(serverFilePath)
            if localFileName not in files:
                try:
                    with open(localFileName,'wb') as file:
                        ftp.retrbinary('RETR %s'%serverFilePath,file.write)
                        print("%s successfully downloaded"%serverFilePath)
                except error_perm:
                    print('%s is not available'%serverFilePath)
                    os.remove(localFileName)
            else:
                print('File %s already exists in downlod folder.'%localFileName)
    ftp.close()


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
            print("Archive extract file %s exists"%archive[:-3])

def addField(indir="/Users/Shivaji/tmp/extracted"):
    os.chdir(indir)
    fileList=glob.glob("*")
    for fileName in fileList:
        df = pandas.read_csv(fileName, sep='\s+',header=None)
        df["Station"]=[fileName.rsplit("-",1)[0]]*df.shape[0]
        df.to_csv(fileName+".csv",index=None,header=None)

def concatenate(indir="/Users/Shivaji/tmp/extracted",outfile="/Users/Shivaji/tmp/Concatednated.csv"):
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

def merge(left="/Users/Shivaji/tmp/Concatednated.csv",right="/Users/Shivaji/tmp/station-info.txt", output="/Users/Shivaji/tmp/Concatednated_merged.csv"):
    leftDf = pandas.read_csv(left)
    rightDf = pandas.read_fwf(right, converters={"USAF":str,"WBAN":str})
    rightDf["USAF_WBAN"]= rightDf["USAF"]+'-'+rightDf["WBAN"]
    mergedDf = pandas.merge(leftDf,rightDf.ix[:,["USAF_WBAN","STATION NAME","LAT","LON"]], left_on="ID",right_on="USAF_WBAN")
    mergedDf.to_csv(output)

def pivot(infile="/Users/Shivaji/tmp/Concatednated_merged.csv", outfile="/Users/Shivaji/tmp/Pivoted.csv"):
    df = pandas.read_csv(infile, low_memory=False)
    df= df.replace(-9999, numpy.nan)
    df["Temp"]= df["Temp"]/10.0
    table= pandas.pivot_table(df,index=["ID","LON","LAT","STATION NAME"],columns="Year",values="Temp")
    table.to_csv(outfile)
    return table

def plot(outfigure="/Users/Shivaji/tmp/Ploted.png"):
    df = pivot()
    df.T.plot(subplots=True, kind="bar")
    plt.savefig(outfigure, dip=200)

def kml(inputFile="/Users/Shivaji/tmp/Pivoted.csv",outFile="/Users/Shivaji/tmp/Weather.kml"):
    kml=simplekml.Kml()
    df= pandas.read_csv(inputFile,index_col=["ID","LON","LAT","STATION NAME"])
    for lon,lat,name in zip(df.index.get_level_values("LON"),df.index.get_level_values("LAT"),df.index.get_level_values("STATION NAME")):
        kml.newpoint(name=name, coords=[(lon,lat)])
        kml.save(outFile)

if __name__ == "__main__":
    #stationIdList=["010010-99999","010014-99999","010015-99999"]
    stationsStr= input("Enter statins names seperated by commas: ")
    startYear= input("Enter starting year: ")
    endyear= input("Enter end year: ")
    stationIdList= stationsStr.split(",")
    ftpDownloader(stationIdList,int(startYear),int(endyear))
    extractFiles()
    addField()
    concatenate()
    merge()
    pivot()
    kml()
    plot()