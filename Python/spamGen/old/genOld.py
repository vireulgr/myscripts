# coding: cp1251

import sys
import time
import gzip
import shutil
from pathlib import Path
from spamGen import SpamGenerator
from logFile import LogFileTrunc, LogFileRename

# =======================
# CONFIGURATION
# =======================
fileNameTemplate = "testLog"

refFileName = "refLog"

#sizeThreshold = 1024 * 2 # number of kibibytes
sizeThreshold = 1024 * 5

totalBytesOnLog = 1024 * 50

fileNamesList = (
    "logFirst", "logSecond",
    "AlgTwo_0", "AlgTwo_1",
    "fileWithDataOne", "fileWithDataTwo")

# =============================
# FUNCTIONS
# =============================
def getTotalProgress( logsList ):
    sumOfProgr = 0
    for log in logsList:
        progr = log.getProgress()
        sumOfProgr += 1.0 if  progr > 1.0 else progr
    return sumOfProgr / len( logsList )

intervalIndex = 0
#printedInCurInterval = False

def printProgressTick( cur, total ):
    # convert to 0-100 interval
    cur = int( cur/total * 100 )
    total = 100
    cell = 10
    #global printedInCurInterval
    global intervalIndex
    # make a 10-unit mesh and find position of cur in a cell of a mesh
    #posInCell = cur % cell
    # get cell index (interval index) inside mesh
    #intervalIndex = cur / cell
    # we assume that progress can only increase from step to step
    # hence, when posInCell become higher than the middle of the cell
    # we can print progress tick
    #if cur > cell * 0.5 and not printedInCurInterval and cur / cell == intervalIndex:
    # print( "cur: {0}, int idx prev: {1}, int idx cur: {2}, printed: {3}"
    #         .format( cur, intervalIndex, cur // cell, printedInCurInterval ) )
    res = False
    if cur // cell > intervalIndex:
        #if printedInCurInterval:
        #    pass
        #else:
        #    printedInCurInterval = True    

        intervalIndex = cur // cell
        res = True
    elif cur // cell == intervalIndex:
        res = False
        #if printedInCurInterval:
        #    res = False
        #else:
        #    printedInCurInterval = True    
        #    res = True

    return res
    
# =======================
# MAIN
# =======================
def main( argv ) :

    iters = 0
    noSleep = False
    noArchive = False
    noProgress = False
    outDir = "d:\\test\\logs"

    argsLeft = len(argv) -1 # one for script name
    for arg in argv:
        if arg.isnumeric():
            iters = int( arg )
        #elif arg == "--nosleep":
        #    noSleep = True
        elif arg == "--noprogress":
            noProgress = True
        elif arg == "--noarchive":
            noArchive = True
        elif arg.startswith( "--out-dir" ):
            a, b, outDir = arg.partition( '=' )
        elif arg.startswith( "--sleep" ):
            a, b, deciSec = arg.partition( '=' )
        else:
            argsLeft += 1

        argsLeft -= 1

    print( outDir )
    outDirs = outDir.split()
    print( outDirs )

    if argsLeft > 0 :
        print( "Achtung! Not all arguments processed!\nArgs left: {0}".format( argsLeft ) )
        print( "Usage: {0} <args>; <args> can be:\n"
                "   <number>               - number of lines to generate\n"
                "   --out-dir=<directory> - directory where to dump files\n"
                "   --noprogress          - don't print progress in console\n"
                "   --noarchive           - don't actually gzip files, just change extension\n"
                "   --nosleep             - don't sleep between iterations,\n"
                "                           dump all lines as fast as can\n"
                )
        exit()

    # setup sleep
    noSleep = int( deciSec ) <= 0
    sleepSSec = int(deciSec) * 0.1

    if not Path( outDir ).exists():
        print( "{0} - NO such directory! Cannot work further...".format( outDir ) )
        exit()

    gen = SpamGenerator()

    refFile = open( "{0}\\..\\{1}.txt".format( outDir, refFileName ), "w" )
# =======================================================================
    # def __init__( self, outDir, fileName, threshold, maxBytes ):
    # logsList = [ LogFile( outDir, name, 1024, 1050, noArchive ) for name in fileNamesList ]
    logsList = [ LogFileTrunc( outDir, fileNamesList[0], sizeThreshold, totalBytesOnLog, noArchive ),
                    LogFileTrunc( outDir, fileNamesList[1], sizeThreshold, totalBytesOnLog, noArchive ),
                    LogFileRename( outDir, fileNamesList[2], sizeThreshold, totalBytesOnLog, noArchive ),
                    LogFileRename( outDir, fileNamesList[3], sizeThreshold, totalBytesOnLog, noArchive ) ]
    ite = 0
    totalProgress = getTotalProgress( logsList )
    while totalProgress < 1.0:
        if not noProgress:
            if printProgressTick( totalProgress, 1 ):
                print("|", sep='', end="", flush=True ) # print progress in console

        for log in logsList:
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
    print("|", sep='', end="", flush=True ) # print progress in console
# =======================================================================

    # RETURN ==================================
    return

    filePath = "{0}\\{1}.log".format( outDir, fileNameTemplate )

    logFile = open( filePath, "a" )
    
    # search for files by mask and if exists, continue counter
    # \warning template for globbing must be compatible with one 
    # that is used for gzipFileName file name creation! see below
    gzipFiles = [ x.name for x in list( Path( outDir ).glob( "{0}.*.gz".format( fileNameTemplate ) ) ) ]
    # gzipFiles.sort() not needed
    gzipFileNameCounter = len(gzipFiles) != 0 and int( (gzipFiles[-1].split('.'))[-2] ) + 1 or 0

    for it in range( iters ):

        if not noProgress:
            if ((50/iters) > ((it*100/iters)%10) ) or ( ((it*100/iters)%10) > 10 - (50/iters)): # MAGIC
                print("|", sep='', end="", flush=True ) # print progress in console

        newLine = "{0}: line {1:04d}: {2}".format( time.strftime("%H:%M:%S_%d.%m.%y"), it, gen.generateMessage( it ) )

        logFile.write( newLine + '\n' )
        refFile.write( newLine + '\n' )
        logFile.flush()

        if logFile.tell() > sizeThreshold: # if more, gzip old and truncate new
            logFile.close()
            gzipFileName = "{0}.{1:04d}.gz".format( filePath, gzipFileNameCounter )
            with open( filePath, "rb" ) as inFile:
                if noArchive:
                    with open( gzipFileName, "wb" ) as gzFile:
                        shutil.copyfileobj( inFile, gzFile )
                else:
                    with gzip.open( gzipFileName, "wb" ) as gzFile:
                        shutil.copyfileobj( inFile, gzFile )
            gzipFileNameCounter += 1
            logFile = open( filePath, "w" )

        elif not noSleep:
            time.sleep( sleepSSec )

    logFile.close()
    refFile.close()
    print( '' )

if __name__ == "__main__" :
    main( sys.argv )

# class CmdLineOption:
#     def __init__(self, name, defVal ):
#         self.name = name
#         self.defVal = defVal
#         self.cmdLineArgLong = "--arg1"
#         self.cmdLineArgShort = "-a1"

