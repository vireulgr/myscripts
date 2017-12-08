
# ==================================
# print pretty size with measure units
# ==================================
# TODO
function FormatSize
{
    param( [long]$arg )

#     $MB_MUL = 1024*1024
#     $KB_MUL = 1024
#     $B_MUL = 1
# 
#     [int]$megabytes = [Math]::Floor( $arg / $MB_MUL )
#     [int]$kilobytes = [Math]::Floor( $arg / $KB_MUL ) - $megabytes * $MB_MUL / $KB_MUL
#     [int]$bytes = [Math]::Floor( $arg / 1 ) - $megabytes * $MB_MUL/$B_MUL - $kilobytes * $KB_MUL/$B_MUL
# 
#     write-host $megabytes " Mb " $kilobytes " kb " $bytes " b "

    # arrays needed to represent units
    $txt = @( "bytes", "kb", "Mb", "Gb", "Tb" )
    $muls = @( 1, 1024, (1024*1024), (1024*1024*1024), (1024*1024*1024*1024) )
    # result coefficients before each unit
    [int[]]$coefs = @( 0, 0, 0, 0, 0 )

    # process first coefficients, before the last one
    for( $i=0; $i -lt $muls.length - 1; $i++) {
        $partSum = 0
        for( $k = 0; $k -lt $i - 2; $k++ ) {
            $partSum += $coefs[$k] * $muls[$k]
            # write-host "part sum is " $partSum
        }
        $coefs[$i] = ( $arg % $muls[$i+1] - $partSum ) / $muls[$i]
        # write-host "coefs " $i " is " $coefs[$i]
    }

    # get last (biggest) coefficient
    $partSum = 0
    for( $k = 0; $k -lt $i - 1; $k++ ) {
        $partSum += $coefs[$k] * $muls[$k]
        # write-host "part sum is " $partSum
    }
    $coefs[$coefs.length - 1] = ($arg - $partSum) / $muls[$coefs.length -1 ]
    
    for( $i = $txt.length -1; $i -ge 0; $i-- ) {
        if( $coefs[$i] -ne 0 ) {
            write-host -nonewline $coefs[$i] $txt[$i] " "
        }
    }
    write-host " "
}

# ====================
# message box example
# ====================

function MsgBoxExample {
    param( [string]$text = "Message box", [string]$caption = "Information" )

    Add-type -assemblyName System.Windows.Forms

    $result = [System.Windows.Forms.MessageBox]::Show( $text, $caption,
                                                        [System.Windows.Forms.MessageBoxButtons]::YesNo,
                                                        [System.Windows.Forms.MessageBoxIcon]::Information,    
                                                        [System.Windows.Forms.MessageBoxDefaultButton]::Button1,
                                                        [System.Windows.Forms.MessageBoxOptions]::ServiceNotification )
#
# Also available simlpe [System.Windows.Forms.MessageBoxButtons]::OK button
#

    if ( $result -eq 'Yes' ) {
        write 'user clicked yes'
    }
    else {
        write 'User Clicked No!'
    }
}

# =================================================
# function for getting MD5 sum for a file contents
# =================================================

function MD5File {
    param( [string]$file ) # file - path to a file

    $fullPath = Resolve-path $file

    $algo = [System.Security.Cryptography.HashAlgorithm]::Create("MD5")
    $stream = New-Object System.IO.FileStream($fullPath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read )

    $md5StringBuilder = New-Object System.Text.StringBuilder
    $algo.ComputeHash($stream) | % { [void] $md5StringBuilder.Append($_.ToString("x2")) }
    $md5StringBuilder.ToString()

    $stream.Dispose()
}

# =================================================
# function for getting MD5 sum for a file contents
# =================================================

function dateFromName {
    param( [string]$fileName = "20160614_16241AC2_Some_Test" )

    $Datestr = $fileName.split('_')[0]

    [DateTime]$dt = new-object DateTime

    [DateTime]::TryParseExact( $DateStr, "yyyyMMdd", [System.Globalization.Cultureinfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::None, [ref]$dt )

    return $DateStr
}

