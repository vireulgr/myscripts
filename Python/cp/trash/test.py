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

        self.btn_sineLaunch = Button( frame, text="Compute", width = self.btn_wd, command=self.sineLaunch )
        self.btn_sineLaunch.grid( row=2, column=0 )
        
        self.btn_sbSettings = Button( frame, text="Settings", width = self.btn_wd, command=self.sineBiasSettings )
        self.btn_sbSettings.grid( row=3, column=0)

        ## Entries
        self.e_data = Entry( frame, width = 40 )
        self.e_data.grid( row = 1, column = 1 )
        self.e_data.insert( END, "D:\\Source\\cpp\\tasks\\release\\cjjs_py_out.bin" )
        
        self.e_exec = Entry( frame, width = 40 )
        self.e_exec.grid( row = 2, column = 1 )
        self.e_exec.insert( END, 'D:\\Source\\cpp\\tasks\\release\\chain jjs.exe' )
        
        self.e_sets = Entry( frame, width = 40 )
        self.e_sets.grid( row = 3, column = 1 )
        self.e_sets.insert( END, 'D:\\source\\cpp\\tasks\\cjjs.txt' )

        ## browse buttons
        self.btn_browse1 = Button( frame, text="...", command=self.browse1 )
        self.btn_browse1.grid( row=1, column=2 )

        self.btn_browse2 = Button( frame, text="...", command=self.browse2 )
        self.btn_browse2.grid( row=2, column=2 )
        
        self.btn_browse3 = Button( frame, text="...", command=self.browse3 )
        self.btn_browse3.grid( row=3, column=2)

    ## ==========    
    ## methods
    ## ==========
    def sineBias( self ):
        print( "Plotting..." )
        #===============
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

        # plotting
        fig = plt.figure(1)
        ax = fig.add_subplot( 111 )
        ax.plot( time, euler, 'ro')
        leg = ax.legend(( '1st', '2nd' ), 'best' )
        ax.grid(True)
        #ax.set_xlim(-1, 50 )
        #ax.set_ylim(-1, 10 )
        ax.set_xlabel("U")
        ax.set_ylabel("I" )
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
        flei = open( "D:\\Source\\cpp\\tasks\\release\\cjjs_py_out_fidot.bin", "rb" )
        # initializing array size
        size, = struct.unpack( 'i', flei.read(4) )
        
        flei.read(1) # skip newline escape character
        
        # initializing function values
        time = array.array('d')
        time.fromfile( flei, size )
        euler = array.array('d')
        euler.fromfile( flei, size )
        #hune = array.array('d')
        #hune.fromfile( flei, size )
        #phase3 = array.array('d')
        #phase3.fromfile( flei, size )
        
        flei.close()

        # plotting
        fig = plt.figure(2)
        ax = fig.add_subplot( 111 )
        ax.plot( time, euler, 'r-')#, time, hune, 'g-', time, phase3, 'b-' )
        #leg = ax.legend(( '1st', '2nd', '3rd' ), 'best' )
        ax.grid(True)
        ax.set_xlabel("time")
        ax.set_xlim(-1, 20 )
        #ax.set_ylabel("phase" )
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

   
    def sineLaunch( self ):
        filename = self.e_exec.get();
        self.lbl['text'] = 'Now computing...'
        call( [filename] )
        self.lbl['text'] = 'Done'
  
    def jjsLaunch( self ):
        call( ['D:\\source\\cpp\\tasks\\release\\Chain jjs.exe'] )
         
    def sineBiasSettings( self ):
        print( "Settings file has been opened" )
        filename = self.e_sets.get()
        startfile( filename )

    def JJsystemSettings(self ):
        print( "start jjsystem settings file" )
        startfile( "e:\source code\JJsystem.txt" )

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
        result = askopenfilename( defaultextension='.exe', parent=self.container,
                         filetypes=[("Executable", ".exe")], initialdir=pathname[0] )
        if not (result == ""):
            #result.replace( "/", "\\" )
            self.lbl['text']=result
            self.e_exec.delete( 0, END )
            self.e_exec.insert( END, result )
        
    def browse3( self ):
        pathname = self.e_sets.get()
        pathname = split(pathname)
        #self.lbl['text'] = pathname[0]
        result = askopenfilename( defaultextension='.txt', parent=self.container,
                         filetypes=[("Text file", ".txt")], initialdir=pathname[0] )
        if not (result == ""):
            self.lbl['text']=result
            self.e_sets.delete( 0, END )
            self.e_sets.insert( END, result )
        
root = Tk()
root.resizable( False, False )
root.title( "Josephson juncitons" )
myapp = LaunchPanel(root)

root.mainloop()





