cd 'g:\'
[string[]]$includeList = 'arch1','var1'
[string]$includeRegExp = ''
foreach ( $item in $includeList ) {
    $includeRegExp = "$includeRegExp(?=.*$item)"
}
write $includeRegExp

gci tempDir -recurse -include doc1* -exclude '*results*', '*analysis*' | ? { $_.psiscontainer -eq $false -and $_.fullname -match $includeRegExp } | select fullname
write ''