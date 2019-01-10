#
# UDP client
#

import socket
import sys
from time import sleep

SYS_LOG_PORT = 514
#HOSTNAME = "win8go.land.esxi"
HOSTNAME = "localhost"

def main( argv ):
    #HOST, PORT = "localhost", 27183

    # message = "This is the message. It will be echoed from the server."
    messages = ( "<166>2017-01-30T09:09:43.450Z esxi808go.confi.ru Vpxa: [FFC72B70 info 'commonvpxLro' opID=HB-host-123@88-545e21b6-bb] [VpxLRO] -- FINISH task-internal-35 --  -- vmodl.query.PropertyCollector.Filter.destroy --" 
    , "<86>2017-01-30T09:09:48Z esxi808go.confi.ru DCUI: pam_per_user: create_subrequest_handle(): doing map lookup for user \"root\"" 
    , "<86>2017-01-30T09:09:48Z esxi808go.confi.ru DCUI: pam_per_user: create_subrequest_handle(): creating new subrequest (user=\"root\", service=\"system-auth-generic\")" 
    , "<32>2017-01-30T09:09:48Z esxi808go.confi.ru DCUI: Authentication of user root succeeded" 
    , "<14>2017-01-30T09:09:48Z esxi808go.confi.ru DCUI: User root logged in" 
    , "<86>2017-01-30T09:09:48Z esxi808go.confi.ru DCUI: pam_per_user: create_subrequest_handle(): doing map lookup for user \"root\"" 
    , "<86>2017-01-30T09:09:48Z esxi808go.confi.ru DCUI: pam_per_user: create_subrequest_handle(): creating new subrequest (user=\"root\", service=\"system-auth-generic\")" 
    , "<85>2017-01-30T09:09:48Z esxi808go.confi.ru DCUI: pam_unix(system-auth-generic:auth): authentication failure; logname= uid=0 euid=0 tty= ruser= rhost=  user=root" 
    , "<12>2017-01-30T09:09:49Z esxi808go.confi.ru nssquery: Group lookup failed for 'DL\ESX Admins'"  )


    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

    # server_address = ( "localhost", 27183 )
    server_address = ( HOSTNAME, SYS_LOG_PORT )

    for msg in messages:
        try:  
            sent = sock.sendto( bytes( msg, "utf-8" ), server_address )
            sleep( 0.5 )
        except: 
            sock.close()
            break

    if sock.isOpen():
        sock.close()

    # try:
    #     print( "Sending: {0}". format( message ) )
    #     sent = sock.sendto( bytes( message, "utf-8" ), server_address )

    #     print( "Waiting to receive" )
    #     received, server = sock.recvfrom( 4096 )
    #     #received = str( sock.recv(1024), "utf-8" )
    #     print( "from {1} received: {0}".format( received, server ) )

    #     message = "exit"
    #     print( "Sending: {0}". format( message ) )
    #     sent = sock.sendto( bytes( message, "utf-8" ), server_address )

    #     print( "Waiting to receive" )
    #     received, server = sock.recvfrom( 4096 )
    #     #received = str( sock.recv(1024), "utf-8" )
    #     print( "from {1} received: {0}".format( received, server ) )

    # finally:
    #     print( "closing socket" )
    #     sock.close()


if __name__ == "__main__":
    main( sys.argv )
