# -*- coding: utf-8 -*-
from math import cos, pi

A = [ [10,1],
      [1,5] ]

b = [ 31, 8 ]

x0 = [ 0.0, 0.0 ]

curSol = [0.0, 0.0]

k=3

lmb1 = 4
lmbN = 11

def AMul( vec ):
    result = list()
    for i in range(len(A)):
        result.append(0.0)
        for j in range(len(vec)):
            result[i] += A[i][j]*vec[j]
    return result

def dotProduct( vec1, vec2 ):
    temp = 0.0
    for r, l in zip(vec1, vec2):
        temp += r*l
    return temp

def res( ):
    global curSol
    temp = AMul( curSol )
    for i in range(len(curSol)):
        temp[i] = temp[i] - b[i]
    return temp
    
def tau(s):
    temp = (lmb1+lmbN)+(lmbN-lmb1)*cos(0.5*pi*(2*s+1)/k)
    return 2/temp
                
def newSol( n ):
    global curSol
    if n == 0:
        return x0
    else:
        vec = list()    
        temp = res()
        temp2 = tau(n-1)

        for cs, tmp in zip( curSol, temp ):
            vec.append( cs - tmp*temp2 )
        tempstr = str()
        tempstr ="iteration\t" + str(n) + "\nres:\t" + str(temp) + "\ntau\t" + str(temp2)+ \
                "\nsolution\t" +str(vec) 
        print( tempstr )
        return vec

def IMLA( n ):
    global curSol
    for i in range( 1, n ):
        curSol = newSol(i)
    return curSol

def main():
    IMLA(2*k+1)

    
if __name__ == "__main__":
    main()
