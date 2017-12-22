#
import shutil
import gzip
import re
from pathlib import Path

# DEBUG ====================================
#import os

# ======================================
class LogFile:

    def __init__( self, dirName, fileName, threshold, maxBytes, noArchive ):
        self.dirName       = dirName 
        self.fileName      = fileName
        self.sizeThreshold = threshold
        self.maxBytes      = maxBytes
        self.noArchive     = noArchive

        self.bytesWritten  = 0
        self.nameCounter = 0

        self.initNamesCounters()
    
    def initNamesCounters( self ):
        self.filePath = "{0}\\{1}.log".format( self.dirName, self.fileName )
        # search for files by mask and if exists, continue counter
        # \warning template for globbing must be compatible with one 
        # that is used for gzipFileName file name creation! see below
        gzipFiles = [ x.name for x in list( Path( self.dirName ).glob( "{0}*.gz".format( self.fileName ) ) ) ]
        # gzipFiles.sort() not needed
        # print( gzipFiles[-1] )
        self.nameCounter = len(gzipFiles) != 0 and int( re.split("[_.]", gzipFiles[-1])[-3] ) + 1 or 0
        
    def onFileOverflow( self ):
        gzipFileName = "{0}.{1:04d}.gz".format( self.filePath, self.nameCounter )
        with open( self.filePath, "rb" ) as inFile:
            if self.noArchive:
                with open( gzipFileName, "wb" ) as gzFile:
                    shutil.copyfileobj( inFile, gzFile )
            else:
                with gzip.open( gzipFileName, "wb" ) as gzFile:
                    shutil.copyfileobj( inFile, gzFile )
            
        self.nameCounter += 1
        logFile = open( self.filePath, "w" )
        logFile.close()

    def addContent( self, content ):
        if( self.bytesWritten > self.maxBytes ):
            return
        
        # DEBUG ========================
        #if not os.access( self.filePath, os.W_OK ):
        #    print( "file cannot be opened! " )
        #    return

        logFile = open( self.filePath, "a" )
        logFile.write( content )
        logFile.flush()

        filePos = logFile.tell()
        logFile.close()
        self.bytesWritten += len( content )

        # DEBUG ===================
        # print( "{0: >20s}: {1: <5d}".format( self.fileName, self.bytesWritten ) )

        if filePos > self.sizeThreshold: # if more, gzip old and truncate new
            self.onFileOverflow( )

    def getProgress( self ):
        return self.bytesWritten / self.maxBytes

    def getFilePath( self ):
        return self.filePath
    

# =============================================
class LogFileRename( LogFile ):
    def __init__( self, dirName, fileName, threshold, maxBytes, noArchive ):
        LogFile.__init__( self, dirName, fileName, threshold, maxBytes, noArchive )

    def initNamesCounters( self ):
        # search for files by mask and if exists, continue counter
        # \warning template for globbing must be compatible with one 
        # that is used for gzipFileName file name creation! see below
        gzipFiles = [ x.name for x in list( Path( self.dirName ).glob( "{0}*.log.gz".format( self.fileName ) ) ) ]
        # gzipFiles.sort() not needed
        self.nameCounter = len(gzipFiles) != 0 and int( re.split("[_.]", gzipFiles[-1])[-3] ) + 1 or 0

        self.filePath = "{0}\\{1}_{2:04d}.log".format( self.dirName, self.fileName, self.nameCounter )
        
        # DEBUG ===================
        # print( "Rename: filePath: {0}; nameCounter: {1}".format( self.filePath, self.nameCounter ) )

    def onFileOverflow( self ):
        gzipFileName = "{0}.gz".format( self.filePath )
        # DEBUG ===================
        # print( "Rename: gz file name: " + gzipFileName )
        with open( self.filePath, "rb" ) as inFile:
            if self.noArchive:
                with open( gzipFileName, "wb" ) as gzFile:
                    shutil.copyfileobj( inFile, gzFile )
            else:
                with gzip.open( gzipFileName, "wb" ) as gzFile:
                    shutil.copyfileobj( inFile, gzFile )
        oldFileName = self.filePath 
        self.nameCounter += 1
        self.filePath = "{0}\\{1}_{2:04d}.log".format( self.dirName, self.fileName, self.nameCounter )

        shutil.move( oldFileName, self.filePath )
            
        logFile = open( self.filePath, "w" )
        logFile.close()

# =============================================
class LogFileTrunc( LogFile ):
    def __init__( self, dirName, fileName, threshold, maxBytes, noArchive ):
        LogFile.__init__( self, dirName, fileName, threshold, maxBytes, noArchive )

    def initNamesCounters( self ):
        self.filePath = "{0}\\{1}.log".format( self.dirName, self.fileName )
        # search for files by mask and if exists, continue counter
        # \warning template for globbing must be compatible with one 
        # that is used for gzipFileName file name creation! see below
        gzipFiles = [ x.name for x in list( Path( self.dirName ).glob( "{0}.log.*.gz".format( self.fileName ) ) ) ]
        # gzipFiles.sort() not needed
        self.nameCounter = len(gzipFiles) != 0 and int( re.split("[_.]", gzipFiles[-1])[-2] ) + 1 or 0

        # DEBUG ===================
        #print( "Trunc: filePath: {0}; nameCounter: {1}".format( self.filePath, self.nameCounter ) )

    def onFileOverflow( self ):
        gzipFileName = "{0}.{1:04d}.gz".format( self.filePath, self.nameCounter )
        with open( self.filePath, "rb" ) as inFile:
            if self.noArchive:
                with open( gzipFileName, "wb" ) as gzFile:
                    shutil.copyfileobj( inFile, gzFile )
            else:
                with gzip.open( gzipFileName, "wb" ) as gzFile:
                    shutil.copyfileobj( inFile, gzFile )
            
        self.nameCounter += 1
        logFile = open( self.filePath, "w" )
        logFile.close()

