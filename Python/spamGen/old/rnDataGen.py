# random data generator
import sys
import random
import base64
from spamGen import SpamGenerator
from logFile import LogFile

fileNamesList = (
    "logFileAlgOne0",
    "logFileAlgOne1",
    "AlgTwo1LogFile",
    "AlgTwo2LogFile",
    "fileWithDataOne",
    "fileWithDataTwo"
    )

def isAllComplete( logsList ):
    res = True
    for log in logsList:
        res = res and log.isComplete()
    return res
    

def main( argv ):

    logsList = [ LogFile( name ) for name in fileNamesList ]

    print( logsList )

    gen = SpamGenerator()

    while not isAllComplete( logsList ):
        for log in logsList:
            log.addContent( gen.generateMessage(random.randrange(7)) )

if __name__ == "__main__":
    main( sys.argv )

