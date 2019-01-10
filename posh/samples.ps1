# get current PoSh version
Write-Output $PSVersionTable.PSVersion
# display files only
Get-ChildItem .\ -Recurse | where-object {!$_.PSIsContainer} # | select fullname -first 10

# выбрать файлы .hpp и .cpp из директории 

[string]$PATTERN='\.cpp$|\.hpp$'
[string]$PATH='F:\HarmanSystem\p4\Work_System\Work_System\imp\ntg5\pathology'
[string]$OUT_FILE='.\filelist.txt'

Get-ChildItem -path $PATH -recurse | Where-Object {$_.Name -match $PATTERN} | Select-Object FullName | Out-File $OUT_FILE -encoding "UTF8" 


# get directory size

Get-ChildItem -Recurse | Measure-Object -Sum Length


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

# parse date from string
$fileName = "20110324_rR_rR_6789_menainglessword_d169_L2K1016L241PV_Driving_Test"
$Datestr = $fileName.split('_')[0]

[DateTime]$dt = New-Object DateTime

[DateTime]::TryParseExact( $DateStr, "yyyyMMdd", [System.Globalization.Cultureinfo]::InvariantCulture,
                            [System.Globalization.DateTimeStyles]::None, [ref]$dt )


# copy all files with the same name to one directory, renaming them
$rootDir = 'F:\dir\target'
$destDir = 'F:\tempDir\enumBins'

$binAlias = 'filename'

sl $rootDir
$binaries = gci . -recurse -filter $binAlias | ? { !$_.psiscontainer } 

new-item -itemtype Directory -Force -Path $destDir

[int]$cnt = 0
ForEach ( $binaries ) {
    $cnt += 1
    copy-item $_.fullname "$destDir\$($_.name)$cnt"  
}

