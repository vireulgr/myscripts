# 
param( [string]$SrcRt = "S", [string]$SrcDir = "Confi" )

function CreateShortcut {
    param( [string]$Target, [string]$Location = "$home\Desktop\NewShortcut.lnk")
    $WshShell = new-object -COMObject WScript.Shell;
    $ShCut = $WshShell.CreateShortcut($Location);
    if( $? ) {
        $ShCut.TargetPath = $Target;
        $ShCut.Save();
    }
    else {
        Write-Host "Cannot create shortcut to $Target";
    }
}

$SrcDir = "${SrcRt}:\$SrcDir";

$DesktopPath =  "${HOME}\Desktop";

Write-Host "In SWDL"

# MSI s -- replaced with shortcuts to build directories
# Copy-Item "$SrcDir\DLVI*\*" $DesktopPath
# Copy-Item "$SrcDir\DL80v*\*" $DesktopPath
# scripts -- already in folder
# Copy-Item -Path "$SrcRt\Scripts\functions.ps1" -Destination $DesktopPath
# Copy-Item -Path "$SrcRt\Scripts\updCommon.ps1" -Destination $DesktopPath

Write-Host "Browser, rutoken, debugger"
# Browser -- do we really need this?
Copy-Item "${SrcRt}:\Yandex*" $DesktopPath -ErrorAction SilentlyContinue
if( $? -eq $false ) { Write-Host "Error copying yandex"; }
# RUTOKEN drivers -- needed only on SSVI machine
Copy-Item "${SrcRt}:\rtDrivers.x64.v.2.100.00.0542.exe" $DesktopPath -ErrorAction SilentlyContinue
if( $? -eq $false ) { Write-Host "Error copying RuToken"; }
# Remote debugger
Copy-Item "${SrcRt}:\Remote Debugger\x64" $DesktopPath -Recurse -ErrorAction SilentlyContinue
if( $? -eq $false ) { Write-Host "Error copying Remote debugger"; }

Write-Host "Vim"
# Vim settings
Copy-Item "${SrcRt}:\Vim\vimfiles" "C:\Users\${env:UserName}" -Recurse -ErrorAction SilentlyContinue
if( $? -eq $false ) { Write-Host "Error copying vimfiles"; }
# Vim folder
Copy-Item "${SrcRt}:\Vim"          "${env:ProgramFiles(x86)}" -Recurse -ErrorAction SilentlyContinue
if( $? -eq $false ) { Write-Host "Error copying vim"; }
# assoc vim session file type (vis) with vim
cmd /D /C "assoc .vis=vimsession" | Out-Null
cmd /D /C "ftype vimsession=`"${env:ProgramFiles(x86)}\Vim\Vim80\gvim.exe`" -S `"%1`" `"%2`" `"%3`" `"%4`"" | Out-Null

# !!!!!!!!!!!!! INSTALL PS5!! (this is for Win7x64) Bad luck (((( 
# \\george-808\vmshared\soft\Win7AndW2K8R2-KB3134760-x64.msu
#
Write-Host "Shortcuts"
# Shortcut on a desktop for remote debugger
CreateShortcut "$DesktopPath\x64\msvsmon.exe" "$DesktopPath\RmDbgAgent.lnk";
# Shortcut on a desktop for Vim
CreateShortcut "${env:ProgramFiles(x86)}\Vim\Vim80\gvim.exe" "$DesktopPath\gvim.lnk";

