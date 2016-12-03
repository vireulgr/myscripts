from Tkinter import *
from os import startfile
import matplotlib.pyplot as plt
import struct
import array
from subprocess import call

class LaunchPanel:
    def __init__( self, myParent = None ):
        self.parent = myParent

        self.btn_wd = 15

        self.container = Frame( self.parent )
        self.container.pack()
        frame = Frame( root )
        frame.pack( ipadx = "1m", ipady = "1m" )
        
        self.btn_sineBias = Button( frame, text="Sine Bias", width = self.btn_wd, command=self.sineBias )
        self.btn_sineBias.grid( row=1, column=0 )

        self.btn_sineLaunch = Button( frame, text="Launch", width = self.btn_wd, command=self.sineLaunch )
        self.btn_sineLaunch.grid( row=2, column=0 )
        
        self.btn_jjSystem = Button( frame, text="System of JJs", width = self.btn_wd, command=self.JJsystem )
        self.btn_jjSystem.grid( row=1, column=1 )

        self.btn_jjsLaunch = Button( frame, text="Launch", width = self.btn_wd, command= self.jjsLaunch )
        self.btn_jjsLaunch.grid( row=2, column=1 )
        
        self.btn_sbSettings = Button( frame, text="Settings", width = self.btn_wd, command=self.sineBiasSettings )
        self.btn_sbSettings.grid( row=3, column=0)
        
        self.btn_jjsSettings = Button( frame, text="Settings", width = self.btn_wd, command=self.JJsystemSettings )
        self.btn_jjsSettings.grid( row=3, column=1)
        
        self.lbl = Label( frame, text="just click on the button" )
        self.lbl.grid(row=0, column=0,columnspan=2 ) 
        
    def sineBias( self ):
        print( "sineBIas has started" )
        #===============
        flei = open( "E:\Source code\sb_py_out.bin", "rb" )
        # initializing array size
        size, = struct.unpack( 'i', flei.read(4) )
        
        flei.read(1) # skip newline escape character
        
        # initializing function values
        time = array.array('d')
        time.fromfile( flei, size )
        euler = array.array('d')
        euler.fromfile( flei, size )
        hune = array.array('d')
        hune.fromfile( flei, size )
        flei.close()

        # plotting
        fig = plt.figure(1)
        ax = fig.add_subplot( 111 )
        ax.plot( time, euler, 'r-', time, hune, 'g-' )
        leg = ax.legend(( '1st', '2nd' ), 'best' )
        ax.grid(True)
        ax.set_xlabel("time")
        ax.set_ylabel("phase" )
        ax.set_title("Plot")
        plt.show()
        print("plot 1 close ")
        plt.close()
        #================
##        plt.figure( 1 )
##        xax = [1,2,3]
##        ax1 = plt.subplot(121)
##        plt.plot( xax, [1,2,3], "g^" )
##        ax2 = plt.subplot( 122, sharex = ax1 )
##        plt.plot( xax, [3,2,1], "ro" )
##        plt.show()

    def JJsystem( self ):
        print( "josephson junctions system simulation has started" )
        #========================
        flei = open( "E:\Source code\C++\Tasks\jjs_py_out.bin", "rb" )
        # initializing array size
        size, = struct.unpack( 'i', flei.read(4) )
        
        flei.read(1) # skip newline escape character
        
        # initializing function values
        time = array.array('d')
        time.fromfile( flei, size )
        euler = array.array('d')
        euler.fromfile( flei, size )
        hune = array.array('d')
        hune.fromfile( flei, size )
        phase3 = array.array('d')
        phase3.fromfile( flei, size )
        
        flei.close()

        # plotting
        fig = plt.figure(2)
        ax = fig.add_subplot( 111 )
        ax.plot( time, euler, 'r-', time, hune, 'g-', time, phase3, 'b-' )
        leg = ax.legend(( '1st', '2nd', '3rd' ), 'best' )
        ax.grid(True)
        ax.set_xlabel("time")
        ax.set_ylabel("phase" )
        ax.set_title("Plot")
        plt.show()
        print("plot 2 close")
        plt.close()
        #===================
##        plt.figure( 2 )
##        xax = [1,2,3]
##        ax1 = plt.subplot(211)
##        plt.plot( xax, [1,2,3], "g^" )
##        ax2 = plt.subplot( 212, sharex = ax1 )
##        plt.plot( xax, [3,2,1], "ro" )
##        plt.show()

    def jjsLaunch( self ):
        call( ['E:\\Source code\\C++\\Tasks\\Release\\DifEq.exe'] )

    def sineLaunch( self ):
        call( ['E:\\Source code\\C++\\Tasks\\Release\\sine bias.exe'] )
         
    def sineBiasSettings( self ):
        print( "start sinebias settings file" )
        startfile( "e:\source code\SineBias.txt" )

    def JJsystemSettings(self ):
        print( "start jjsystem settings file" )
        startfile( "e:\source code\JJsystem.txt" )
    

root = Tk()
root.resizable( False, False )
root.title( "JJs" )
myapp = LaunchPanel(root)

root.mainloop()





