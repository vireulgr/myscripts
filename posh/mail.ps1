# Script for automatically process email stability reports

# Stability folder name
$FolderName = 'Stability'

# DTB mail patterns: 
$DTBLogPathPat = '//server-name/stability'

# Elvis mail patterns
$ElvisLogTicketPat = 'Ticket:'

# date from which mails need to analyze
$dateString = $(Get-Date -UFormat '%Y-%m-%d 00:00:00')

$dlLogFile = 'f:\prog\posh\dl_log_file.ps1'

## ======================================================
## Getting needed log archives and Elvis ticket numbers
## ======================================================

# getting mails from outlook
Add-type -assembly "Microsoft.Office.Interop.Outlook"
$OutlookApp = New-Object -comobject Outlook.Application
$namespace = $OutlookApp.GetNameSpace( "MAPI" )
# Get only mail, that received not later than the dateString
$StabilityMail = $( $namespace.Folders.Item(1).Folders.Item('Inbox').Folders.Item($FolderName).Items | ? { $_.ReceivedTime -gt $dateString } )

#write "stab mail len: $($StabilityMail.length)"

# DTB mails processing
$DTBLogs = $StabilityMail | ? { $_.Subject -match 'Analysis completion mail' }

[string[]]$logNames = @();

#write 'dtb len: ', $($dtblogs).length

if ( $DTBLogs ) {
    ForEach ( $mail in $DTBLogs ) {

        $patt =  ".*($DTBLogPathPat/[^ ]+) completed.*"
        #$patt = "^.*($DTBLogPathPat/[^ ]+) completed.*$"
        #$($mail.Body.Split("`n")) | % { 
        #    if( $_ -match $DTBLogPathPat ) { 
        #        [string[]]$logNames += $( $_ -replace $patt,'$1' ) 
        #    } 
        #}
        $mail.Body -match 'Fatal:[\t ]*(\d+)' | Out-null
        $numFatals = $($matches[1])
        #write-host "fatals: $numFatals"
        if( $mail.Body -match $patt -and $numFatals -gt 0 ) {
            [string[]]$logNames += $($matches[1])
        }
    } 

    $logNames | get-unique
}

[int[]]$ticketNumbers = @();

# Elvis ticket mails processing
$ElvisLogs = $StabilityMail | ? { $_.Subject -match "*subj*" }

if ( $ElvisLogs ) {
    ForEach ( $mail in $ElvisLogs ) {

        $patt =  "^.*$LogTicketPat[\t ]?(\d+).*$"
        [int[]]$ticketNumbers += $( $mail.Subject -replace $patt,'$1' ) 
    }

    $ticketNumbers | get-unique
}
else {
    write 'elvis ticket numbers not found'
}

# for message box
#Add-type -assemblyName System.Windows.Forms
#
#$result = [System.Windows.Forms.MessageBox]::Show( 'Mail analyze', 'Caption', [System.Windows.Forms.MessageBoxButtons]::OK,
#                                                        [System.Windows.Forms.MessageBoxIcon]::Information,    
#                                                        [System.Windows.Forms.MessageBoxDefaultButton]::Button1,
#                                                        [System.Windows.Forms.MessageBoxOptions]::ServiceNotification )

## ======================================================
## Downloading DTB log archives to local directory
## ======================================================

ForEach( $log in $logNames ) {
    #            log name                  year                 weekNumber
    & $dllogFile $(split-path -leaf $log ) $log.split('/')[-3]  $( $log.split('/')[-2] -replace "CW","" )
}

