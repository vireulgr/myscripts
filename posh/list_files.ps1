# выбрать файлы .hpp и .cpp из директории 

[string]$PATTERN='\.cpp$|\.hpp$'
[string]$PATH='F:\HarmanSystem\p4\Work_System\Work_System\imp\ntg5\pathology'
[string]$OUT_FILE='.\filelist.txt'

Get-Childitem -path $PATH -recurse | Where-Object {$_.name -match $PATTERN} | Select-Object FullName | Out-File $OUT_FILE -encoding "UTF8" 
