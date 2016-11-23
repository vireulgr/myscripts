# Script to obtain baseline by version name
# 
#
param( [string]$buildVersion )

$versionPattern = "[PR]L_NTG5_[0-9]{3}.[0-9]{2}[0-9a-z]_[0-9A-Z]{8}"
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

#$url = "http://hifiwscc07.ad.harman.com/cgi-bin/dai-ntg5/dbis.pl"
#$current = "PL_NTG5_230.408_16216AC2"
#$current = "PL_NTG5_230.408_16216AC2_M067"
$url = "http://hifiwscc07.ad.harman.com/cgi-bin/dai-ntg5/dbis.pl?current=$current"
$out = "F:\\docs\\ps_down_file.html"
$request.Headers.Add( "User-Agent", $userAgent )
$request.DownloadFile( $url, $out )
write "Download complete"

$baselinePat = '\<td\>[^<]+?TCFG[^<]+?\<.td\>[trd<>/ ]+?([0-9]+?)\<.td>'
# Get-Content $out | WHERE { $_ -match "\<tr>[^<]TCFG[^<]\<td\>([0-9]+)\<\/td\>","$1" }
#$str = "<td><a href='file:'></a></td></tr><tr><td>Date of Latest Submitted TCFG</td> <td>2016/05/27 19:40:42</td></tr><tr><td>//Daimler_NTG_5/Public/TCFG/Development/Default/... up to</td><td>4653046</td></tr><tr><td colspan='2'><h3>PD Applications</h3></td></tr>" 
gc $out | % { if( $_ -match $baselinePat ) { Write-Host  "Baseline: $($matches[1])" -foregroundcolor "magenta" } }
# if( $str -match $pat ) {
#     Write-host "code: $($matches[1])"
# }

#"<td><a href='file:'></a></td></tr><tr><td>Date of Latest Submitted TCFG</td> <td>2016/05/27 19:40:42</td></tr><tr><td>//Daimler_NTG_5/Public/TCFG/Development/Default/... up to</td><td>4653046</td></tr><tr><td colspan='2'><h3>PD Applications</h3></td></tr>" | Select-string '\<tr\>[^<]TCFG[^<]\<td\>([0-9]+)\<\/td\>'
#"<td><a href='file:'></a></td></tr><tr><td>Date of Latest Submitted TCFG</td> <td>2016/05/27 19:40:42</td></tr><tr><td>//Daimler_NTG_5/Public/TCFG/Development/Default/... up to</td><td>4653046</td></tr><tr><td colspan='2'><h3>PD Applications</h3></td></tr>" | Select-string -pattern 'TCFG'


