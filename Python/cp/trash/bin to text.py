from Tkinter import *
import array
import struct
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
        self.btn_sineBias = Button( frame, text="Convert", width = self.btn_wd, command=self.sineBias )
        self.btn_sineBias.grid( row=1, column=0 )    

        ## Entries
        self.e_data = Entry( frame, width = 40 )
        self.e_data.grid( row = 1, column = 1 )
        self.e_data.insert( END, "e:\\Source code\\c++\\tasks\\chain jjs\\cjjs_py_out.bin" )

        ## browse buttons
        self.btn_browse1 = Button( frame, text="...", command=self.browse1 )
        self.btn_browse1.grid( row=1, column=2 )

    def sineBias( self ):
        #===============
        filename = self.e_data.get()
        flei = open( filename, "rb" )
        # initializing array size
        size, = struct.unpack( 'i', flei.read(4) )
        
        flei.read(1) # skip newline escape character
        
        # reading binary data
        time = array.array('d')
        time.fromfile( flei, size )
        euler = array.array('d')
        euler.fromfile( flei, size )
        flei.close()

        filename = filename[:-3] + "dat"
        flei = open( filename, "w" )
        
        for i in xrange( len(time) ):
            data = "\t" + str(time[i]) + "    \t" + str(euler[i]) + "\n"
            flei.write( data )

        flei.close()
        
        self.lbl['text']="Done. Filename: "+filename

    def browse1( self ):
        pathname = self.e_data.get()
        pathname = split(pathname)
        result = askopenfilename( defaultextension='.txt', parent=self.container,
                         filetypes=[("Binary file", ".bin")], initialdir=pathname[0] )
        if not (result == ""):
            self.lbl['text']=result
            self.e_data.delete( 0, END )
            self.e_data.insert( END, result )
        
root = Tk()
root.resizable( False, False )
root.title( "Binary to text" )
myapp = LaunchPanel(root)

root.mainloop()





