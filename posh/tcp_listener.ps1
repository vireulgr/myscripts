
function listen {
    $port = 23
    $endpoint = New-Object System.Net.IPEndPoint( [system.net.ipaddress]::Parse( "127.0.0.1"), $port )

    $listener = New-Object System.Net.Sockets.TcpListener $endpoint

    $listener.start()
    $client = $listener.acceptTcpClient()
    $stream = $client.GetStream()

    [byte[]]$bytes = 0..255 #| % {0}
    [int]$i = 0
    #while( 1 ) {
        while(( $i = $stream.Read( $bytes, 0, $bytes.length )) -ne 0 ) 
        {
            Write-host "length: $i"
            $bytes[$i] = 0
            $text = [System.Text.Encoding]::ASCII.GetString( $bytes, 0, $i  ) 
            Write-host "text is: " $text
            if( $text -match "exit" ) {break;}
        }
        
    #}

    $listener.stop()
}

listen
