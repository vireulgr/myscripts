import matplotlib.pyplot as plt
import array as ar
#import numpy as np

def init_arrays( filename, axis, ordinate ):
        
        flei = open( filename )

        lines = flei.readlines()
        #print lines[3::10]
        #str.rpartition()
        for line in lines:
        	first, sep, second = line.rpartition("  ")
        	axis.append( float(first) )
        	ordinate.append( float(second) )
        flei.close()

axss1 = ar.array('f')

ords1 = ar.array('f')

dirname = "D:\\cp_data\\"

filename = dirname + "cpu.dat"
init_arrays( filename, axss4, ords4 )

# plotting
fig = plt.figure(1)
ax = fig.add_subplot( 111 )
#ax.plot( axsbi, ordbi, 'k-', axss1, ords1, 'b-', axss2, ords2, 'g-',
         #axss3, ords3, 'r-', axss4, ords4, 'm-')
ax.plot( axss1, ords1, 'r-' ) 
#leg = ax.legend(( '1st', '2nd' ), 'best' )
ax.grid(True)
#ax.set_xlim(-1, 50 )
#ax.set_ylim(-0.05, 2.05 )
ax.set_xlabel("x")
ax.set_ylabel("y" )
ax.set_title("Plot")
plt.show()
print("plot 1 close ")
plt.close()
	
