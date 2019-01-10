# Script to obtain baseline by version name
# 
#
param( [string]$buildVersion )

$versionPattern = "[PR]K_PCA_[0-9]{3}.[0-9]{2}[0-9a-z]_[0-9A-Z]{8}"
$userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36" 

# getting proxy credentials
$proxy = [System.Net.WebRequest]::GetSystemWebProxy()
$proxy.Credentials = [System.Net.CredentialCache]::DefaultCredentials

$current = ''
write $buildVersion
if( $buildVersion -match $versionPattern ) {
    $current = $($matches[0])
}
else {
    write "Achtung! Wrong version format!!"
    #[Environment]::Exit(0)
    Break
}
write "Current read as: $current"

# request
$request = New-Object System.Net.WebClient
$request.UseDefaultCredentials = $true              # proxy credentials only
$request.Proxy.Credentials = $request.Credentials

$url = "http://servername.com/cgi-bin/script.pl?current=$current"
$out = "F:\\docs\\ps_down_file.html"
$request.Headers.Add( "User-Agent", $userAgent )
$request.DownloadFile( $url, $out )
write "Download complete"

$baselinePat = '\<td\>[^<]+?THFD[^<]+?\<.td\>[trd<>/ ]+?([0-9]+?)\<.td>'
# Get-Content $out | WHERE { $_ -match "\<tr>[^<]THFD[^<]\<td\>([0-9]+)\<\/td\>","$1" }

gc $out | % { if( $_ -match $baselinePat ) { Write-Host  "Baseline: $($matches[1])" -foregroundcolor "magenta" } }
# if( $str -match $pat ) {
#     Write-host "code: $($matches[1])"
# }
