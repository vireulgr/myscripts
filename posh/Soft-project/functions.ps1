# ================
# Processes
# >>>>>>>>>>>>>>>>
# stop-process -name "vcenteragentservice"
# taskkill
# get-process | ? { $_.processName -like "*vcenteragentservice*" }
# taskinfo
# <<<<<<<<<<<<<<<<

# ================
# Services
# >>>>>>>>>>>>>>>>
# Get-Service -Name "dl vi vcenter agent service"
# Stop-Service -Name "dl vi vcenter agent service"
# Start-Service -Name "dl vi vcenter agent service"
# <<<<<<<<<<<<<<<<

# ================
# Display resolution on Windows server 2012 with Powershell v3
# >>>>>>>>>>>>>>>>
# Get-DisplayResolution
# Set-DisplayResolution -width 1024 -height 768 -force
# <<<<<<<<<<<<<<<<

# ================
# Shutdown/Reboot
# >>>>>>>>>>>>>>>>
# Stop-Computer .    # ~ shutdown
# Restart-Computer . # ~ shutdown /r
# <<<<<<<<<<<<<<<<

# ================
# Remote desktop connection
# >>>>>>>>>>>>>>>>
# Get-ItemProperty -path "HKLM:\System\CurrentControlSet\Control\Terminal Server" | select fDenyTSConnections # view current state
# (gp "HKLM:\System\CurrentControlSet\Control\Terminal Server" ).fDenyTSConnections                           # same as above
# <Win+R>mstsc
# <<<<<<<<<<<<<<<<

# ================
# Get IP address
# >>>>>>>>>>>>>>>>
# Get-NetIPAddress # ps 3.0+
# [System.Net.Dns]::GetHostEntry( "" )
# <<<<<<<<<<<<<<<<

# ===============
# Clear DNS cache
# >>>>>>>>>>>>>>>>
# Clear-DNSClientCache # ps 4.0+
# ipconfig /flushdns
# <<<<<<<<<<<<<<<<

# ================
# Get powershell version
# >>>>>>>>>>>>>>>>
# $PSVersionTable.PSVersion
# Get-Host
# <<<<<<<<<<<<<<<<
#
# ================
# Get windows version
# >>>>>>>>>>>>>>>>
# [System.Environment]::OSVersion.VersionString
# <<<<<<<<<<<<<<<<

# ================
# Turn off windows firewall
# >>>>>>>>>>>>>>>>
# Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False # ps 3.0+
# netsh advfirewall set allprofiles state off
# <<<<<<<<<<<<<<<<

# ================
# Get active network connections
# >>>>>>>>>>>>>>>>
# Get-NetTCPConnection                  # list network connections on PS 5
# netstat -abno                         # works wit CMD also
# <<<<<<<<<<<<<<<<

# ================
# Other useful
# >>>>>>>>>>>>>>>>
# Test-Connection george-808                # Ping
# Test-Path variable:global:foo             # test if variable exist
# Remove-Item -Recurse -Force some_dir      # recursevily delete folder and its content
# [System.IO.Path]::GetFileName( "c:\path\to\file.txt" )
# [System.IO.Path]::GetDirectoryName( "c:\path\to\file.txt" )
# [System.IO.Path]::GetFileNameWithoutExtension( "c:\path\to\file.txt" )
# <<<<<<<<<<<<<<<<

# $username = "username"
# $password = ConvertTo-SecureString "password" -AsPlainText -Force
# $cred = new-object -typename System.Management.Automation.PSCredential -argumentlist $username, $password

#  _____________________________________
# //////////////////////////////////////
# WMI
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# ================
# WMI classes listings
# >>>>>>>>>>>>>>>>
# gwmi -namespace ROOT -class "__Namespace" | select name   # list namespaces
# gwmi -namespace ROOT\cimv2 -list | select name            # list classes inside namespace
# <<<<<<<<<<<<<<<<

# ================
# Set computer name
# >>>>>>>>>>>>>>>>
# $obj = gwmi Win32_ComputerSystem
# $obj.rename( "newName" );
# <<<<<<<<<<<<<<<<

# ================
# Disable/Enable network adapter
# >>>>>>>>>>>>>>>>
# $obj = gwmi Win32_NetworkAdapter -Filter "Name LIKE '%Intel%'";
# $obj.enable();
# $obj.disable();
# <<<<<<<<<<<<<<<<
#
# ================
# Display IP address
# >>>>>>>>>>>>>>>>
# gwmi -class "Win32_NetworkAdapterConfiguration" -Filter IPEnabled=TRUE -ComputerName .
# <<<<<<<<<<<<<<<<
#
# ================
# Display shares on host
# >>>>>>>>>>>>>>>>
# gwmi Win32_Share 
# <<<<<<<<<<<<<<<<
#
# ================
# Create shared folder
# >>>>>>>>>>>>>>>>
# $wmishare = [wmiclass]"Win32_Share"
# $wmishare.create( "D:\test", "test", 0)
# <<<<<<<<<<<<<<<<
# 
# ================
# Delete share
# >>>>>>>>>>>>>>>>
# gwmi Win32_Share | % { if( $_.name -eq "test" ) { $_.delete() } }
# <<<<<<<<<<<<<<<<

# ________________________________________________
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# FUNCTIONS
# /////////////////////////////////////////////////

function CopyBinary {
    param( [string]$src, [string]$dest )
    if( test-path $src ) {
        try {
            Copy-Item $src $dest -Force 2>&1| out-null
            # Write-host "Copyed:        $dest" 
        }
        catch {
            Write-host "FAILED to copy $dest" 
        }
    }
    else {
        Write-host "DOESN'T exist: $src"
    }
}


