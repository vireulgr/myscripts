#
# import multiprocessing
from multiprocessing import Pool, current_process
import cmdArgs
import os   
import sys

myConfig = cmdArgs.Config()

myConfig.addParam( "sleep",          "s", "0", "Tenths of seconds to wait before adding new portion of lines to logs" )
myConfig.addParam( "out-dir",        "o", "D:\\test\\logs", "Directory where logs storage files resides" ) 
myConfig.addParam( "size-threshold", "t", "20480",          "Size threshold when log must be archived" ) 
myConfig.addParam( "total-size",     "T", "51200",          "Total size to generate" ) 
myConfig.addParam( "noarchive",      "A", False,            "Do we need to really compress log files?" )
myConfig.addParam( "noprogress",     "P", False,            "Show progress?" )


def initFunc( argOne ):
    #argOne.printConfig()
    print( "init; PID: {0} PPID: {2}: {1}".format( str( os.getpid( ) ), str( argOne ), os.getppid() ) )

def mpJob( config, argTwo ):
    workerId = current_process().ident
    print( "=Job; PID: {0} {1} PPID: {2}: arg Two: {3}".format( str( os.getpid() ), workerId, os.getppid(), str( argTwo ) ) )
    config.printConfig()


if __name__ == "__main__":
    if myConfig.parseCmdLine( sys.argv ) != 0:
        myConfig.printUsage()
        exit()

    procPool = Pool( 3, initFunc, ( "hello", ) )
    #procPool.apply( mpJob, ("APPLY for job func", "arg two", ) )
    #procPool.map( mpJob, [ ("job on 1st", "arg 2 on 1st" ) , ("job on 2nd", "arg 2 on 2nd" ) , ( "job on 3rd", "arg 2 on 3rd" ) ] )
    procPool.starmap( mpJob, [ ( myConfig, "arg 2 on 1st" ) , ( myConfig, "arg 2 on 2nd" ) , ( myConfig, "arg 2 on 3rd" ) ] )
    procPool.close()
    procPool.join()

