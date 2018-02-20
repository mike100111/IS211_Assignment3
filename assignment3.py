# -*- coding: cp1252 -*-

import urllib2
import datetime
import logging
import argparse
import sys
import os
import csv
import re


##Method to download the data from the specified url
def downloadData(url):
    ##open url
    f = urllib2.urlopen(url)
   
    ##return read data to calling Method
    return f

##Method to parse the downloaded data in a valid dictionary
def processData(data):
    ##Get the configured logger
    logger = getLogger()

    parsedData = []    
    reader = csv.reader(data)
    for row in reader:
        rowData = {'path': row[0], 'dateAccessed': row[1], 'browser': row[2], 'status': row[3], 'size': row[4] } 
        parsedData.append(rowData)
    
    return parsedData  

## Searches for images in the data
def searchImages(data):
    imageCount = 0
    firefox = 0
    chrome = 0
    safari = 0
    ie = 0

    #for m in re.findall('([-\w]+\.(?:jpg|gif|png))', data):
    #print m

    i = 0
    while i < len(data):       
            
        if re.search('([-\w]+\.(?:jpg|gif|png))', data[i]['path']):
            imageCount += 1
       
        regexp = re.compile(r'Chrome')
        if regexp.search(data[i]['browser']):
            chrome +=1
        regexp2 = re.compile(r'Safari')
        if regexp2.search(data[i]['browser']):
            safari +=1
        regexp3 = re.compile(r'Firefox')
        if regexp3.search(data[i]['browser']):
            firefox +=1
        regexp3 = re.compile(r'MSIE')
        if regexp3.search(data[i]['browser']):
            ie +=1
            
        i += 1
    print('Image requests account for ' + str(100 * float(imageCount)/float(i)) + '% of all requests')

    greatestName = ''
    greatest = safari
    greatestName = 'Safari'
    if chrome > greatest:
        greatest = chrome
        greatestNamew = 'Chrome'
    if firefox > greatest:
        greatest = firefox
        greatestName = 'Firefox'
    if ie > greatest:
        greatest = ie
        greatestName = 'IE'
    
    print greatestName + ' was the most popular today.'
    
def getLogger():

     ##configure logger
    logger = logging.getLogger(__name__)
    hdlr = logging.FileHandler('C:\Users\Meir\Documents\IS211\IS211_Assignment2\errors.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.ERROR)
    return logger

def main():

    ##Add the --url parameter requirement
    #parser = argparse.ArgumentParser()
    #parser.add_argument("url")
    #args = parser.parse_args()   

    ##donwlaod csv data
    #csvData = downloadData(sys.argv[1])

    csvData = downloadData('http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv')    

    ##Process csv data
    data = processData(csvData)

    searchImages(data)
main() 
