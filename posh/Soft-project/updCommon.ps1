# 
$SrcRoot = "S:"
$SrcDir = "$SrcRoot\Confi"


$DLVIDir = "C:\progDir\subdir"

[string[][]]$filesList = @(@());

function MyStopService {
    param( [string]$serviceName )
    # if( $( Get-Service | ? { $_.name -like "*vicore*" } ).Status -eq "Running" ) 
    if( $( Get-Service $serviceName ).Status -eq "Running" ) 
    { 
        Write-Host "Service $serviceName is running, trying to stop"
        # Get-Service | ? { $_.name -like "*vicore*" } | Stop-Service
        Stop-Service $serviceName -erroraction SilentlyContinue
        if( -not $? ) {
            Write-host "Failed to stop the service! Exit";
            exit;
        }
    }
    else { Write-Host "Service $serviceName is not running" } 
} 


. .\functions.ps1
if( -not (Test-Path $SrcDir) ) {
    MakeRemoteDisk "\\GEORGE-922\Shared" $($SrcRoot.Chars(0))
}
Start-Sleep 7

# __________________________
# \\\\\\\\\\\\\\\\\\\\\\\\\\\
# Check host
# ///////////////////////////
#
$features = @( $( (Get-Service "Service One" -ErrorAction SilentlyContinue ) -ne $null )
             , $( (Get-Service "Service Two" -ErrorAction SilentlyContinue ) -ne $null )
             , $( (Get-Service "Service Three" -ErrorAction SilentlyContinue ) -ne $null ) )

if( $features[0] -and -not ($features[1] -or $features[2]) ) {
    write-host "Current host is of type one"
    $SrcVCAgentDir = "$SrcDir\_DirWithFiles"
    $serviceName = "Service One"

    $filesList = @(
                ("$SrcVCAgentDir\someExecutableBinaryName.exe",$DLVIDir)
                );
    # kill a process
    #Get-Process | ? { $_.processName -like "*vcenteragentservice*" } | Stop-Process 
    Stop-Process -Name "ServiceOneProcName" -ErrorAction SilentlyContinue;
    if( -not $? ) {
        write-host "Cannot stop process ServiceOneProcName; Exiting"
        exit;
    }
}
elseif( $features[1] -and -not ($features[0] -or $features[2]) ) {
    Write-Host "Current host is of type two"
    $SrcCoreDir = "$SrcDir\_dirWithFilesFOrTypeTwo"
    $SrcMiscDir = "$SrcDir\_dirWithFilesFOrTypeTwoTwo"
    $serviceName = "ServiceNameTwo"
    $filesList = @( 
                ("$SrcCoreDir\SomeExecutableBinaryName.exe", $DLVIDir)
                );
    # stop service
    MyStopService $serviceName;

    # close console 
    $SscVi = Get-Process "ConsoleForServiceTwo" -ErrorAction SilentlyContinue;
    if( $? ) {
        Write-Host "`r`nConsole is working. Closing window`r`n"
        $SscVi.CloseMainWindow() | Out-Null;
        Start-Sleep 2;
    }
}
elseif( $features[2] -and -not ($features[0] -or $features[1]) ) {
    Write-Host "Current host is Of type three server"
    $serviceName = "ServiceThree"
    $SrcHVAgentDir = "$SrcDir\_filesForServiceThree"

    $filesList = @(
        ("$SrcHVAgentDir\SomeExecutableFileName.exe",$DLVIDir)
        )
    MyStopService $serviceName;
}
else {
    Write-Host "Error! Cannot determine type of current host! Exiting"
    exit;
}

######################
# ACTION!
######################

Get-Date

foreach( $el in $filesList ) {
    BkUpnCopy $el[0] $el[1] 
}

# if( $( Get-Service | ? { $_.name -like "*vcenteragent*" } ).Status -eq "Running" ) 
if( $( Get-Service $serviceName ).Status -eq "Running" ) { 
    Write-Host "WTF?!? service is running?!?!?" 
}
else { 
    #Start-Service $serviceName ;
    Get-Service $serviceName ;
    #Write-Host "Service $serviceName Started" 
} 

