#
# All options, passed to addParam method MUST have all parameters (incl. short option, default value and description)
#


class CmdLineArg:
    def __init__( self, optLong, optShort, defVal, dscr ):
        self.optLong    = optLong
        self.optShort   = optShort
        #self.value      = defVal
        self.description = dscr


    # this method must be reload in every child class
    def match( self, strVal ):
        if "=" in strVal:
            if strVal.startswith( "--" + self.optLong ) or strVal.startswith( "-" + self.optShort ):
                a, b, value = strVal.partition( '=' )
                # DEBUG ====================
                #print( "        " + value )
                self.value = value
                return True
        else:
            if strVal == ("--" + self.optLong) or strVal == ('-' + self.optShort):
                # DEBUG ====================
                #print( strVal + " matches " + self.optLong + " or " + self.optShort )
                self.value = True                        
                return True

        return False


class FloatArg( CmdLineArg ):
    def __init__( self, optLong, optShort, defVal, dscr ):
        CmdLineArg.__init__(  self, optLong, optShort, defVal, dscr )
        self.value = float(defVal)


    def match( self, strVal ):
        if "=" in strVal:
            if strVal.startswith( "--" + self.optLong ) or strVal.startswith( "-" + self.optShort ):
                a, b, value = strVal.partition( '=' )
                # DEBUG ====================
                #print( "        " + value )
                self.value = float(value)
                return True
        else:
            return False


class IntArg( CmdLineArg ):
    def __init__( self, optLong, optShort, defVal, dscr ):
        CmdLineArg.__init__(  self, optLong, optShort, defVal, dscr )
        self.value = int(defVal)


    def match( self, strVal ):
        if "=" in strVal:
            if strVal.startswith( "--" + self.optLong ) or strVal.startswith( "-" + self.optShort ):
                a, b, value = strVal.partition( '=' )
                # DEBUG ====================
                #print( "        " + value )
                self.value = int(value)
                return True
        else:
            return False


class StringArg( CmdLineArg ):
    def __init__( self, optLong, optShort, defVal, dscr ):
        CmdLineArg.__init__(  self, optLong, optShort, defVal, dscr )
        self.value = defVal


    def match( self, strVal ):
        if "=" in strVal and ( strVal.startswith( "--" + self.optLong ) 
                                or strVal.startswith( "-" + self.optShort ) ):
            a, b, value = strVal.partition( '=' )
            # DEBUG ====================
            #print( "        " + value )
            self.value = value
            return True

        return False


class BoolArg( CmdLineArg ):
    def __init__( self, optLong, optShort, defVal, dscr ):
        CmdLineArg.__init__(  self, optLong, optShort, defVal, dscr )
        self.value = False


    def match( self, strVal ):
        if strVal == ("--" + self.optLong) or strVal == ('-' + self.optShort):
            # DEBUG ====================
            #print( strVal + " matches " + self.optLong + " or " + self.optShort )
            self.value = True                        
            return True



class StrListArg( CmdLineArg ):
    def __init__( self, optLong, optShort, defVal, dscr ):
        CmdLineArg.__init__(  self, optLong, optShort, defVal, dscr )
        self.value = []
        self.value.append( defVal )
        self.isDefault = True


    def match( self, strVal ):
        if "=" in strVal and ( strVal.startswith( "--" + self.optLong ) 
                                or strVal.startswith( "-" + self.optShort ) ):
            if self.isDefault:
                self.value.clear()
                self.isDefault = False

            a, b, value = strVal.partition( '=' )
            # DEBUG ====================
            #print( "        " + value )
            self.value.append( value )
            return True

        return False



class Config:
    def __init__( self ):
        self.params = []
        self.binName = "" 

    def getParamVal( self, longName ):
        for param in self.params:
            if param.optLong == longName:
                return param.value
        return None


    def addParam( self, lng, shrt, defVal, descr ):
        tmp = CmdLineArg( lng, shrt, defVal, descr )
        self.params.append( tmp )


    def addParam( self, cmdArgParam ):
        self.params.append( cmdArgParam )


    def parseCmdLine( self, argv ):
        #argsLeft = len(argv) -1 # one for script name
        self.binName = argv[0]
        cmdLine = argv[1:]
        for arg in cmdLine:
            processed = False
            # DEBUG ====================
            #print( arg ) 
            for param in self.params:
                # DEBUG ====================
                #print( "    " + param.optLong )
                if param.match( arg ):
                    processed = True
                    break;

            if not processed: 
                print( "Argument not matched! (" + arg + ")" )
                return -1

        return 0

    def printUsage( self ):
        print( "Usage: {0} <args>; <args> can be:".format( self.binName ) ) 
        for param in self.params:
            print( "--{0:<20} -{1:<5} {2}\n".format( param.optLong, param.optShort, param.description ) )

    def printConfig( self ):
        for param in self.params:
            print( "{0:>20}: {1}".format( param.optLong, param.value ) )

