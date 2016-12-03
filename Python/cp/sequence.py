#!/usr/bin/python
import sys
import subprocess

from time import sleep
from decimal import Decimal
from math import ceil, floor
from os import system

import matplotlib.pyplot as plt
import array as ar

# ============================
# Parse results file and fill arrays for plot
# ============================
def initFromJTLRslt( filename, contacts, sigma, mean ):
    # example line from results file
    #conts:           30	 mean:    19.001277	 sigma:   0.10085366
    flei = open( filename )
    for line in flei:
        tokens = line.split()
        if tokens != []:
            contacts.append( Decimal(tokens[1]) )
            mean.append( Decimal(tokens[3]) )
            sigma.append( Decimal(tokens[5]) )
        
    flei.close()

# ===========================
# Writing params back to file
# ===========================
def writeParamsFile( params, fileName ):
    """
    Converts parameters list of tuples (name, value) to single
    multiline string and writes this string to parameters file
    in correct order. 
    """

    toWriteStr = ""
    strNames = ""
    strVals = ""

    #print( "Params are {par}\n".format( par=params) )

    for item in params: # merging array of names and values into one string to write to parameters file
        if (item[0] == "coef") or (item[0] == "mu"): # mu and coef parameters must start a new line in parameters file
            strNames += '\n'
            strVals += '\n'
            toWriteStr += strNames + strVals
            strNames = ""
            strVals = ""

        if item[0] ==  '' or item[1] == '': continue
        strNames += "{:>10s}; ".format( item[0] )
        strVals += "{:>10s}; ".format( item[1] )

    strNames.rsplit( ";" )
    strNames.rsplit( ";" )
    toWriteStr += strNames + '\n' + strVals + '\n'

    paramsFile = open( fileName, 'w+t' )
    paramsFile.write( toWriteStr )
    paramsFile.close()

def main( argv ):
    #print( "in main\nargv is %(argv)s" % {'argv':argv} );

    dirname = "./"

    frm = 20
    to = 60
    step = 10

    execute = False

    if len(argv) < 2:
        execute = True
    else:
        if argv[1].strip() == "--no-compute" or argv[1].strip() == "-N":
            execute = False
        else:
            execute = True

    if execute: 
# ============================
# Reading params from file
# ============================

        paramsFname = dirname + "params.txt"
        fil = open( paramsFname, 'r+t' )

        strList = []
        for line in fil:
            strList.append( line.replace("\t", "") )

        #fil.seek( 0 )

        keys = []
        vals = []
        keys.extend( strList[0].split(";") )
        vals.extend( strList[1].split(";") )
        keys.extend( strList[2].split(";") )
        vals.extend( strList[3].split(";") )
        keys.extend( strList[4].split(";") )
        vals.extend( strList[5].split(";") )

        keys = [ tk.strip() for tk in keys ]
        vals = [ tk.strip() for tk in vals ]

        #print( "{:>7.4g}".format( 3.141592 ) )

        paramArr = []
        for key, val in zip( keys, vals ):
            paramArr.append( list([key.strip(" \n"), val.strip(" \n")]) )

        print( keys )

        varsInd = keys.index("vars")
# =======================
# Run simulation
# =======================
        #print( "Starting JTL simulation\nNum of contacts from " 
        #        "{a_frm} to {a_to} with step {a_step}"
        #        .format( a_frm=frm, a_to=to, a_step=step 
        #        ) )
        for numOfVars in range( frm, to + 1, step ):
            paramArr[varsInd][1] = str(numOfVars)
            writeParamsFile( paramArr, paramsFname )
            # -l - with logging; 
            # -f - parameters file will be `paramsFname`; 
            # -s - OpenCL C source will be /trunk/ocl_c_src.cl
            subprocess.call(['trunk\\prog.exe', '-l', '-f', paramsFname, '-s', 'trunk\\ocl_c_src.cl'])
            sleep( 1 ) # halt for 1 second to give system time to free resources on graphic card

        #print( "End of cycle" )

# =========================
# Parse results
# =========================

    filename = "../JTL.log"

    contacts = ar.array('f')
    sigma = ar.array('f')
    mean = ar.array('f')

    initFromJTLRslt( filename, contacts, sigma, mean )

    rtabs = [ i for i in range( int(floor(contacts[0])), int(ceil(contacts[len(contacts)-1]) )) ]
    rtord = [ 0.136*(ax **0.5) - 0.5 for ax in rtabs ]

    #print( contacts, sigma, mean, sep='\n' )
# =======================
# Plotting
# =======================
    fig = plt.figure(1)
    ax = fig.add_subplot( 111 )
    ax.plot( contacts, sigma, 'ro' ) 
    #ax.plot( contacts, mean, 'g-' ) 
    ax.plot( rtabs, rtord, 'b-' )
    #leg = ax.legend(( 'Sigma', 'Mean', '0.0313*sqrt(N)' ), 'best' )
    leg = ax.legend(( r'$\sigma$', r'$0.136\sqrt{N}-0.5$' ), 'best' )
    numTicks = 50
    tickMin = int(floor(min(sigma)))*10
    tickMax = int(ceil(max(sigma)))*10
    tickStep = int( ceil((tickMax - tickMin) / (numTicks-1)) )
    ax.xaxis.set_ticks( [i for i in range( int(floor(contacts[0])), int(ceil(contacts[len(contacts)-1]) + 1 ), step ) ] )
    ax.yaxis.set_ticks( [i*0.1 for i in range( tickMin, tickMax, tickStep) ] ) 
    ax.grid(True)
    #ax.set_xlim(-1, 50 )
    #ax.set_ylim(-0.05, 2.05 )
    ax.set_xlabel("Number of contacts")
    #ax.set_ylabel("Sigma" )
    ax.set_title("Results")
    plt.show()
    #print("plot 1 close ")
    plt.close()

if __name__ == "__main__":
    main( sys.argv ) 

