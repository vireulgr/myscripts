#
#
# Script will get core file, get shared libs dependencies, try to find those 
# shared libs, copy found files to workdir and finally get backtrace with GDB
#

param( [string]$corePath = './Prediction.core' )

function findBin {
    param( [string[]]$fileName = 'libsocket.so.3', [string]$rootPath, [string[]]$inList, [string[]]$exList )

    [string]$includeRegExp = '^('
    foreach ( $item in $inList ) {
        if( -not $item ) { continue; }
        $includeRegExp = "$includeRegExp(?=.*$item)|"
    }
    $includeRegExp = $($includeRegExp -replace "\)\|$",")).*$")

    [string]$excludeRegExp = '^('
    foreach ( $item in $exList ) {
        if( -not $item ) { continue; }
        #$excludeRegExp = "$excludeRegExp(?=.*$item)"
        $excludeRegExp = "$excludeRegExp(?=.*$item)|"
    }
    $excludeRegExp = $($excludeRegExp -replace "\)\|$",")).*$")

    #gci $rootPath -recurse -include $fileName -exclude $exList `
    #    | ? { -not $_.psiscontainer `
    #        -and $_.FullName -match $includeRegExp -and $_.FullName -notmatch $excludeRegExp } `
    #    | SELECT -expandProperty FullName

    [string[]]$fileList = gci $rootPath -recurse -include $fileName `
        | ? { -not $_.psiscontainer `
            -and $_.FullName -match $includeRegExp -and $_.FullName -notmatch $excludeRegExp `
             } `
        | SELECT -expandProperty FullName
    #$fileList = gci $rootPath -recurse -include $fileName -exclude $exList `
    #    | ? { -not $_.PSisContainer -and $_.FullName -match $includeRegExp -and $_.FullName -notmatch $excludeRegExp } | SELECT -expandProperty FullName

    #gci $rootPath -recurse -include $fileName -exclude $exList `
    #    | ? { -not $_.psiscontainer -and $_.FullName -match $includeRegExp } | SELECT -expandProperty FullName

    #gci $rootPath -recurse -include $fileName `
    #    | ? { -not $_.PSisContainer -and $_.FullName -match $includeRegExp -and $_.FullName -notmatch $excludeRegExp } | SELECT -expandProperty FullName

    #gci $rootPath -recurse -include $fileName `
    #    | ? { -not $_.PSisContainer -and $_.FullName -match $includeRegExp } | SELECT -expandProperty FullName

    #$fileList | % { write $_.fullname }
    $fileList
    #return #$fileList
}

# ======================================================
# Start of the script
# ======================================================

# ====================================================
# Settings
# ====================================================

[string]$root = 'F:\P4\p4_client_dev\deliveries'

#####################
# Patterns
#####################

#[string[]]$excludeList = "ntr", "flex", "asia",                     "j6", "arm", "aml"    # for Intel
#[string[]]$excludeList = "ntr", "flex", "asia", "intel", "x86"                            # for AML
#[string[]]$excludeList = "ntr", "flex", "asia", "intel", "x86", "j6"                      # for Jacinto
 [string[]]$excludeList = "ntr", "flex", "asia", "intel", "x86",                  "aml"    # for J6

 [string[]]$depIncList = "-osz", "-rel", "rtti"
#[string[]]$depIncList = "osz-trc-rel-rtti","9092"                                            # for Intel and Jacinto (arm)
#[string[]]$depIncList = "armv7-qnx-m650sp1-4.4.2-osp-trc-rel-rtti", "armle-v7"               # HMI_App J6; manually copy scp j6, not armle(-v7)
#[string[]]$depIncList = "sys-ssp-tr-ntg5_M067_j6_m650sp1", "jacinto6-ntg5", "armle-v7"       # HMI_App J6; manually copy scp j6, not armle(-v7)
#[string[]]$depIncList = "sys-graphic-650sp1-jacinto6-ntg5", "armle-v7", "runtimeSDK-debug"   # adl J6
#[string[]]$depIncList = "sys-qnx-650sp1-all", "armle-v7"                                     # JpnItsl

[string[]]$binIncList = ,'j6'

$NOT_PREFERRED_KEYWORDS = ,'-dbg';

#####################

[string]$gdb = 'g:\AnalysisTools\perl\icb\ntoarm-gdb.exe'

[string]$unitType = 'HU'
if( $unitType -eq 'FU' ) {
    $binIncList  += '9091'

    $depIncList  += '9091'

    $excludeList += '9083'
    $excludeList += '9099'
}
else {
    $depIncList  += '9083'
    $depIncList  += '9099'

    $binIncList  += '9083'
    $binIncList  += '9099'

    $excludeList += '9091'
}

$findLibsGDBScript = 'g:\AnalysisTools\perl\icb\find_libs.gcf'
$getBTGDBScript = 'g:\AnalysisTools\perl\icb\backtrace.gcf'
$libDepsFile = 'lib_list.txt'

# =============================================
# =============================================

# get working directory
$workDir = $( Split-Path $corePath -parent )

# get binary name
$( Split-Path $corePath -leaf ) -match '^(.*)\.core.*$' | out-null
$binName = $($matches[1])


[string[]]$results = findBin $binName $root $binIncList $excludeList 
#[string[]]$results = findBin $binName $root $includeList $excludeList 
#   if there are several files, which are suitable for search query, show question
[int]$ind = 0
if( -not $results ) {
    write "Error: Can't find corresponding binary"
    return
}
[int]$choose = 0

if( $($results.length) -gt 1 ) {

    $results | % { write "$ind => $_"; $ind++ }
    #for( [int]$i = 0; $i -le $($results.Length); $i++ ) {
    #    write-host "$i -> $($results[$i])"
    #}
    [int]$choose = read-host -Prompt 'Enter number of your choose'
    write "You choose $choose -> $($results[$choose])"
}

# Copy item to working directory 
copy-item $($results[$choose]) $workDir -force

# get list of needed shared libs
#   execute gdb with necessary script file
&  $gdb "$workDir`\$binName" "$workDir`\$binName.core" -q -x "$findLibsGDBScript" 2>&1 | out-null

#   get files list from the output file
if( test-path  "$workDir`\$libDepsFile" ) {
    get-content "$workDir`\$libDepsFile" | SELECT -skip 1 | % { 
        [string[]]$depends += ($_ -replace '^(?:[a-fxA-F0-9]+\s+){0,2}\s*(?:Yes|No)\s+([^ \t]+)$','$1') | split-path -leaf
    }
}

( clear-variable results )
$results = findBin $depends $root $depIncList $excludeList 

foreach ( $dep in $depends ) {

# search and copy files to workdir
#   if there are several files, which are suitable for search query, show question
    if( -not $results ) {
        write "Error: Can not find dependency library $dep"
        continue
    }
    [int]$choose = 0
    [int]$ind = 0

    if( $($results.length) -gt 1 ) {

        foreach( $item in $results ) { write "$ind => $item"; $ind++ }

        [int]$choose = read-host -Prompt 'Enter the number of your choice'
        write "You choose $choose -> $($results[$choose])"
    }

    #   Copy item to working directory 
    copy-item $($results[$choose]) $workDir -force
}

# additional
$libmountObserve = "F:/P4/p4_client_dev/tcfg/ntg5/9083_B1/arm/fs/ifs/boot/overrides/boot/lib/libmountObserve.so";
copy-item $libmountObserve $workDir

#   execute gdb with necessary script file
&  $gdb "$workDir`\$binName" "$workDir`\$binName.core" -q -x "$getBTGDBScript" 2>&1 | out-null


