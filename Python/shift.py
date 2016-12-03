#!/usr/bin/python
#
#

import sys
import matplotlib.pyplot as plt
import numpy as np

N = 1024 
begi = 0
alpha = 0.25*np.pi
endi = 1

def main( argv ):
    print( "in main" )
    # create data
############################
    # all array variables are numpy arrays so all operations 
    # (like minus, times, plus, applying math functions etc.) are vectorized automatically
    absc = np.linspace( begi, endi, N )

    # INSERT YOUR FUNCTIONS HERE!!!!!
###################
    fdata = np.reciprocal( np.cosh( absc - 2 ) )
    imgDataF = np.fft.fft( fdata ) / N 
    #freq = np.linspace( -N//2, N-1//2, N )
    freq = np.linspace( 0, N-1, N )
    print( freq )
    imgDataF = imgDataF*np.exp( -(0+1.j)*alpha*freq )
    #print( imgDataF )
    origData = np.fft.ifft( imgDataF ) * N
#    gdata = np.reciprocal( np.sqrt( np.sin(absc ) ) )
###################

    # compute convolution using FFT
############################
# preparing data
#    origDataF = np.zeros( 2*N )
#    origDataG = np.zeros( 2*N )
#    origDataF[0:N] = fdata
#    #origDataG[0:N] = gdata
#    origDataG = origDataG[::-1]
# computing images
    #imgDataF = np.fft.fft( origDataF ) / N 
    #imgDataG = np.fft.fft( origDataG ) / N 
# computing product and reverse transform
    #imgConv = np.multiply( np.conj(imgDataF), imgDataG )
    #origData = np.fft.ifft( imgConv ) * N

    # compute convolution directly
############################
#    directConv = np.zeros( 2*N, dtype='float' )
#    it = np.nditer( directConv, flags=['f_index'], op_flags=['writeonly'] )
#    it.iternext()
#    while not it.finished:
#        if it.index < N:
#            #it[0] = np.sum( gdata[0:it.index] * fdata[it.index-1::-1]) / N
#        elif it.index == N: 
#            #print( "index, N ", int(it.index ), N )
#            #it[0] = np.sum( gdata[:] * fdata[::-1]) / N
#        else:
#            #print( "index, N ", int(it.index ), N )
#            #it[0] = np.sum( gdata[it.index-N:N] * fdata[N:it.index-N-1:-1]) / N
#        it.iternext()
#
    # compute convolution using numpy function
############################
    #convData = np.convolve( gdata, fdata ) / N

    #print( "orig data len", len(origData) )
    #print( "imgConv len", len(imgConv) )
    #print( "imgData len", len(imgDataF) )
    #print( "convData len", len(convData) )
    #print( "directConv len", len(directConv) )

    # plotting
############################
    fig = plt.figure( 1 )
    ax = fig.add_subplot( 121 )
    ax.set_title("functions")
    #ax.plot( absc, fdata, 'r--' )
    #ax.plot( np.linspace( begi, endi*2, 2*N ), origDataF, 'g-' )
    #ax.plot( np.linspace( begi, endi*2, 2*N ), origDataG, 'b--' )
    ax.plot( absc, fdata, 'b-' )
    #ax.set_xlim( -0.2, 3.4 )
    #ax.set_ylim( -1, 34 )
    ax.grid(True)

    dx = fig.add_subplot( 122 )
    dx.set_title("convolution")
    #dx.plot( np.linspace( begi, endi*2, 2*N-1 ), convData, 'g--' ) 
    #dx.plot( np.linspace( begi, endi*2, 2*N ), directConv, 'r:' ) 
    #dx.plot( np.linspace( begi, endi*2, 2*N ), origData, 'r-' ) 
    dx.plot( absc, origData, 'r-' ) 
    #dx.set_xlim( -0.1, 3.4 )
    #dx.set_ylim( -0.1, 2.4 )
    dx.grid(True)

    plt.show()
    plt.close()

if __name__ == '__main__':
    main(sys.argv[1:])
#
#
