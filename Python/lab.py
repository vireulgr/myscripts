# -*- coding: cp1251 -*-
# ������������ ������ �� ������� �����������
# ����� �������
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

points = []             #
funcVals = []           #
#a = 0                   # ������ ������� 
#b = 10                  # ����� �������
#L = 5                   # ��������� �������
epsilon = 10**-2        # ��������
Q = sp.Function('Q')    # ������� 
x = sp.Symbol('x')      # ��������
Qmin = 100501           # ���������� �������� �������
Rmin = 100500           # ���������� ��������������
a = float(raw_input( "Enter start point of the interval: " ))
b = float(raw_input( "Enter end point of the interval: " ))
#Q = sp.sympify( raw_input( "Input function: " ) )
Q = 1.5*sp.cos(2*x) + 0.15*(x-4)**2+5
print Q
# ������� ��� ��������� 
axis = np.arange( a, b, 0.1)
func = np.array([Q.subs(x,arg).evalf() for arg in axis ])

# ���������� ������� � ������� ���������
points.append(a)
points.append( a + (b-a)/4.)
points.append( a + (b-a)/2.)
points.append( a + (b-a)*3./4.)
points.append(b)

axisG = []
funcG = []

# ���������� ������� �������� �������
for arg in points:
    Qval = Q.subs(x, arg).evalf()
    if Qval < Qmin:
        Qmin = Qval
    funcVals.append( Qval )

# ���������� ��������� �������
for i in xrange( len(points) - 1):
    Lmax = 0
    dif = abs(funcVals[i] - funcVals[i+1])/abs(points[i] - points[i+1])
    if Lmax < dif:
        Lmax = dif

if Lmax != 0: L = Lmax * 10
else: L = 1

print "Lipschitz const:", L

# ���������� �������� ��� ��������� ���������
# ������� ����������� ��������������

#index = 0
for i in xrange( len(points) - 1 ):
    Rcur = (funcVals[i]+funcVals[i+1])*0.5 - L*0.5*(points[i+1]-points[i])
    funcG.append( funcVals[i])
    funcG.append( Rcur )
    Xnew = (points[i] + points[i+1])*0.5 - (funcVals[i+1]-funcVals[i])/(2.*L)
    axisG.append(points[i])
    axisG.append(Xnew)
    
    if Rcur < Rmin:
        #index = i
        Rmin = Rcur
        
axisG.append(points[i+1])
funcG.append(funcVals[i+1])

# print funcVals, len(axisG), len(funcG)

plt.ion()
lineQ, lineG = plt.plot(axisG, funcG, "r-", axis, func, "g-" )
#plt.savefig('lab.png', dpi=300 )

#plt.show()
# ==========================================
raw_input( "before while" )
# ==========================================
# WHILE
# ==========================================
while (Qmin - Rmin) > epsilon:
# TODO ?? ��������� ������ ��������� �������
# ���������� ��������� �������
#    for i in xrange( len(points) - 1):
#        Lmax = 0
#        dif = abs(funcVals[i] - funcVals[i+1])/abs(points[i] - points[i+1])
#        if Lmax < dif:
#            Lmax = dif
#
#    if (Lmax != 0) and (Lmax > L * 0.33): L = Lmax * 3
#    else: L = 1
# ==========================================

    # ��������� ��������������
    Rmin = 100500
    index = 0
    for i in range( len(points) - 1 ):
        Rcur = (funcVals[i]+funcVals[i+1])*0.5 - L*0.5*(points[i+1]-points[i])
        if (Rcur < Rmin) :
            index = i
            Rmin = Rcur
            
    #print Rmin
    
    # ����� ����� ���������
    Xnew = axisG[ (2*index)+1 ]
    #print Xnew
    #print axisG

    #print Rmin
    #print funcG
    
    # ���������� ��������� � ����� �����
    Qval = Q.subs(x, Xnew).evalf()
    
    if Qval < Qmin: Qmin = Qval
    
    # ������� ����� ����� ���������
    points.insert( index+1, Xnew )
    funcVals.insert(index+1, Qval)

    # TODO �������� ���������� �������� ��� ��������� ���������
    funcG[ 2*index+1 ] = Qval
    
    axisG.insert( (2*index)+2,
                  (points[index+1] + points[index+2])*0.5
                  - (funcVals[index+2]-funcVals[index+1])/(2*L) )
    axisG.insert( (2*index)+1,
                  (points[index] + points[index+1])*0.5
                  - (funcVals[index+1]-funcVals[index])/(2*L)     )
    
    funcG.insert( (2*index)+2,
                  (funcVals[index+1]+funcVals[index+2])*0.5
                  - L*0.5*(points[index+2]-points[index+1]) )
    funcG.insert( (2*index)+1,
                  (funcVals[index]+funcVals[index+1])*0.5
                  - L*0.5*(points[index+1]-points[index])     )

    #print "Xnew:", Xnew
    #print "axisG:", axisG[ 2*index : 2*index+5 ]
    #print "Rmin:" , Rmin
    #print "funcG:", funcG[ 2*index : 2* index+5]
    
    # TODO ���������� ���������
    lineG.set_xdata(axisG)
    lineG.set_ydata(funcG)
    lineQ.set_ydata(func)
    lineQ.set_xdata(axis)
    plt.draw()
    
    # �������� Rmin, Qmin
    #raw_input( "make step" )
    
print "Qmin:", Qmin, "Xnew:", Xnew
raw_input( "end of script\nPress Enter..." )
plt.ioff()
plt.close()
