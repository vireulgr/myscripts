
param( [string] $IP = "127.0.0.1", [int] $port = 23, [string[]] $commands )
#param( [string] $remoteHost = "localhost", [int] $port = 23, [string[]] $commands )

try { ## Open the socket, and connect to the computer on the specified port
	write-host "Connecting to $remoteHost on port $port"

  # ==================================================
  $address = [system.net.IPAddress]::Parse($IP) 

  # Create IP Endpoint 
  $End = New-Object System.Net.IPEndPoint $address, $port 

  # Create Socket 
  $Saddrf = [System.Net.Sockets.AddressFamily]::InterNetwork 
  $Stype = [System.Net.Sockets.SocketType]::Stream 
  $Ptype = [System.Net.Sockets.ProtocolType]::TCP
  $Sock = New-Object System.Net.Sockets.Socket $saddrf, $stype, $ptype 
  $Sock.TTL = 26 
  
  # Connect to socket 
  $sock.Connect($end)
  
	#$socket = new-object System.Net.Sockets.TcpClient($remoteHost, $port)

	#if($socket -eq $null) {
	#	throw ("Could Not Connect")
	#}
	#$stream = $socket.GetStream() 
    #$writer = new-object System.IO.StreamWriter($stream)

	$buffer = new-object System.Byte[] 1024
	$encoding = new-object System.Text.AsciiEncoding

        # Send the byte array 
        $Sent = $Sock.Send($Message)
        "{0} characters sent to: {1} " -f $Sent,$IP
        "Message is: $Message" 
        
    #$buffer = @( 0xff, 0xfb, 0x1f, 0xff, 0xfb, 0x20, 0xff, 0xfb, 0x18, 0xff, 0xfb, 0x27, 0xff, 0xfd, 0x01, 0xff, 0xfb, 0x03, 0xff, 0xfd, 0x03) 
    #$buffer | % { $writer.Write( $_ ) } 
    #$writer.Write( "\xff\xfb\x1f\xff\xfb\x20\xff\xfb\x18\xff\xfb\x27\xff\xfd\x01\xff\xfb\x03\xff\xfd\x03" )
    #$writer.Flush()

    #$buffer = @( 0xff, 0xfc, 0x23 )
    #$buffer | % { $writer.Write( $_ ) } 
    #$writer.Flush()
    #start-sleep 2

    #$writer.WriteLine("exit")
    ##$writer.Flush()
    start-sleep 2

    #$buffer = @( 0xFF, 0xFC, 0x24 ) 
    #$buffer | % { $writer.Write( $_ ) } 
    #$writer.Flush()

    #$buffer = @( 0xff, 0xfa, 0x1f, 0x00, 0x50, 0x00, 0x18, 0xff, 0xf0 )
    #$buffer | % { $writer.Write( $_ ) } 
    #$writer.Flush()
}
catch {

	#When an exception is thrown catch it and output the error.
	#this is also where you would send an email or perform the code you want when its classed as down.

	write-host $error[0]

	$dateTime = get-date

	$errorOccurence = "Error occurred connecting to $remoteHost on $port at $dateTime"

	write-host $errorOccurence
}

finally {
	## Close the streams
	## Cleans everything up.
    Write-host "Finally"
	#$writer.Close()
	#$stream.Close()

}
