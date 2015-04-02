#!/usr/bin/python
'''
This script goes through .mapping directories printing historical change log 
based on timestamps within the dirs and filenames

Author: daniel.borek@nexenta.com
'''

import fnmatch
import os
import time

def printDiff (old, new):
    '''
    print diff between newlist and oldlist
    '''
    if old == new:
            print('No changes')
    
    for i in new:
        if i not in old:
            print('-> ' + i)
            
    for i in old:
        if i not in new:
            print('<- ' +i)

def makeList (dirName):
    '''
    construct list based on directory name passed
    return list containing all views
    '''
    list = []

    for file in os.listdir(dirName):
        if fnmatch.fnmatch(file, '@@*'):
            list.append(str(file))
    return list
        
def getTime (dirName):
    '''
    given dir get it's timestamp, contained in tidyUpFile and convert to
    human readable form
    '''
    
    dateFile = '' # file containing the date string
    
    file = ''
    count = 0
    for file in os.listdir(dirName):
        if fnmatch.fnmatch(file, 'tid*'):
            dateFile = dirName + '/' + str(file)
            count += 1
    
    # read a line from dateFile and convert it
    f = open(dateFile, "r")
    dateString = '\t' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(f.readline())))

    
    if count > 1:
        dateString += ' more than one tidyUp file found'
    elif count < 1:
        dateString += ' no tidyUp file found'
    
    return dateString
    
def makeDirList ():
    '''
    return a list of all .mapping directories
    '''
    dirList = []

    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '.mapping*'):
            dirList.append(file)
    
    return dirList


# get list of directories    
dirList = makeDirList()
list.sort(dirList, reverse = True)

oldList = []
newList = []

for i in dirList:
    oldList = newList[:]
    newList = makeList(i)
    print(i + ' ' + getTime(i) + '  ' + str(len(newList)) + ' views')
    printDiff(oldList, newList)
    print('\n')
