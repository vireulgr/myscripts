from math import cos, pi

A = [ [12,2,1],
      [2,8,1],
      [1,1,4] ]

b = [ 15, 11, 6 ]

x0 = [ 0.0, 0.0, 0.0 ]

curSol = [0.0, 0.0, 0.0]

k=4

lmb1 = 2
lmbN = 15

def AMul( vec ):
    result = [0.0, 0.0, 0.0]
    for i in range(3):
        for j in range(3):
            result[i] += A[i][j]*vec[j]
            #print( i, j, result[i] )
    return result

def dotProduct( vec1, vec2 ):
    temp = 0.0
    for i in range( vec.size() ):
        temp+=vec1[i]*vec2[i]
    return temp

def res( ):
    global curSol
    temp = AMul( curSol )
    for i in range(3):
        temp[i] = temp[i] - b[i]
    return temp
    
def tau():
    result = 2.0/(lmb1+lmbN)
    return result
                
def newSol( n ):
    global curSol
    if n == 0:
        return x0
    else:
        vec = [0.0,0.0,0.0]
        temp = res()
        temp2 = tau()
        for i in range(3):
            vec[i] = curSol[i] - temp[i]*temp2
        return vec

def IMLA( n ):
    global curSol
    for i in range( n ):
        curSol = newSol(i)
        print( curSol )
    return curSol

#def __main__() :
IMLA(16)
    #print( AMul( res() ) )
#print( AMul( curSol ) )
#print( res() )
#temp1 = res()
#temp2 = AMul( temp1 )
#print( dotProduct( temp1, temp2 ) )
#print( dotProduct( temp2, temp2 ) )
#print( tau(1) )
