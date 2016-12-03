#!usr/bin/env python
from sys import hexversion
if hexversion < 0x03000000:
    # if python version less than 3.0
    from Tkinter import *
    from tkFileDialog import askopenfilename
else:
    from tkinter import *
    from tkinter.filedialog import askopenfilename
    
from os import startfile
import matplotlib.pyplot as plt
import struct
import array
from subprocess import call
from os.path import split


filename = "d:\\kink"

fig = plt.figure( 1 )
ax = fig.add_subplot( 111 )

i = int( 1 )
#for i in range( 3, 20, 2 ):

filePath =  filename+str(i) 
datFile = open( filePath + ".bin", mode="rb" )
print( filePath )
absciss = array.array( "f" )
ordinate = array.array( "f" )
#pi_absc = array.array( "f" )
#pi_ord  = array.array( "f" )

datSize, = unpack( "i", datFile.read( 4 ) )
print( datSize )

print( datFile.read(1) )

flei = open( filename )
lines = flei.readlines()

for line in lines:
    first, sep, second = line.rpartition("  ")
    axis.append( float(first) )
    ordinate.append( float(second) )
flei.close()

absciss.fromfile( datFile, datSize )
ordinate.fromfile( datFile, datSize )

#pi_absc = array.array( "f", ordinate )

#for i in range( len( ordinate ) ) :
    #pi_ord.append( pi )
    
datFile.close()

ax.grid( True )
ax.set_xlim(0, 90*10*0.01 )
ax.set_ylim( -1, 10 )
ax.set_xlabel( "Contact" )
ax.set_ylabel( "Voltage" )
ax.set_title( "Soliton" )

ax.plot( ordinate, absciss )
#ax.plot( pi_absc, pi_ord, "r-" )
fig.savefig( filePath + ".png" )
ax.clear()
#fig.clf( keep_observers=True )
#plt.show()
#plt.close()
