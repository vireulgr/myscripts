#!/usr/bin/python
# 
from Tkinter import *
from os import startfile
import matplotlib.pyplot as plt
import struct
import array
from subprocess import call
from tkFileDialog import askopenfilename
from os.path import split

class LaunchPanel:
    def __init__( self, myParent = None ):
        self.parent = myParent

        self.btn_wd = 15

        self.container = Frame( self.parent )
        self.container.pack()
        
        frame = Frame( root )
        frame.pack( ipadx = "1m", ipady = "1m" )

        self.lbl = Label( frame, text="just click on the button" )
        self.lbl.grid(row=0, column=0,columnspan=2 ) 

        ## buttons
        self.btn_sineBias = Button( frame, text="Plot", width = self.btn_wd, command=self.sineBias )
        self.btn_sineBias.grid( row=1, column=0 )    

        ## Entries
        self.e_data = Entry( frame, width = 40 )
        self.e_data.grid( row = 1, column = 1 )
        self.e_data.insert( END, "e:\\Source code\\c++\\tasks\\chain jjs\\cjjs_py_out.bin" )
        
        self.e_exec = Entry( frame, width = 40 )
        self.e_exec.grid( row = 2, column = 1 )
        self.e_exec.insert( END, 'D:\\cp_data\\Ua01N10L01.dat' )

        ## browse buttons
        self.btn_browse1 = Button( frame, text="...", command=self.browse1 )
        self.btn_browse1.grid( row=1, column=2 )

        self.btn_browse2 = Button( frame, text="...", command=self.browse2 )
        self.btn_browse2.grid( row=2, column=2 )
        

    ## ==========    
    ## methods
    ## ==========

    def init_arrays( self, filename, axis, ordinate ):
        
        flei = open( filename )
        lines = flei.readlines()
  
        for line in lines:
        	first, sep, second = line.rpartition("  ")
        	axis.append( float(first) )
        	ordinate.append( float(second) )
        flei.close()


    def sineBias( self ):
        
        filename = self.e_data.get()
        flei = open( filename, "rb" )
        # initializing array size
        size, = struct.unpack( 'i', flei.read(4) )
        
        flei.read(1) # skip newline escape character
        
        # initializing function values
        time = array.array('d')
        time.fromfile( flei, size )
        euler = array.array('d')
        euler.fromfile( flei, size )
        flei.close()

        ## to compare =====
        axsbi = array.array('f')
        ordbi = array.array('f')
        
        #dirname = "D:\\cp_data\\"
        #filename = dirname + "Ua01N10L01.dat"

        filename = self.e_exec.get()
        self.init_arrays( filename, axsbi, ordbi )

        # plotting
        fig = plt.figure(1)
        ax = fig.add_subplot( 111 )
        ax.plot( axsbi, ordbi, 'k-' )
        #ax.plot( axss1, ords1, 'b-', axss2, ords2, 'g-',
        #         axss3, ords3, 'r-', axss4, ords4, 'm-' )#, time, euler, 'r-', lw = 2)
        ax.plot( time, euler, 'y-', lw=2, alpha=0.6 )
        #leg = ax.legend(( '1st', '2nd' ), 'best' )
        ax.grid(True)
        ax.set_xlim(-0.05, 1.2 )
        ax.set_ylim(-0.05, 1.2 )
        ax.set_xlabel("U")
        ax.set_ylabel("I")
        ax.set_title("Plot")
        plt.show()
        print("plot 1 close ")
        plt.close()

    def browse1( self ):
        pathname = self.e_data.get()
        pathname = split(pathname)
        #self.lbl['text'] = pathname[0]
        result = askopenfilename( defaultextension='.bin', parent=self.container,
                         filetypes=[("Binary file", ".bin")], initialdir=pathname[0] )
        if not (result == ""):
            self.lbl['text']=result
            self.e_data.delete( 0, END )
            self.e_data.insert( END, result )

    def browse2( self ):
        pathname = self.e_exec.get()
        pathname = split(pathname)
        #self.lbl['text'] = pathname[0]
        result = askopenfilename( defaultextension='.dat', parent=self.container,
                         filetypes=[("Text data", ".dat")], initialdir=pathname[0] )
        if not (result == ""):
            #result.replace( "/", "\\" )
            self.lbl['text']=result
            self.e_exec.delete( 0, END )
            self.e_exec.insert( END, result )
        
root = Tk()
root.resizable( False, False )
root.title( "Compare plots" )
myapp = LaunchPanel(root)

root.mainloop()





