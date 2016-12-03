# reads data from file in text mode and shows a plot
import matplotlib.pyplot as plt
import array as ar
#import numpy as np
from decimal import Decimal
from math import ceil, floor
from math import sqrt
#from math import sin

def init_arrays( filename, axis, ordinate ):
        
        flei = open( filename )

        #lines = flei.readlines()
        #print lines[3::10]
        #str.rpartition()
        for line in flei: #lines:
            print( line )
            first, sep, second = line.rpartition(";")
            #print( first, second )
            if first != '':
                axis.append( Decimal(first) )
                ordinate.append( Decimal(second) )

        flei.close()

axss1 = ar.array('f')

ords1 = ar.array('f')

dirname = "D:\\cp_data\\"

filename = dirname + "my.txt"
init_arrays( filename, axss1, ords1 )

rtax = [ i for i in range( floor(axss1[0]), ceil(axss1[len(axss1)-1]) ) ]
rtord = [ 0.0280*(ax **0.5) for ax in rtax ]

# plotting
fig = plt.figure(1)
ax = fig.add_subplot( 111 )
#ax.plot( axsbi, ordbi, 'k-', axss1, ords1, 'b-', axss2, ords2, 'g-',
         #axss3, ords3, 'r-', axss4, ords4, 'm-')
ax.plot( axss1, ords1, 'ro' ) 
ax.plot( rtax, rtord, 'b-' )
leg = ax.legend(( 'Results', '0.0313*sqrt(N)' ), 'best' )
ax.grid(True)
#ax.set_xlim(-1, 50 )
#ax.set_ylim(-0.05, 2.05 )
ax.set_xlabel("Number of contacts")
ax.set_ylabel("Sigma" )
ax.set_title("Sigma vs N")
plt.show()
print("plot 1 close ")
plt.close()
	
