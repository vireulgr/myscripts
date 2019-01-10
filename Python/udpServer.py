#
# UDP server
#

import socketserver
import sys

EULER_PORT = 27183
SYS_LOG_PORT = 514

logFileName = "D:\\pyServerLog.log"

class MyUDPHandler( socketserver.BaseRequestHandler ):
    def handle( self ):
        data = self.request[0].strip()
        socket = self.request[1]

        print( "{0} wrote:".format( self.client_address ) )
        print( data )

        log = open( logFileName, "a" )
        log.write( data.decode( "utf-8" ) )
        log.close()

        #if data == "exit":
        #    socket.sendto( bytes( "exiting", "utf-8" ), self.client_address )
        #else:
        #    socket.sendto( data.upper(), self.client_address )



def main( argv ):

    srAddr = ( "", SYS_LOG_PORT )

    print( "UDP socket listening started at {0}:{1}".format(srAddr[0],srAddr[1]))
    myServer = socketserver.UDPServer( srAddr, MyUDPHandler )
    myServer.serve_forever() 

if __name__ == "__main__":
    main( sys.argv )

