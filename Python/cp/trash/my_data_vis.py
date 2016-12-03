import matplotlib.pyplot as plt
import array as ar
import struct

def init_arrays( filename, axis, ordinate ):
        
    flei = open( filename, "rb" )

    size, = struct.unpack( 'i', flei.read(4) )
    #print size
    flei.read(1) # skip newline escape character
    
    # initializing function values

    axis.fromfile( flei, size )
    ordinate.fromfile( flei, size )
        
    flei.close()

axss1 = ar.array('d')
axss4 = ar.array('d')
axss3 = ar.array('d')
axss2 = ar.array('d')
axss5 = ar.array('d')
axsbi = ar.array('d')

ords1 = ar.array('d')
ords4 = ar.array('d')
ords3 = ar.array('d')
ords2 = ar.array('d')
ords5 = ar.array('d')
ordbi = ar.array('d')

dirname = "D:\\cp_data\\"

filename = dirname + "correct_one.bin"
init_arrays( filename, axsbi, ordbi )
filename = dirname + "0-1285_branch.bin"
init_arrays( filename, axss1, ords1 )
filename = dirname + "0-24_branch.bin"
init_arrays( filename, axss2, ords2 )
filename = dirname + "0-42_branch.bin"
init_arrays( filename, axss3, ords3 )
filename = dirname + "0-458_branch.bin"
init_arrays( filename, axss4, ords4 )
filename = dirname + "0-7_branch.bin"
init_arrays( filename, axss5, ords5 )
##for i in range( 10 ):
##    print axsbi[i], ordbi[i]

# plotting
fig = plt.figure(1)
ax = fig.add_subplot( 111 )
ax.plot( axsbi, ordbi, 'k-' , axss1, ords1, 'b-', axss2, ords2, 'g-',
       axss3, ords3, 'ro', axss4, ords4, 'mv', axss5, ords5, 'c^' )
#leg = ax.legend(( '1st', '2nd' ), 'best' )
ax.grid(True)
ax.set_xlim(-0.05, 1.4 )
ax.set_ylim(-0.05, 1.4 )
ax.set_xlabel("x")
ax.set_ylabel("y" )
ax.set_title("Plot")
plt.show()
print("plot 1 close ")
plt.close()
