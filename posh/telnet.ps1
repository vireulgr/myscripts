## Connect-Computer.ps1
## Interact with a service on a remote TCP port
# f:\distr\WinDump.exe -qNnXt host 10.13.15.133 and host HINNP59762.symphonyteleca.com and port 23 > packets.txt
#
#


param( [string] $remoteHost = "localhost", [int] $port = 23, [string[]] $commands )

$TempLogFilePath = "Temp.log"

Start-Transcript -Path "$TempLogFilePath"

try { ## Open the socket, and connect to the computer on the specified port
	write-host "Connecting to $remoteHost on port $port"
	$socket = new-object System.Net.Sockets.TcpClient($remoteHost, $port)

	if($socket -eq $null) {
		throw ("Could Not Connect")
	}

    #write-host "Wait some time"
    #start-sleep 1

	$stream = $socket.GetStream() 
    $writer = new-object System.IO.StreamWriter($stream)

	$buffer = new-object System.Byte[] 1024
	$encoding = new-object System.Text.AsciiEncoding

    $writer.Write( @( 0xff, 0xfb, 0x1f, 0xff, 0xfb, 0x20, 0xff, 0xfb, 0x18, 0xff, 0xfb, 0x27, 0xff, 0xfd, 0x01, 0xff, 0xfb, 0x03, 0xff, 0xfd, 0x03) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xff, 0xfc, 0x23 ) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xFF, 0xFC, 0x24 ) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xff, 0xfa, 0x1f, 0x00, 0x50, 0x00, 0x18, 0xff, 0xf0 ) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xff, 0xfa, 0x20, 0x00, 0x33, 0x38, 0x34, 0x30, 0x30, 0x2c, 0x33, 0x38, 0x34, 0x30, 0x30, 0xff, 0xf0 ) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xff, 0xfa, 0x27, 0x00, 0xff, 0xf0 ) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xff, 0xfa, 0x18, 0x00, 0x58, 0x54, 0x45, 0x52, 0x4d, 0xff, 0xf0 ) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xff, 0xfa, 0x18, 0x00, 0x58, 0x54, 0x45, 0x52, 0x4d, 0xff, 0xf0 ) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xff, 0xfc, 0x01 ) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xff, 0xfe, 0x05 ) )
    $writer.Flush()
    start-sleep 1
    $writer.Write( @( 0xff, 0xfc, 0x21 ) )
    $writer.Flush()
    start-sleep 1
    $writer.WriteLine( "root" )
    $writer.Flush()
    start-sleep 1
    $writer.WriteLine( "root" )
    $writer.Flush()
    start-sleep 1

    # 0xFB - Will 0xfc - Won't  
    # $writer.Write( 0xFF ) # IAC
    # $writer.Write( 0xFC ) # WONT
    # $writer.Write( 0x08 ) #  8 Output line width? backspace? 
    # $writer.Write( 0xFF ) # IAC
    # $writer.Write( 0xFC ) # WONT
    # $writer.Write( 0x20 ) # 32 terminal speed
    # $writer.Write( 0xFF ) # IAC
    # $writer.Write( 0xFC ) # WONT
    # $writer.Write( 0x23 ) # 35 x display location
    # $writer.Write( 0xFF ) # IAC
    # $writer.Write( 0xFC ) # WONT
    # $writer.Write( 0x27 ) # 39 new environment option
    # $writer.Write( 0xFF ) # IAC
    # $writer.Write( 0xFC ) # WONT
    # $writer.Write( 0x24 ) # 36 # Enter username and password
    #$writer.WriteLine("root`n") 
    #$writer.Flush()
    #write-host "Wait some time"
    #start-sleep 1
    #$writer.WriteLine("root`n") 

	#Loop through $commands and execute one at a time.

	for($i=0; $i -lt $commands.Count; $i++) { ## Allow data to buffer for a bit start-sleep -m 500

		## Read all the data available from the stream, writing it to the ## screen when done.
		while($stream.DataAvailable) {
			$read = $stream.Read($buffer, 0, 1024)
			write-host -n ($encoding.GetString($buffer, 0, $read))
		}

		write-host $commands[$i]
		## Write the command to the remote host
		$writer.WriteLine($commands[$i]) 
        $writer.Flush()

        write-host "Wait some time"
        start-sleep 2
	}

	#runs CheckLogs.ps1 script and sends in the output from the telnet emulation and searches for HTML string
	# .\CheckLogs.ps1 -LogFile "$TempLogFilePath" -SearchStrings @('HTML')

	# if($LASTEXITCODE -eq 0) {
	# 	# If string wasnt found then an error is thrown and caught
	# 	throw ("Text Not found")
	# }

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
	$writer.Close()
	$stream.Close()

	stop-transcript
}
