# coding: cp1251

import sys
import time
import cmdArgs
from os import path
from spamGen import SpamGenerator
from logFile import LogFileTrunc, LogFileRename
from multiprocessing import Pool

# =======================
# CONFIGURATION
# =======================
fileNamesList = (
    "logFirst", "logSecond",
    "AlgTwo_0", "AlgTwo_1",
    "fileWithDataOne", "fileWithDataTwo")

myConfig = cmdArgs.Config()

myConfig.addParam( cmdArgs.FloatArg( "sleep", "s", "0.0", 
                    "Tenths of seconds to wait before adding new portion of lines to logs" ) )
myConfig.addParam( cmdArgs.StrListArg("out-dir",    "o", 
                    "D:\\test\\logs", "Directory where logs storage files resides" ) )
myConfig.addParam( cmdArgs.IntArg("size-threshold", "t", 
                    "20480",          "Size threshold when log must be archived" ) )
myConfig.addParam( cmdArgs.IntArg("total-size",     "T",
                    "51200",          "Total size to generate" ) )
myConfig.addParam( cmdArgs.BoolArg("noarchive",     "A",
                    False,            "Do we need to really compress log files?" ) )

# =============================
# FUNCTIONS
# =============================
def processLogFileObject( logFileObj, deciSec ):
    
    #print( "processLogFileObject", logFileObj.getFilePath() )
    #sleep( random.randrange( 1, 5 )*0.1 )
    gen = SpamGenerator()
    ite = 0
    # setup sleep
    noSleep = int( deciSec ) <= 0
    sleepSSec = int(deciSec) * 0.1
    progr = logFileObj.getProgress()

    while progr < 1.0:
        newLine = ""
        for daVariableInDaHouse in range( 3 ):
            newLine += "{0}: line {1:04d}: {2}\n".format(
                                               time.strftime("%H:%M:%S_%d.%m.%y"),
                                               ite, gen.generateMessage() )
            ite +=1


        logFileObj.addContent( newLine )

        if not noSleep:
            time.sleep( sleepSSec )


        progr = logFileObj.getProgress()


    #print("|", sep='', flush=True ) # print progress in console

# =======================
# MAIN
# =======================
def main( argv ) :

    if myConfig.parseCmdLine( argv ) != 0:
        myConfig.printUsage()
        return 0

    outDirs         = myConfig.getParamVal( "out-dir" )
    deciSec         = int( myConfig.getParamVal( "sleep" ) )
    noArchive       = bool( myConfig.getParamVal( "noarchive" ) )
    sizeThreshold   = int( myConfig.getParamVal( "size-threshold" ) )
    totalBytesOnLog = int( myConfig.getParamVal( "total-size" ) )

    for item in outDirs[:]:
        if not path.exists( item ):
            print( "ERROR: Directory doesn't exist {0}".format( item ) )
            outDirs.remove( item ) 

    if not outDirs:
        print( "ERROR: Directory list is empty" )
        return 0

    # print( outDirs )
    # logsList = [ LogFile( outDirs, name, 1024, 1050, noArchive ) for name in fileNamesList ]
    idx = 0
    logsList = [ LogFileTrunc( outDirs[idx % len(outDirs)], fileNamesList[idx],
                                sizeThreshold, totalBytesOnLog, noArchive ) ]
    idx+=1
    logsList.append( LogFileTrunc( outDirs[idx % len(outDirs)], fileNamesList[idx],
                                    sizeThreshold, totalBytesOnLog, noArchive ) )
    idx+=1
    logsList.append( LogFileRename( outDirs[idx % len(outDirs)], fileNamesList[idx], 
                                    sizeThreshold, totalBytesOnLog, noArchive ) )
    idx+=1
    logsList.append( LogFileRename( outDirs[idx % len(outDirs)], fileNamesList[idx], 
                                    sizeThreshold, totalBytesOnLog, noArchive ) )

    argsList = [ (ent, deciSec ) for ent in logsList ]

    workerPool = Pool( len( logsList ) )
    workerPool.starmap( processLogFileObject, argsList )

if __name__ == "__main__" :
    main( sys.argv )

