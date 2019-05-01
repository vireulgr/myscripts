import re
import os

# ******************************************************************************************
# 
# ******************************************************************************************
def recurseDirs( rootDir, extToDelete ):
    matches = []
    for root, dirs, files in os.walk( rootDir ):
        for ext in extToDelete:
            for item in fnmatch.filter( files, ext ):
                matches.append( os.path.join( root, item ) )
    return matches

# test ==============================
def TEST_recurseDirs() :
    rootDir = "Z:\\VI\\VSphere\\SoapProxyLib"
    extToDelete = (".obj", ".lib", ".ipdb", ".iobj" )
    matches = []

    matches = myutil.recurseDirs( rootDir, extToDelete )
    print( matches )


# ******************************************************************************************
# 
# ******************************************************************************************

def myPyGrep( regExp, fileName ):
    with open( fileName ) as origin_file:
        #for line in origin_file:
        for num, curLine in enumerate( origin_file ):
            line = re.findall( regExp, curLine )
            #if line:
            #   line = line[0].split('"')[1]
            if line:
                print( fileStr + ":" + str( num ) )
                print( curLine )

# test ==============================
def TEST_myPyGrep():
    fileStr = "spamGen.py"
    findStr = "смятенье"
    matches = []
    matches = myPyGrep( fileStr, findStr )
    print( matches )

#################################################################################
#
#################################################################################
def swapDirs( rootDir, dirFrom, dirTo ):
    tempSuffix = "_tmp"
    os.rename( os.path.join( rootDir, dirTo ), os.path.join( rootDir, dirTo + tempSuffix  ) )
    os.rename( os.path.join( rootDir, dirFrom ), os.path.join( rootDir, dirTo ) )
    os.rename( os.path.join( rootDir, dirTo + tempSuffix ), os.path.join( rootDir, dirFrom ) )

# test
def TEST_swapDirs():
    dirNameFrom = "temp_old"
    dirNameTo   = "temp_new"
    dirRoot     = "D:\\"

    swapDirs( dirRoot, dirNameFrom, dirNameTo )
