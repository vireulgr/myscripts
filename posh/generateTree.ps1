$dirTemplate = "folder{0}"

$itemName = "name{0}" -f ($index).toString("000")
New-Item -name $itemName -type "file"

# empty folder "de"
$itemName = $dirTemplate -f ($index).toString("000")
New-Item -name $itemName -type "directory"
# folder with files only "df"
# folder with folders only "dd"
# folder with files and folders "db"



function createStructure {

    param( [string]$nameTemplate, [string]$index, [string]$type )

    # switch( $type ) {
    #   "de" { }
    #   "df" { }
    #   "dd" { }
    #   "db" { }
    # }

    if( $type = 'de' ) { # create current directory only
        $itemName = $nameTemplate -f ($index).PadLeft(3,"0")
        New-Item -name $itemName -type "directory"
    }
    elif ( $type = 'df' ) {
        $itemName = $nameTemplate -f ($index).PadLeft(3,"0")
        New-Item -name $itemName -type "directory"

        for( $index=0; $index -lt 3; ++$index ) {
            $itemName = $nameTemplate -f ($index).PadLeft(3,"0")
            New-Item -name $itemName -type "directory"
        }
    }
    elif ( $type = 'dd' ) {
        $itemName = $nameTemplate -f ($index).PadLeft(3,"0")
        New-Item -name $itemName -type "directory"
    }
    elif ( $type = 'db' ) {
        $itemName = $nameTemplate -f ($index).PadLeft(3,"0")
        New-Item -name $itemName -type "directory"
    }

}

# example use
# createFolders -parentDir = "D:\test" -nameTemplate = "folder" -num = 3
# createFiles -parentDir = "D:\test" -nameTemplate = "folder" 
# createObjects -parentDir = "D:\test" -nameTemplate = "folder" -type = "directory" -num = 5

function createFolders {

    param( [string]$parentDir, [string]$nameTemplate, [int]$num )

    for( $index=0; $index -lt $num; ++$index ) {
        $itemName = $nameTemplate -f ($index).PadLeft(3,"0")
        New-Item -name $itemName -type "directory"
    }
}

function createFiles {

    param( [string]$parentDir, [string]$nameTemplate, [int]$num )

    for( $index=0; $index -lt $num; ++$index ) {
        $itemName = $nameTemplate -f ($index).PadLeft(3,"0")
        New-Item -name $itemName -type "directory"
    }
}

function createObjects {
    param( [string]$parentDir, [string]$nameTemplate, [string]$type, [int]$num )

    for( $index=0; $index -lt $num; ++$index ) {
        $itemName = $nameTemplate -f ($index).PadLeft(3,"0")
        New-Item -name $itemName -type $type
    }
}
