A = [ [10.0,1.0],
      [1.0,5.0] ]

b = [ 31.0, 8.0 ] #, 6 ]

x0 = [ 1.0, 2.0 ] #, 0.0 ]

curSol = [0.0, 0.0 ] #, 0.0]
drcts = [0.0, 0.0] #, 0.0]
residual = [0.0, 0.0 ] #, 0.0]
betas = 0
alfas = 0

def AMul( vec ):
    global A
    result = list()
    for i in range( len(A)):
        result.append(0.0)
        for j in range( len(A[i])):
            result[i] += A[i][j]*vec[j]
    return result

def dotProduct( vec1, vec2 ):
    temp = float(0.0)
    for i, j in zip(vec1,vec2):
        temp += i*j
    return temp

def res( ):
    global residual
    global b
    temp = AMul( curSol )
    for i in range( len(curSol) ):
        residual[i] = temp[i] - b[i]
    
def beta():
    global residual
    global drcts
    temp1 = dotProduct( AMul( drcts ), residual )
    temp2 = dotProduct( AMul( drcts ), drcts )
    result = temp1/temp2
    return result

def alfa():
    global residual
    global drcts
    temp1 = dotProduct( residual, drcts )
    temp2 = dotProduct( AMul( drcts ), drcts )
    result = - temp1/temp2
    return result

def drct():
    global betas
    global residual
    global drcts
    for i in range( len(drcts) ):
        drcts[i] = betas*drcts[i] - residual[i]

def newSol( ):
    #global curSol
    global alfas
    global drcts
    temp = list()
    for i in range( len(curSol) ):
        temp.append(curSol[i] + drcts[i]*alfas )
    return temp

def IMLA( n ):
    global curSol
    global betas
    global drcts
    global residual
    global alfas
    res()
    drct()
    temp1 = float()
    temp1 = alfa()
    tempstr = str()
    tempstr = "drcts: " + str(drcts) + "\nalfas: " + str(temp1)
    print( tempstr )
    for i in range( len(curSol) ):
        curSol[i] = curSol[i] +temp1*drcts[i]
    for i in range( n-1 ):
        res()
        
        tempstr = "res:\t" + str(residual)
        print( tempstr) 
        betas = beta()
        if not betas :
        
            tempstr = "got exact solution on " + str( i+1 ) + " iteration"
            print( tempstr)
            break
        drct()
        alfas = alfa()
        tempstr = "\nbeta:\t" + str(betas) + "\ndrcts:\t" + str(drcts) + "\nalfas:\t" + str(alfas) + "\ncurSol\t:" + str( curSol)
        print( tempstr )        
        curSol = newSol()
        print( curSol )
    return curSol

def main():
    IMLA(6)

if __name__ == "__main__":
    main()

    
