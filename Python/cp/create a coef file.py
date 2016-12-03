# -*- coding: cp1251 -*-
from sys import hexversion
if hexversion < 0x03000000:
    # if python version less than 3.0
    from Tkinter import *
    from tkFileDialog import askopenfilename
else:
    from tkinter import *
    from tkinter.filedialog import askopenfilename
    
from os import startfile
import struct
import array
from subprocess import call
from os.path import split

class LaunchPanel:
    def __init__( self, myParent = None ):
        self.parent = myParent

        self.btn_wd = 7

        self.container = Frame( self.parent )
        self.container.pack()
        
        frame = Frame( root )
        frame.pack( ipadx = "1m", ipady = "1m" )

        self.lbl = Label( frame, text="just click on the button", wraplength = 390 )
        self.lbl.grid(row=0, column=0, columnspan=7 ) 

        ## view button
        self.btn_sineBias = Button( frame, text="View", command=self.btn_view ) #, width = self.btn_wd
        self.btn_sineBias.grid( row=1, column=0, columnspan=2 )

        ## Entries
        self.e_data = Entry( frame, width = 50 )
        self.e_data.grid( row = 1, column = 2, columnspan=4 )
        self.e_data.insert( END, "d:\\cfs.bin" )
        
        ## browse button
        self.btn_browse1 = Button( frame, text="...", command=self.browse1 )
        self.btn_browse1.grid( row=1, column=6 )

        ## Quantity
        self.lbl1 = Label( frame, text="Quantity" )
        self.lbl1.grid( row=2, column=0, sticky=E )

        self.lbl2 = Label( frame, text="Value" )
        self.lbl2.grid( row=2, column=3, sticky=E )
        
        ## Value
        self.e_qty = Entry( frame )
        self.e_qty.grid( row=2, column=1, columnspan=2, sticky=W)
        self.e_qty.insert( END, "20" )
        
        self.e_val = Entry( frame )
        self.e_val.grid( row=2, column=4, columnspan=2, sticky=W )
        self.e_val.insert( END, "0.1" )

        ## save button
        self.btn_save = Button( frame, text="Write", command= self.btn_save )
        self.btn_save.grid( row=2, column=6 )
        
        ## label for bin file review
        self.l_res = Label( frame, text="<<blank>>", wraplength = 390)
        self.l_res.grid(row=3, column=0,columnspan=7 ) 

    ## ==========
    ## methods
    ## ==========
    def btn_view( self ):

        filename = self.e_data.get()
        flei = open( filename, "rb" )

        size = int(self.e_qty.get())
        qty, = struct.unpack( "i", flei.read(4) )

        hintString = ""
        if size != qty:
            hintString = "Size is choosen by file data"
            #self.lbl['text'] = "Size is choosen by file data"
            self.e_qty.delete( 0, END )
            self.e_qty.insert( END, str(qty) )

        if qty > 1000:
            hintString = "File is too big!\nOnly frist 1000 elements will be displayed."
            qty = 1000
            
        flei.readline()
        time = array.array('d')
        size = qty
        
        try:
            time.fromfile( flei, size )
        except EOFError:
            hintString  = "You've just exceed a bound of the file.\nSo you need to specify lesser number in Quantity field"
            #self.lbl['text'] = "You've just exceed a bound of the file.\nSo you need to specify lesser number in Quantity field"
        else:
            expDrawString = ""
            for i in time:
                expDrawString += str(i)
                expDrawString += "\t "
        
            self.l_res['text'] = expDrawString #time.tostring()            
        finally:
            flei.close()
            if hintString == "":
                hintString = "Ready"

            self.lbl['text'] = hintString
            #self.lbl['text'] = "Ready"

    def btn_save( self ):
        filename = self.e_data.get()
        flei = open( filename, "wb" )
        val = float( self.e_val.get() )
        qty = int(self.e_qty.get())
        init = [ val for i in range( qty ) ]
        data = array.array( "d", init )
        #================================
        flei.write( struct.pack( "i", qty ) )
        flei.write( b"\n"  )
        #================================
        data.tofile( flei )
        ##print data
        flei.close( )
        pass
    
    def browse1( self ):
        pathname = self.e_data.get()
        pathname = split(pathname)
        #self.lbl['text'] = pathname[0]
        result = askopenfilename( defaultextension='.txt', parent=self.container,
                         filetypes=[("Binary file", ".bin")], initialdir=pathname[0] )
        if not (result == ""):
            self.lbl['text']=result
            self.e_data.delete( 0, END )
            self.e_data.insert( END, result )
        
root = Tk()
root.resizable( False, True )
root.title( "Wasya" )
myapp = LaunchPanel(root)

root.mainloop()
