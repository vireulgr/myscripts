#!/usr/bin/python
#
#

import sys
import matplotlib.pyplot as plt
import numpy as np
import math as m

N = 1024*16
#begi = 0.001
begi = 0.0
endi = np.pi# * 0.5
length = endi - begi
step = 0.04

# подсчёт первых 10 членов ряда 
##############################
def objfun( x, t ):
    f = 0;
    for n in range( 1, 10 ): #=1:10
        if n == 2 or n == 4: continue
        nth = 2*( ( (-1)**(n+1) )/(n**3) ) * ( 1-m.cos(n*t) )*(m.sin(n*x));
        #print( nth )
        f += nth;

    #print( f )
    return f+x*t*t;


def main( argv ):
    print( "in main" )
    # create data
############################
    # all array variables are numpy arrays so all operations 
    # (like minus, times, plus, applying math functions etc.) are vectorized automatically

    absc = np.arange( begi, endi, step )

    t = 10
    cutoff = []
    for arg in absc:
        cutoff.append( objfun(arg, t) )
       
    #print( cutoff, absc )

    # plotting
############################
    fig = plt.figure( 1 )
    cutoffPlot = fig.add_subplot( 111 )
    cutoffPlot.plot( absc, cutoff )
    cutoffPlot.grid( True )
    cutoffPlot.set_title( "t = 1" )

    plt.show()
    plt.close()

if __name__ == '__main__':
    main(sys.argv[1:])
#
#
