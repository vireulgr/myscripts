
. .\deploy.ps1

#[string[]]$Hostnames = @('w7dlss','w8dlss','w7dlls')
[string[]]$Hostnames = @(,'w7dlls')

[string[]]$Data = @('Event1','Exit')

# Create UDP socket
# [system.net.sockets.ProtocolFamily]::InterNetwork
#$socket = New-Object System.Net.Sockets.Socket ([system.net.sockets.AddressFamily]::InterNetwork), `
#                                      ([system.net.sockets.SocketType]::Dgram), `
#                                      ([system.net.sockets.ProtocolType]::Udp)

# UDP client
$UdpClient = $null;
$UdpClient = New-Object system.net.sockets.udpclient $port
if( $UdpClient -eq $null ) {
  write-host "error creating udpclient"
  return;
}

foreach( $Node in $Hostnames ) {
  # send data to host
  write-host "seinding to $Node"
  # Create Endpoint
  $IpEndpoint = CreateEndpoint $Node $port
  if( $ipendpoint -eq $null ) {
    write-host "can't create endpoint for $Node"
    continue;
  }

  foreach( $DataItem in $Data ) {
    write-host "seinding $dataItem"
    # send data item
    # Serialize data
    $bytes = [system.text.encoding]::Unicode.GetBytes( $DataItem );

    # Socket sendto
    #$socket.SendTo( $bytes, $IpEndpoint );
    $UdpClient.send( $bytes, $bytes.length, $IpEndpoint );
    start-sleep 2
  }
}
$UdpClient.close();
# $socket.Shutdown( [System.Net.Sockets.Socketshutdown]::Both );
# $socket.Close();
# $socket = $null;

