# coding: cp1251
import subprocess
import datetime
from os import path


class WorkingCopy():
    def __init__( self, path ):
        self.path = path
        self.rev = 0

#workingDir = "Z:/"

WCs = (
    WorkingCopy( "Z:/VI" ),
    WorkingCopy( "Z:/DL80" ),
    WorkingCopy( "Z:/DLCommon" )
    )


# План Б - реверт к исходной ревизии и собрать проект
# TODO
def planB( workingCopy ):
    
    print( "plan b" )
    retcode = subprocess.call( ["svn", "update", workingCopy.path, "-r", workingCopy.rev, "--accept" ,"theirs-full" ] )

    buildWC( workingCopy )

# TODO
def buildWC( workingCopy ):
    print( "Don't know how to build (((" )
    return 0


for wc in WCs:
# сохранить патч текущей рабочей копии
    dateTimeStr = datetime.datetime.now().strftime("%d-%m-%y_%H-%M")
    workingCopyName = wc.path.split( "/" )[-1]
    workingDir = wc.path.split( '/' )[0]
    diffFileName = "{0}/{1}_{2}.diff".format( workingDir, workingCopyName, dateTimeStr ) 
    #ofl = open( diffFileName, "w+" )
    #if not path.exists( diffFileName ):
    opnStr = "w" if not path.exists( diffFileName ) else "a"
    #with open( diffFileName, "a" ) as ofl:
    print( opnStr , diffFileName )

    with open( diffFileName, opnStr ) as ofl:
        retCode = subprocess.call( ['svn','diff', wc.path ], stdout=ofl )
        if retCode != 0: # don't care
            print( "svn diff command finished with non-zero error code!" )
            pass
    #ofl.close()

# получить текущую ревизию (чтобы было ясно куда откатываться)
    outBytes = subprocess.check_output( ['svn','info', wc.path] )
    outStr = outBytes.decode( "cp1251" )
    revNumStr = outStr.split( "\n" )[10]
    revNum = int( revNumStr.split( ':' )[1] )
    wc.rev = revNum
    print( wc.path, wc.rev )

# обновиться до последней ревизии
    retCode = subprocess.call( [ "svn", "update", wc.path, "-r", "HEAD", "--accept", "theirs-full" ] )

    if retCode != 0:
# в случае ошибок слияния   - план Б
        print( "Update failed" )
        planB( wc )

# попытаться собрать с последней ревизией
    retCode = buildWC( wc )

    if retCode != 0:
# в случае ошибок сборки    - план Б
        print( "Build failed!" )
        planB( wc )
        
    pass # end of cycle over WCs

