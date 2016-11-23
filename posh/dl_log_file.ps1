param( [string]$logName = '20160603_BB_FP_2578_BPfanedler_M060_C2_E230.500_16223AC2_Driving_Test', 
        [int]$year = [int]$(get-date -UFormat "%Y"), 
        [int]$weekNum = [int]$(get-date -UFormat "%W") )

#$logName        = '20160603_BB_FP_2578_BPfanedler_M060_C2_E230.500_16223AC2_Driving_Test'
$stabNetDir     = '\\OEFIW3FS05.hbi.ad.harman.com\Archivetraces\DC\NTG5\stability'
$stabLocalDir   = 'G:\LogDir'

$yearDir        = $year #'2016'
$curWeekDir     = "CW$weekNum"

write "Searching for log name  $logName  in  $stabNetDir`\$yearDir`\$curWeekDir "

# search for archive with required name
#$repoLogPath = gci $stabNetDir -exclude "analysis","results" -filter $logName -recurse
$localLogPath = gci "$stabNetDir`\$yearDir`\$curWeekDir`\*" -exclude '*analysis*','*results*' -filter "$logName`*" 
write "found: $localLogPath"

#$yearDir = $repoLogPath.split('\')[-2]
#$curWeekDir = $repoLogPath.split('\')[-1]

if( $localLogPath ) { 

    if( test-path "$stabLocalDir`\$yearDir`\$curWeekDir`\$logName" ) {
        write-host "file `"$stabLocalDir`\$yearDir`\$curWeekDir`\$logName`" exist, skip to next"
        continue
    }

    write "Downloading log $logName to  $stabLocalDir`\$yearDir`\$curWeekDir"
    #write '#commented out'
    #copy-item $localLogPath.FullName "$stabLocalDir`\$yearDir`\$curWeekDir"

    # copy using windows shell
    $shell = New-Object -Com Shell.Application
    $shell.NameSpace("$stabLocalDir`\$yearDir`\$curWeekDir").CopyHere( $($localLogPath.FullName) )

    # $shell = New-Object -Com Shell.Application
    # $folder = $shell.NameSpace("$path\Folder")
    # $shell.NameSpace($otherpath).CopyHere($folder)
}

