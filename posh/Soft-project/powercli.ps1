<# 
Скрипт для первоначальной настройки vSphere. 

Запускается из консоли администратора PowerShell, требует установки PowerCLI
https://code.vmware.com/web/dp/tool/vmware-powercli/6.5

Установка PowerCLI из бинаря (лежит на шаре)
\\192.168.0.162\soft\virtual (VMware)\VMware-PowerCLI-6.3.0-3737840.exe

Установка PowerCLI из галереи PowerShell для версии PowerShell >= 5.0 (в Win10 эта версия по умолчанию) 
https://blogs.vmware.com/PowerCLI/2017/04/powercli-install-process-powershell-gallery.html
https://www.powershellgallery.com/packages/VMware.PowerCLI/6.5.1.5377412

Скрипт добавляет в чистый vCenter один Datacenter, один хост и одну ВМ на хосте.
На хосте также настраивается время и настраивается дамп корок в файл с именем MyDumpFile
(какой конкретно файл можно узнать командой esxcli system coredump file list)
Скрипт можно запускать с удалённой машины, у которой есть сетевой доступ до сервера vCenter.
Параметры в переменных, думаю, из названия понятно какой в них смысл. 
Для более подробных сведений см. руководства по PowerShell и PowerCLI или в консоли help <имя команды>
Необходимо убедиться что на vCetner отключены МЭ
#>

################################################
# SETTINGS
################################################

$netDomain  = "domain.local"
$vCenterName = "ws8x64"

$vCenterUserName   = "administrator"
$vCenterUserDomain = "vsphere.local"
$vCenterUserPwd    = "1234"

$esxiName2    = "esxi62"
$esxiName1    = "esxi61"

$hostUserName = "root"
$hostUserPwd  = "3124"

$datacenterName = "DatacenterOne"

$vmName1 = "NewVm1"
$vmName2 = "NewVm2"
$vmName3 = "NewVm3"
$vmName4 = "NewVm4"

################################################
# FUNCTIONS
################################################
function MakeCredential {
    param( [string]$userDomainName, [string]$userPwdText )
    $pwdEnc = ConvertTo-SecureString -AsPlainText $userPwdText -Force;
    $psCred = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $userDomainName,$pwdEnc
    return  $psCred;
}

function SetupHost {
    param( [string]$hostName <#, [string]$hostDomain, [System.Management.Automation.PSCredential]$hostCred#> )

    # NEED TO RENAME DATASTORE IN ORDER TO MAKE SCRIPT WORK!!!!!!
    #esxcli storage filesystem unmount -l esx61DL

    # Connect-ViServer "$esxiName.$netDomain" -Credential $hostCred
    #$esxcli = Get-EsxCli
    # Time setup
    $esxcli = Get-EsxCli -VmHost $hostName
    $currentTime = Get-Date
    $esxcli.system.time.set( $currentTime.day, $currentTime.hour, $currentTime.minute,
                             $currentTime.month, $currentTime.second, $currentTime.year );

    # CoreDump settings
    $esxcli.system.coredump.file.add( $null, "DS$hostName", $null, "MyDumpFile" );
    $corePath = ( $esxcli.system.coredump.file.list( ) | Select -last 1 ).Path
    $esxcli.system.coredump.file.set( $null, $corePath );
    $esxcli.system.coredump.file.add( 1 );
}

# Add host
function SimpleAddHost {
    param( [string]$hostName, [string]$hostDomain, [string]$datacenterName, [System.Management.Automation.PSCredential]$hostCred )

    Get-VmHost $hostName -ErrorAction SilentlyContinue
    if( $? -eq $false ) {
        # Add host
        Add-VMHost -Name "$hostName.$hostDomain" -Location $datacenterName -Credential $hostCred -Force -Confirm:$false
        if( $? -eq $false ) { 
            Write "Error adding host $hostName on $datacenterName";
            return; 
        }
    }
    else {
        Write-Host "Host $hostName is already exist in vCenter inventory";
    }
}
# Create VM
function SimpleCreateVM {
    param( [string]$vmName, [string]$hostName )

    Get-Vm -Name $vmName -ErrorAction SilentlyContinue
    if( $? -eq $false ) {
        New-Vm -Name $vmName -VmHost $hostName -Datastore "DS$hostName" -DiskGb 15 -DiskStorageFormat Thin -MemoryGb 0.5 -GuestId 'rhel6_64Guest'
        if( $? -eq $false ) { 
            Write "Error creating VM $vmName on host $hostName";
            return; 
        }
    }
    else {
        Write-Host "VM $vmName is already exist on host $hostName";
    }
}

################################################
# ENTRY POINT
################################################

# Make credential
$vCenterCred    = MakeCredential  "$vCenterUserDomain\$vCenterUserName" $vCenterUserPwd
$hostCred       = MakeCredential  $hostUserName $hostUserPwd

Connect-ViServer "$vCenterName.$netDomain" -Credential $vCenterCred -ErrorAction Stop
# if( $? -eq $false ) { exit; }

Get-DataCenter $datacenterName -ErrorAction SilentlyContinue
if( $? -eq $false ) {
    # Create datacenter
    $datacenter = New-DataCenter -Location (Get-Folder -NoRecursion) -Name $datacenterName -ErrorAction Stop
    #if( $? -eq $false ) { exit; }
}

# host 1
SimpleAddHost $esxiName1 $netDomain $datacenterName $hostCred
SetupHost $esxiName1
SimpleCreateVM $vmName1 $esxiName1
SimpleCreateVM $vmName2 $esxiName1

# host 2
SimpleAddHost $esxiName2 $netDomain $datacenterName $hostCred
SetupHost $esxiName2
SimpleCreateVM $vmName3 $esxiName2
SimpleCreateVM $vmName4 $esxiName2

# Get-VmHost $esxiName -ErrorAction SilentlyContinue
# if( $? -eq $false ) {
#     # Add host
#     Add-VMHost -Name "$esxiName.$netDomain" -Location $datacenterName -Credential $hostCred -Force -Confirm:$false
#     if( $? -eq $false ) { exit; }
# }
# 
# Get-Vm -Name "$($vmName)1" -ErrorAction SilentlyContinue
# if( $? -eq $false ) {
#     # Create VM
#     New-Vm -Name "$($vmName)1" -VmHost $esxiName -Datastore "datastore1" -DiskGb 15 -DiskStorageFormat Thin -MemoryGb 0.5 -GuestId 'rhel6_64Guest'
#     if( $? -eq $false ) { exit; }
# }

# $esxcli = Get-EsxCli -VmHost $esxiName
# $currentTime = get-date
# $esxcli.system.time.set( $currentTime.day, $currentTime.hour, $currentTime.minute,
#                          $currentTime.month, $currentTime.second, $currentTime.year )
# 
# # Connect-ViServer "$esxiName.$netDomain" -User $hostUserName -Password $hostUserPwd
# # $esxcli = Get-EsxCli
# 
# # CoreDump settings
# $esxcli.system.coredump.file.add( $null, "datastore1", $null, "MyDumpFile" )
# $corePath = ( $esxcli.system.coredump.file.list( ) | select -last 1 ).Path
# $esxcli.system.coredump.file.set( $null, $corePath )
# $esxcli.system.coredump.file.add( 1 )

Disconnect-ViServer -Force -Confirm:$false

Write-host "Done"
Start-Sleep 2

