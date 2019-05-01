#

import sys
import time
import shutil
import cmdArgs
from spamGen import SpamGenerator
from logFile import LogFileTrunc, LogFileRename
from pathlib import Path

# =======================
# CONFIGURATION
# =======================
fileNameTemplate = "testLog"

refFileName = "refLog"

fileNamesList = (
    "logFirst", "logSecond",
    "AlgTwo_0", "AlgTwo_1",
    "fileWithDataOne", "fileWithDataTwo")

myConfig = cmdArgs.Config()

myConfig.addParam( "sleep",          "s", "0", "Tenths of seconds to wait before adding new portion of lines to logs" )
myConfig.addParam( "out-dir",        "o", "D:\\test\\logs", "Directory where logs storage files resides" ) 
myConfig.addParam( "size-threshold", "t", "20480",          "Size threshold when log must be archived" ) 
myConfig.addParam( "total-size",     "T", "51200",          "Total size to generate" ) 
myConfig.addParam( "noarchive",      "A", False,            "Do we need to really compress log files?" )
myConfig.addParam( "noprogress",     "P", False,            "Show progress?" )

# =============================
# FUNCTIONS
# =============================
def processLogFileObject( logFileObj, noProgress, deciSec ):
    ite = 0
    gen = SpamGenerator()
    # setup sleep
    noSleep = int( deciSec ) <= 0
    sleepSSec = int(deciSec) * 0.1
    progr = logFileObj.getProgress()
    while progr < 1.0:
        if not noProgress:
            if printProgressTick( progr, 1 ):
                print("|", sep='', end="", flush=True ) # print progress in console


        #for log in logsList:
        newLine = "{0}: line {1:04d}: {2}".format(
                                               time.strftime("%H:%M:%S_%d.%m.%y"),
                                               ite, gen.generateMessage( ite ) )
        #refFile.write( newLine + '\n' )
        logFileObj.addContent( newLine )
        ite +=1


        if not noSleep:
            time.sleep( sleepSSec )
        progr = logFileObj.getProgress()
        #print( "{0:2.2f} ".format( progr ) , sep="", end="", flush=True ) # print progress in console
    print("|", sep='', flush=True ) # print progress in console


def getTotalProgress( logsList ):
    sumOfProgr = 0
    for log in logsList:
        progr = log.getProgress()
        sumOfProgr += 1.0 if  progr > 1.0 else progr
    return sumOfProgr / len( logsList )

intervalIndex = 0
def printProgressTick( cur, total ):
    # convert to 0-100 interval
    cur = int( cur/total * 100 )
    total = 100
    cell = 10
    global intervalIndex
    # get cell index (interval index) inside mesh
    # we assume that progress can only increase from step to step
    # hence, when posInCell become higher than the middle of the cell
    # we can print progress tick
    res = False
    if cur // cell > intervalIndex:
        intervalIndex = cur // cell
        res = True
    elif cur // cell == intervalIndex:
        res = False

    return res
    
# =======================
# MAIN
# =======================
def main( argv ) :

    if myConfig.parseCmdLine( argv ) != 0:
        myConfig.printUsage()
        return 0

    outDir          = myConfig.getParamVal( "out-dir" )
    deciSec         = int( myConfig.getParamVal( "sleep" ) )
    noArchive       = myConfig.getParamVal( "noarchive" )
    noProgress      = myConfig.getParamVal( "noprogress" )
    sizeThreshold   = int( myConfig.getParamVal( "size-threshold" ) )
    totalBytesOnLog = int( myConfig.getParamVal( "total-size" ) )

    # setup sleep
    noSleep = int( deciSec ) <= 0
    sleepSSec = int(deciSec) * 0.1

    if not Path( outDir ).exists():
        print( "{0} - NO such directory! Cannot work further...".format( outDir ) )
        exit()

    gen = SpamGenerator()

    refFile = open( "{0}\\..\\{1}.txt".format( outDir, refFileName ), "w" )

    # def __init__( self, outDir, fileName, threshold, maxBytes ):
    # logsList = [ LogFile( outDir, name, 1024, 1050, noArchive ) for name in fileNamesList ]
    logsList = [ LogFileTrunc( outDir, fileNamesList[0], sizeThreshold, totalBytesOnLog, noArchive ),
                    LogFileTrunc( outDir, fileNamesList[1], sizeThreshold, totalBytesOnLog, noArchive ),
                    LogFileRename( outDir, fileNamesList[2], sizeThreshold, totalBytesOnLog, noArchive ),
                    LogFileRename( outDir, fileNamesList[3], sizeThreshold, totalBytesOnLog, noArchive ) ]
    # ============================================================
    ite = 0
    totalProgress = getTotalProgress( logsList )
    while totalProgress < 1.0:
        if not noProgress:
            if printProgressTick( totalProgress, 1 ):
                print("|", sep='', end="", flush=True ) # print progress in console

        for log in logsList:
            # Process one log file ===============================
            newLine = "{0}: line {1:04d}: {2}".format(
                                                   time.strftime("%H:%M:%S_%d.%m.%y"),
                                                   ite, gen.generateMessage( ite ) )
            refFile.write( newLine + '\n' )
            log.addContent( newLine )
            ite +=1
        if not noSleep:
            time.sleep( sleepSSec )
        totalProgress = getTotalProgress( logsList )
        #print( "{0:2.2f} ".format( totalProgress ) , sep="", end="", flush=True ) # print progress in console
    print("|", sep='', flush=True ) # print progress in console
    # =======================================

if __name__ == "__main__" :
    main( sys.argv )

# class CmdLineOption:
#     def __init__(self, name, defVal ):
#         self.name = name
#         self.defVal = defVal
#         self.cmdLineArgLong = "--arg1"
#         self.cmdLineArgShort = "-a1"

