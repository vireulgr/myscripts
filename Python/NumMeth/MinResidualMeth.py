A = [ [6,1,1],
      [1,8,1],
      [1,1,4] ]

b = [ 8, 10, 6 ]

x0 = [ 1.0, 0.0, 0.0 ]

curSol = [1.0, 0.0, 0.0]

def AMul( vec ):
    result = [0.0, 0.0, 0.0]
    for i in range(3):
        for j in range(3):
            result[i] += A[i][j]*vec[j]
            #print( i, j, result[i] )
    return result

def dotProduct( vec1, vec2 ):
    return vec1[0]*vec2[0]+vec1[1]*vec2[1]+vec1[2]*vec2[2]

def res( ):
    global curSol
    temp = AMul( curSol )
    for i in range(3):
        temp[i] = temp[i] - b[i]
    return temp
    
def tau( ):
    result = 0.0
    temp1 = res()
    temp2 = AMul(temp1)
    result = dotProduct( temp1, temp2 ) / dotProduct( temp2, temp2 )
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
        curSol = newSol(n)
    return curSol

print( IMLA( 1 ) )
#print( AMul( res() ) )
#print( AMul( curSol ) )
#print( res() )
#temp1 = res()
#temp2 = AMul( temp1 )
#print( dotProduct( temp1, temp2 ) )
#print( dotProduct( temp2, temp2 ) )
#print( tau() )
