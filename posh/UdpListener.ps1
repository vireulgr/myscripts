$port = 27183

Try {
    Write-host "UDP listener is starting @ port $port"
    While( $True ) {
        $ep = New-Object System.Net.IPEndpoint( [IPAddress]::Any, $port )
        $client = New-Object System.Net.Sockets.UDPClient $port

        $in = $client.Receive( [ref] $ep );
        $text = [Text.Encoding]::ASCII.GetString( $in )
        Write-Host "$($ep.Address.ToString()):$($ep.Port.ToString()) msg: $text"
        $client.Close();
        Start-Sleep -Milliseconds 400
    }
}
Catch {
    "$($Error[0])"
}
