# Setup

$VMSharedDir = "\\GEORGE-808\VMShared"; 
$SrcRoot = "S:";

$DLVIDir = "C:\\DLLOCK80\\DLVI";

. .\functions.ps1 

# Connect remote drive
if( -not (Test-Path $SrcRoot) ) {
    MakeRemoteDisk $VMSharedDir "$($SrcRoot.Chars(0))"
}
if( -not (Test-Path .\settings.reg) ) {
    Write-Host "Cannot find registry settings file; Exiting";
    exit;
}

# Configure VM
# - Default keyboard layout - English
# - Set up not to turn off display 
# - Shortcut on a desktop for command line              -- no need
# - Configure cmd.exe (font, window size)               -- In reg file
# - Network share folder connected as network disk      -- Done upper
# - Display file extension for registered file types    -- In reg file
# - Disable Andimalware service executable              -- TODO

# schtasks /create /RU "NT AUTHORITY\LOCALSERVICE" /SC ONLOGON /TN Gosha\RemoteDebug /TR C:\Users\Username\Desktop\x64\msvsmon.exe /RL HIGHEST
$cmdToRun = "C:\Users\Username\Desktop\x64\msvsmon.exe" 
$schtasksCmd = "schtasks /create /SC ONLOGON /TN Gosha\RemoteDebug /TR `"$cmdToRun`" /RL HIGHEST"

cmd.exe /D /C $schTasksCmd

# !!!!!! ENable powershell remoting enable-psremoting
# Enable-PSRemoting -Force
# Set-Item -Path WSMan:\localhost\Client\TrustedClients -Value "george-808"
# <OPTIONAL> Sets one of the network interfaces as a private network
# Set-NetConnectionProfile -InterfaceIndex <nic_index> -NetworkCategory Private 

#cmdkey /generic:\\192.168.0.162\

# $StartTime = (Get-Date).AddMinutes( 2 ).ToLongTimeString();
# schtasks /create /S . /U isc\ggv /P psswd /SC ONCE /ST $StartTime /K /TN Gosha\RemoteDebug /TR C:\Users\Username\Desktop\x64\msvsmon.exe /RL HIGHEST

$contentValue = @'
@echo off
:: Hello! This is a startup batch file!
hostname
ipconfig | findstr "IPv4"
'@

New-Item -path "${HOME}\BatRC.bat" -ItemType File -Value $contentValue -ErrorAction SilentlyContinue

New-Item -path $profile -ItemType File -Value $contentValue -ErrorAction SilentlyContinue

( Get-Content settings.reg ) -replace '{THEUSERNAME}',"${env:UserName}" | Set-Content settings.reg;
regedit /s settings.reg;

$contentValue = @'
# addition by setupVM script
192.168.128.7       ws8vc60     ws8vc60.dl.local
192.168.128.5       ws12vc60    ws12vc60.dl.local
192.168.128.19      w7dlss      # w7dlss.dl.local - not in domain
192.168.128.23      w7dlls      # w7dlls.dl.local - not in domain
192.168.128.29      esxi61      esxi61.dl.local
192.168.128.31      esxi62      esxi62.dl.local
192.168.128.37      esxi62      esxi62.dl.local
# end of addition
'@

Add-Content "${env:windir}\System32\drivers\etc\hosts" -Value $contentValue

# Copy files
. .\swdl.ps1 "$($SrcRoot.Chars(0))" "Confi" 

Write-Host 'Turn off win firewall'
if( $PSVersionTable.PSVersion.Major -ge 3 ) {
    Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
}
else {
    netsh advfirewall set allprofiles state off
}
# add this values if installed on Windows 10 or 8 or similar servers
# [HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender]
# "DisableAntiSpyware"=dword:00000001
# 
# [HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection]
# "DisableBehaviorMonitoring"=dword:00000001
# "DisableOnAccessProtection"=dword:00000001
# "DisableScanOnRealtimeEnable"=dword:00000001


# Install browser
# Remove browser installation file

# Make a snapshot

# Install DL 8.0
# Install DL SecServer
# Install DLVI

Write-Host "$0 is done"
