$port = 27183
$hostname = 'localhost'
$message = 'hello from vireulgr'

Try {
    $client = New-Object System.Net.Sockets.UDPClient
    $out = [Text.Encoding]::ASCII.GetBytes( $message )
    [void] $client.Send( $out, $out.length, $hostname, $port )
    Write-Host "$message $($hostname):$($port)"
    $client.Close();
}
Catch {
    "$($Error[0])"
}
