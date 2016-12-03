# лаба по численным методам?
import math
a, b, c, d = 0.0, 1.0, 0.0, 2.0 
m, n = 4, 4

hx = ( b-a )/n
hy = ( d-c )/m


def func( x, y ):
	temp = math.sin( math.pi*x*y)
	return math.exp( temp*temp )

def rhs( x, y ) :
	temp = 2.0*math.pi*x*y
	temp2 = math.sin( temp )
	res = math.pi*math.pi*(temp2*temp2+2.0*math.cos(temp))*(x*x+y*y)*func(x,y)
	return res

print( "values for rhs" )
for j in range( m, -1, -1 ):
    for i in range( n+1 ):
        if i%(n+1) == 0: print( )
        print( '({0:.2f}, {1:.2f}) {2: >10.8g}\t'. format( i*hx, j*hy, rhs( i*hx, j*hy )), end="")
print( )
print( "values for func" )
for j in range( m, -1, -1 ):
    for i in range( n+1 ):
        if i%(n+1) == 0: print( )
        print( '({0:.2f}, {1:.2f}) {2: >10.8g}\t'. format( i*hx, j*hy, func( i*hx, j*hy )), end="")
print()
print( "{0:>30.10g} ".format( math.pi ), end="" )
print( "{0:=9.9f}".format( math.pi ) )
        

