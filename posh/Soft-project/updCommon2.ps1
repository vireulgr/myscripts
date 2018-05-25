# ?? Копировать сами файлы в отдельное место и делать символьные ссылки на файлы в нужной директории
# Сделать так, чтобы можно было обновлять только те файлы, которые новее текущих, а не все подряд
# Не стоит останавливать консоль, если не собираемся её обновлять.
#
# function MakeReplaceElem {
#   param( [string]$src, [string]$dst, [string[]]$exe )
#   return New-Object PSObject -Property @{ SrcPath=$src; DestPath=$dst; ExecDeps=$exe }
# }
#
# для всех элементов замены
#   если объект из DestPath НЕ существует
#     копировать из SrcPath в DestPath
#     следующий ReplaceElement
#
#   $a = время изменения объекта из SrcPath 
#   $b = время изменения объекта из DestPath
#   если $a -le $b
#     следующий ReplaceElement
#
#   для всех процессов из ExecDeps
#     если процесс работает
#       остановить процесс
#       ждать
#       если процесс работает
#         ошибка
#         следующий ReplaceElement
#     
#   копировать с созданием бэкапа (если бэкап есть - перезаписать файл DestPath)
#   BkUpnCopy
#

$referenceFiles = @("a","b","c")

$assembledFiles = @("b","d")

$currentFiles = @("a","b","e")


$destName = $wasya;
$srcName = $petya;

#write-host "$((get-item $el[0]).LastWriteTime) and $((get-item $destFile).LastWriteTime)"
$src = get-item $srcName; 
if( Test-Path $destName ) {
    $dest = get-item $destFile;
    if( $src.LastWriteTime -le $dest.LastWriteTime ) {
        #Write-Host "[W] Not newer than dest: $($el[0])"
        continue;
    }
}
