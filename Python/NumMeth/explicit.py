
x0 = 1.0
u0 = 1.0
step = 0.01

def rhs( u, x ) :
    return u*u - 2*x*x

def methHewn( h, x0, u0 ):
    u1 = 0.0
    u1_ = 0.0
    u1_ = u0 + rhs( u0, x0 )*h
    u1 = u0 + 0.5*h*( rhs( u1_, x0+h ) + rhs( u0, x0 ) )
    return u1

def hewnIts( n ):
    x = x0
    u = u0
    h = step
    print( x, u, h)
    for i in range(n) :
        u = methHewn( h, x, u )
        x = x+h
        print( x, u )

def main() :
    hewnIts( 3 )    

if __name__ == "__main__" :
    main()
