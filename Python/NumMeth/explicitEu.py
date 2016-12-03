x0=10
u1_0 = 1
u2_0 = 2
step = 0.1

def rhs1( x, u1, u2 ):
    return -x+u1*u1+u2

def rhs2( x, u1, u2 ):
    return u1

def eulerMeth( x0, u1_0, u2_0, h ):
    u1 = 0.0
    u2 = 0.0
    print( rhs1( x0, u1_0, u2_0 ) )
    print( rhs2( x0, u1_0, u2_0 ) )
    u1 = u1_0 + h*rhs1( x0, u1_0, u2_0 );
    u2 = u2_0 + h*rhs2( x0, u1_0, u2_0 );
    return u1, u2

def eulerIts( n ):
    x = x0
    u1 = u1_0
    u2 = u2_0
    h = step
    print( x, u1, u2, h )
    for i in range(n) :
        u1, u2 = eulerMeth( x, u1, u2, h )
        x = x0+h*i
        print( x, u1, u2 )

def main():
    eulerIts( 3 )

if __name__ == "__main__":
    main()  
    
