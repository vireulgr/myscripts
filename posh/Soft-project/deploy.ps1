
[int]$port = 27183

function CreateEndpoint {
  param( [string]$hostname, [int]$port ) 

  $iphostentry = $null;

  Write-Host "getting host entry for $hostname"
  try{ 
    $iphostentry = [System.Net.Dns]::GetHostEntry( $hostname );
  }
  catch {
    Write-Host "exception: $($_.Exception.Message)"
    Write-Host "cannot resolve $hostname"
    return $null;
  }
  # finally {
  # }

  $ip = $null
  foreach( $addr in $iphostentry.AddressList ) {
    if( $addr.AddressFamily -eq [system.net.sockets.addressfamily]::internetwork ) {
      $ip = $addr;
      break;
    }
  }
  if( $ip -eq $null ) {
    Write-Host "Can't find IPv4 address";
    return $null
  }

  $ipendpoint = New-Object System.Net.IPEndpoint $ip, $port 

  return $ipendpoint
}

