# get current PoSh version
write-output $PSVersionTable.PSVersion
# display files only
get-childitem .\ -Recurse | where-object {!$_.PSIsContainer} # | select fullname -first 10

# выбрать файлы .hpp и .cpp из директории 

[string]$PATTERN='\.cpp$|\.hpp$'
[string]$PATH='F:\HarmanSystem\p4\Work_System\Work_System\imp\ntg5\pathology'
[string]$OUT_FILE='.\filelist.txt'

Get-Childitem -path $PATH -recurse | Where-Object {$_.Name -match $PATTERN} | Select-Object FullName | Out-File $OUT_FILE -encoding "UTF8" 


# get directory size

get-childitem -recurse | measure-object -sum Length


# print pretty size
#
# TODO
function FormatSize
{
    param( [int]$bytes )
    [int]$mega = 0
    [int]$kilo = 0
    [int]$bytes = 0
    # switch( $bytes )
    # {
    #     { $_ / (1024*1024) -gt 1 } { $mega = $_ / (1024*1024) }
    #     { $_ / (1024) -gt 1 } { $kilo = $_ / (1024) }
    #     { $_ -gt 1 } { $bytes = $_ / (1024) }
    # }
    $mega = $bytes / (1024*1024)
    $kilo = ( $bytes - $mega * 1024*1024 ) / 1024
    $bytes = $bytes - $mega*1024*1024 - $kilo*1024
    if( $mega > 1 ) { echo $mega + "Mb" }
    if( $kilo > 1 ) { echo $kilo + "Kb" }
    if( $bytes > 1 ) { echo $bytes + "bytes" }
}
