#

$filepattern = "\mfc{0}.html"
$targetDir = "E:\Docs\books\ProgIT\MFC"

$urlsite = "www.codenet.ru"
$urlbase = "$urlsite/progr/visualc/mfc"
$urlpartspattern = "mfc{0}.php"

New-Item $targetDir -ItemType Directory -ErrorAction SilentlyContinue

for( $i = 1; $i -le 11; ++$i ) {
  $urlpart = $urlpartspattern -f $i
  $filePart = $filepattern -f $i

  # basic content
  $resp = Invoke-WebRequest "$urlbase/$urlpart"  -UseBasicParsing
  $tempStr = $resp.Content | Select-String -Pattern "(?s)cn-hline`"\>(.*)\<div\ class=`"hr`""  `
    | % { $_.Matches.Groups[1].Value -replace "(?s)\<script.*?\<\/script\>","" }

  $tempStr -replace "\/np-includes","np-includes" -replace "\.php",".html" | Set-Content "$targetDir\$filepart"


  # images
  $ImgUrls = $resp.Images.src | Select-String -SimpleMatch -NotMatch "http"  | % { $_.Line }
  ForEach( $url in $imgUrls ) {

    if( -not $url ) { continue; }

    $lastSlash = $url.LastIndexOf( '/' )
    $UrlDirPart = $url.SubString( 0, $lastSlash )
    New-Item "$targetDir/$UrlDirPart" -ItemType Directory -ErrorAction SilentlyContinue

    Invoke-WebRequest "$urlsite/$url" -UseBasicParsing -OutFile "$targetDir/$url"
  }

  start-sleep 5
}