function BkUpnCopy {
  param( [string]$src, [string]$dest )

# Write-Host "$src, $dest" 	

  if( Test-Path $src ) {
      if( Test-Path $dest ) {
          #$curFileName = $( $("C:\docs\pa th1\pa th2\file name.ext" -split "\\")[-1] -split "\.") #"
          # TODO if( $src.LastWriteTime -le $dest.LastWriteTime ) continue
          $pathElements = $( $dest -split "\\")
          $curFileDir = $pathElements[0..$($pathElements.length - 2)] -join "\\"
          $curFileName = $( $pathElements[-1] -split "\.") #"
          $bkupFilePath = "{0}\\{1}_bak.{2}" -F $curFileDir, $curFileName[0], $curFileName[1]

          if( Test-Path $bkupFilePath ) {
              Remove-Item $dest
              # Copy-Item $src $dest | out-null
              CopyBinary $src $dest 
              Write-Host "===== delete $dest and COPY >>> $src"
          } else {
              Move-Item $dest $bkupFilePath
              Write-Host "===== move $dest TO >>> $bkupFilePath"
              # Copy-Item $src $dest | out-null
              CopyBinary $src $dest
              Write-Host "===== copy $src"
          }
      } else {
          # Copy-Item $src $dest | out-null 
          CopyBinary $src $dest
          Write-Host "===== copy $src"
      }
  } else {
      Write-Host "NOT EXIST: $src "
  }
}

function MkDirIfNotExist {
    param( [string]$path )
    if( -not ( test-path $path  ) ) { 
        try {
            New-Item -Path $path -ItemType Container | out-null
            write-host "Created:       $path" 
        }
        catch { 
            write-host "FAILED to create $path" 
        }
    }
}

function MakeRemoteDisk {
    param( [string]$RemoteDir, [string]$DiskLetter )

    New-PSDrive -Name $DiskLetter -Root $RemoteDir -PSProvider FileSystem -Scope Global -ErrorAction SilentlyContinue;

    if( Test-Path $RemoteDir ) { return; }

    write-host "with map network drive: "
    $drive = new-object -COMObject WScript.Network
    $drive.MapNetworkDrive( "${Diskletter}:", $RemoteDir );

    if( Test-Path $RemoteDir ) { return; }

    $RemoteUserName = "GEORGE-808\Username"
    $RemoteUserPwd = "password"

    Write-Host "net use `"${DiskLetter}:`" `"$RemoteDir`" /user:$RemoteUserName $RemoteUserPwd /p:yes"
    cmd /c "net use `"${DiskLetter}:`" `"$RemoteDir`" /user:$RemoteUserName $RemoteUserPwd /p:yes";
}

function SetEnv {
    param( [string]$VarName, [string]$VarValue, [switch]$Force )

    if( [System.Environment]::GetEnvironmentVariable( $VarName, "User" ) -eq $null -or $Force )
    {
        [System.Environment]::SetEnvironmentVariable( $VarName, $VarValue, "User" )
    }
}

function CreateShortcut {
    param( [string]$Target, [string]$Location = "$home\Desktop\NewShortcut.lnk")
    $WshShell = new-object -COMObject WScript.Shell;
    $ShCut = $WshShell.CreateShortcut($Location);
    $ShCut.TargetPath = $Target;
    $ShCut.Save();
}

function wgrep {
    param( [string]$path, [string]$filetype, [string]$pattern )
    Get-ChildItem $path -Include $filetype -Recurse | Select-String -Pattern $pattern
}

function mBoxOkCancel( $x ) { 
    [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") | Out-Null
    [System.Windows.Forms.DialogResult]$res = [System.Windows.Forms.MessageBox]::Show( $x, "Done!",
                            [System.Windows.Forms.MessageBoxButtons]::OK,
                            [System.Windows.Forms.MessageBoxIcon]::Information, 
                            [System.Windows.Forms.MessageBoxDefaultButton]::Button1 )

    return $res.ToString();
}
# Add-Type @"
#     using System;
#     using System.Runtime.InteropServices;
#      
#     namespace mklink
#     {
#         public class symlink
#         {
#             [DllImport("kernel32.dll")]
#             public static extern bool CreateSymbolicLink(string lpSymlinkFileName, string lpTargetFileName, int dwFlags);
#         }
#     }
# "@

# Usage:
# [mklink.symlink]::CreateSymbolicLink('C:\Users\Administrator\Desktop\SQL2008Install', "\\dc1\SharedStorage\SQL 2008", 1)

function AddRegistryValueData {
    param( [string]$regPath, [string]$valueName, [string]$valueData, [string]$dataType )
    $allowedDataTypes = @('String','ExpandString','Binary','DWord','MultiString','QWord','Unknown');
    $found = $false;
    foreach( $dt in $allowedDataTypes ) {
        if( $dt -match $dataType ) {
            $found = $true;
            break;
        }
    }

    if( -not $found ) {
        write "Not allowed datatype"
        return; 
    }

    if( Test-Path $regPath ) {
        Get-ItemProperty -Path $regPath -Name $valueName -ErrorAction SilentlyContinue
        if( $? -eq $true ) {
            Set-ItemProperty -Path $regPath -Name $valueName -Value $valueData
        }
        else {
            New-ItemProperty -Path $regPath -Name $valueName -Value $valueData -PropertyType $dataType
        }
    }
    else {
        New-Item $regPath
        New-ItemProperty -Path $regPath -Name $valueName -Value $valueData -PropertyType $dataType
    }
}

