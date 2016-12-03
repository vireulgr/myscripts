#A = [ [12,2,1],
#      [2,8,1],
#      [1,1,4] ]
A = [ [ 6, 2] ,
      [ 2, 8] ]
#b = [ 15, 11, 6 ]
b = [ 30, 54 ]

#x0 = [ 0.0, 0.0, 0.0 ]
x0 = [ 0.0, 0.0 ]

#curSol = [0.0, 0.0, 0.0]
curSol = [ 0.0, 0.0 ]

lmb1 = 4
lmbN = 10

def AMul( vec ):
    result = list() #[0.0, 0.0, 0.0]
    for i in range(len(A)):
        result.append(0.0)
        for j in range(len(curSol)):
            result[i] += A[i][j]*vec[j]
    return result

def dotProduct( vec1, vec2 ):
    temp = 0.0
    for i in range( vec.size() ):
        temp+=vec1[i]*vec2[i]
    return temp

def res( ):
    global curSol
    temp = AMul( curSol )
    for i in range(len(curSol)):
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
        vec = list() #[0.0,0.0,0.0]
        temp = res()
        temp2 = tau()
        line = str( )
        line = "res:\t" + str(temp) + "\ntau:\t" + str(temp2)
        print( line )
        for cs, tmp in zip( curSol, temp ):
            vec.append( cs - tmp*temp2 )
        return vec

def IMLA( n ):
    global curSol
    for i in range( n ):
        curSol = newSol(i)
        print( curSol )
    return curSol

def main():
    IMLA(16)

if  __name__ == "__main__":
    main()
