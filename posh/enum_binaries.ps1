$rootDir = 'F:\P4\p4_client_dev'
$destDir = 'F:\tempDir\enumBins'

$binAlias = 'scp'

sl $rootDir
$binaries = gci . -recurse -filter $binAlias | ? { !$_.psiscontainer } 

new-item -itemtype Directory -Force -Path $destDir

[int]$cnt = 0
ForEach ( $binaries ) {
    $cnt += 1
    copy-item $_.fullname "$destDir\$($_.name)$cnt"  
}

