# âûáðàòü ôàéëû .hpp è .cpp èç äèðåêòîðèè 

[string]$PATTERN='\.cpp$|\.hpp$'
[string]$PATH='F:\path\to\files'
[string]$OUT_FILE='.\filelist.txt'

Get-Childitem -path $PATH -recurse | Where-Object {$_.name -match $PATTERN} | Select-Object FullName | Out-File $OUT_FILE -encoding "UTF8" 
