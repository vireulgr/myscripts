
#$hostname = "w7dlss"

$af = [System.Net.Sockets.AddressFamily]::InterNetwork
$st = [System.Net.Sockets.SocketType]::Stream
$pt = [System.Net.Sockets.ProtocolType]::Tcp 

$sock = New-Object System.Net.Sockets.Socket( $af, $st, $pt )

#$ipAddress1 = [System.Net.Dns]::Resolve( $hostname );
$ipAddress2 = [System.Net.IPAddress]::Parse( "192.168.13.207" );

$ipEndpoint = New-Object System.Net.IPEndPoint( $ipAddress2, 6500 );

$sock.Bind( $ipEndpoint );

$sock.Listen( 10 );

while( $true ) {

    $mode = [System.Net.Sockets.SelectMode]::SelectRead `
            -bor [System.Net.Sockets.SelectMode]::SelectError `
            -bor [System.Net.Sockets.SelectMode]::SelectWrite

    $res = $sock.Poll( 500, $mode )
    if( $res ) {
        if( -not $sock.Connected ) {
            $sock.Shutdown( [system.net.sockets.socketshutdown]::Both );
        }
        else {
            $clientSock = $sock.Accept( );
            [byte[]]$buffer = @(255,255,225,255)
            $sock.send( $buffer );
        }
    }
}



