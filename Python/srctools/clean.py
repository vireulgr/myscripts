# coding: cp1251
# clean

import fnmatch
import sys
import os

#rootDir = "D:\\VCS\\szvi\\experiments\\LogsPoller"
#rootDir = "D:\\prog\\thirdparty\\zlib-1.2.8"
#rootDir = "D:\\prog\\thirdparty\\googletest-master"
rootDir = "C:\\Users\\ggv\\Desktop\\LogsPoller"

extToDelete = (
                "*.tlog",
                "*.exe",
                "*.obj",
                "*.pdb",
                "*.ilk",
                "*.idb",
                "*.sdf",
                "*.db"
                )

def main( argv ):
    
    matches = []
    notDeleted = []

    for root, dirs, files in os.walk( rootDir ):
        for ext in extToDelete:
            for item in fnmatch.filter( files, ext ):
                matches.append( os.path.join( root, item ) )


    for item in matches[:] :
    # [:] is because cycle body modifies the sequence object
        if os.path.exists( item ):
            if os.path.isfile( item ):
                try:
                    os.remove( item )
                except OSError as ex:
                    notDeleted.append( item )
                    print( "item {0} is not a regular file! ".format(item) )
                finally:
                    matches.remove( item )
            
    for item in matches[:]:
    # [:] is because cycle body modifies the sequence object
        if os.path.exists( item ):
            if os.path.isdir( item ):
                try:
                    # directory will be removed only if it is empty
                    os.rmdir( item ) 
                except OSError as ex:
                    notDeleted.append( item )
                    print( "cannot remove directory " + item )
                finally:
                    matches.remove( item )

    print( "items that not deleted:\n{0}\nskipped:\n{1}\n".format( notDeleted, matches ) )
    input( )


if __name__ == "__main__":
    main( sys.argv )

