
. .\deploy.ps1

[string]$hostname = 'localhost'

# Create Endpoint
$ipendpoint = CreateEndpoint $hostname $port

if( $ipendpoint -eq $null ) {
  write-host "can't create endpoint for $hostname"
  return;
}

# socket udp
#$socket = new-object System.Net.Sockets.Socket ([system.net.sockets.AddressFamily]::InterNetwork), `
#                                              ([system.net.sockets.SocketType]::Dgram), `
#                                              ([system.net.sockets.ProtocolType]::Udp)
#

# buffer
#$buffer = New-object Byte[] 1024

# UDP listener
$listener = $null;
$listener = New-Object system.net.sockets.udpclient $port
if( $listener -eq $null ) {
  write-host "error creating udpclient"
  return;
}

# socket listen
#$socket.Bind( $ipendpoint );

Write-Host "Starting server"
$work = $true
while( $work ) {
  # socket receive
  $remoteIPEP = new-object system.net.ipendpoint ([system.net.ipaddress]::any), 0
  #[int]$received = 0;
  try {
    #$received = $socket.ReceiveFrom( $buffer, [ref]$remoteIPEP );
    write-host "receiving"
    $buffer = $listener.Receive( [ref]$remoteIPEP );
  }
  catch {
    Write-Host "$($_.Exception.Message)"
    break;
  }
  write-host "Received"
    
  # deserialize
  [string]$recStr = [System.Text.Encoding]::Unicode.GetString( $buffer ); 

  Write-Host $recStr;

  if( $recStr -eq 'Exit' ) {
    $work = $false;
  }
}

$listener.Close();

# $socket.Shutdown( [system.net.sockets.socketshutdown]::both );
# $socket.Close();
# $socket = $null;

