# get all archive file names

[string]$PATTERN = '\.7z(\.[0-9]{3})?$|\.zip(\.[0-9]{3})?$'
[string]$PATH = 'f:\logs\1826526'
[string]$xtract_dir = 'out'

$archives = ( Get-Childitem -path $PATH -recurse | Where-Object { $_.name -match $PATTERN -And -Not $_.PSIsContainer } )
#$archives = ( Get-Childitem -path $PATH | Where-Object { $_.name -match $PATTERN -And -Not $_.PSIsContainer } )

# echo $archives

foreach ( $item in $archives ) 
{
    $subdir = $xtract_dir + '\' + $item.name

    if ( test-path ".\$subdir" ) # if directory exists, append time suffix to make it unique
    {
        $subdir += ( Get-Date -uformat %H%M%S )
        #write-host $subdir
    }

    New-Item ".\$subdir" -itemtype directory

    #write-host $subdir
    [string]$cmnd1 = '-o".\' + $subdir + '"'
    [string]$cmnd2 = '"' + $($item.fullname) + '"'
    write-host $cmnd1 $cmnd2
    #get-member -inputobject $cmnd
    #get-member -inputobject $subdir

    #& 7z $cmnd
    #$AllArgs = @( '-o".\' + $subdir + '"'cmnd1, $cmnd2 )
    & 7z x $cmnd1 -- $cmnd2
}
