#!/bin/bash

files_dir="${HOME}/muzlib"
texts_dir="${files_dir}/texts"
backup_dir="${HOME}/muzbackup"
history_file="${files_dir}/history"

g_wasCmdCmpl=0

#######
# FUNCTIONS
#######
function addFile() {
    # 1 - filename
    if [ ! -f $1 ]; then
        echo "[E] file $1 not exists or is not a regular file!"
        g_wasCmdCmpl=0
        return
    fi
    # check extension
    fileMime=$(file -b --mime-type $1)
    if [[ ! 'audio/mpeg audio/x-flac audio/x-wav' =~ $fileMime ]]; then 
        echo "[E] file $1 is $fileMime and cannot be put in library"
        g_wasCmdCmpl=0
        return
    fi
    # check size
    fileSize=$(du -s $1 | cut -f1)
    if [ $fileSize -gt 10240 ]; then
        echo "[E] file $1 is $fileSize Kb is too large!"
        g_wasCmdCmpl=0
        return
    fi

    newName="${files_dir}/$(basename $1)" 

    while [ -f "$newName" ]; do
        echo "[W] File $newName exists in the library"
        ans=''
        read -p "Do you want to save this file with a different name? " ans

        if [[ $ans =~ ^[Yy]$ ]]; then
            ans=''
            read -p "Enter new name: " ans
            newName="${files_dir}/$ans"
        else
            g_wasCmdCmpl=0
            return;
        fi
    done
    
    cp $1 $newName
    echo "File $1 was added as $newName"
    g_wasCmdCmpl=1
}

function deleteFile() {
    songFile="${files_dir}/$(basename $1)" 

    if [ ! -f "$songFile" ]; then
        echo "[E] File $FileName is not exists in library"
        g_wasCmdCmpl=0
        return;
    fi
    
    ans=''

    read -p "Do you want to delete file $songFile" ans

    if [[ ! $ans =~ ^[Yy]$ ]]; then
        g_wasCmdCmpl=0
        return
    fi

    textFile="${texts_dir}/$(basename $1).txt"

    if [ -f "$textFile" ]; then
        rm $textFile
    fi

    rm $songFile

    g_wasCmdCmpl=1
}

function getFile() {
    # 1 - filename
    fileName=$(basename $1)

    if [ ! -f "${files_dir}/${fileName}" ]; then
        echo "[E] File $fileName is not exists in library"
        return;
        g_wasCmdCmpl=0
    fi

    cp "${files_dir}/${fileName}" .

    echo "File $fileName was copied in current directory"

    g_wasCmdCmpl=1
}

function addText() {

    if [ ! -f "${files_dir}/$(basename $1)" ]; then
        echo "[E] File $FileName is not exists in library"
        g_wasCmdCmpl=0
        return;
    fi

    newFile="${texts_dir}/$(basename $1).txt"

    if [ -f "$newFile" ]; then
        echo "[W] File $newFile exists in library"
        ans=''
        read -p "Do you want to overwrite current file? " ans

        if [[ ! $ans =~ ^[Yy]$ ]]; then
            return;
            g_wasCmdCmpl=0
        fi
    fi

    echo "Please enter song text; stop-word is 'end_of_song'"
    temp='';
    line='';
    read line
    while [ "$line" != "end_of_song" ]; do
        temp="$temp\r\n$line"   
        read line
    done
    echo -n -e "$temp" > $newFile

    echo "Text to file $1 was added as $newFile"
    g_wasCmdCmpl=1
}


function searchSong() {
    # $1 - quoted pattern
    # pushd "$files_dir" > /dev/null 2>&1
    # find . -maxdepth 1 -name "*$1*" -printf "%f\n"
    # popd > /dev/null 2>&1

    find "$files_dir"  -maxdepth 1 -name "*$1*" -printf "%f\n"
}

function searchText() {
    # $1 - quoted pattern
    grep -Ri -e "$1" "$texts_dir"
}

function journal() {
    # 1 - action 2 - file
    printf "%s %s %s %s\n" $(whoami) $1 $2 $(date +"%s") >> $history_file
}

function setBackup() {
    ( crontab -u $(whoami) -l | echo "0 12 1 * * $0 --do-backup" ) | crontab -u $(whoami) -
    echo "Cron task added"
}

function unsetBackup() {
    crontab -u $(whoami) -l | grep -v "$0" | crontab -u $(whoami) -
    echo "Cron task removed"
}

function doBackup() {
    pushd "$files_dir" > /dev/null 2>&1
    tar czf "$backup_dir/bkup_$(date +%d%m%y_%s).tar.gz" .
    popd > /dev/null 2>&1
    echo "Backup is done"
}

function doSetup() {
    if [ ! -d "$files_dir" ]; then
        mkdir $files_dir
    fi
    if [ ! -d "$backup_dir" ]; then
        mkdir $backup_dir
    fi
    if [ ! -d "$texts_dir" ]; then
        mkdir $texts_dir
    fi
    if [ ! -f "$history_file" ]; then
        touch $history_file
    fi
    echo "Setup is done"
}

function printUsage() {

    cat <<-HEREDOC

		Usage: musiclib.sh [operation with params]
		
		--setup
		
		--add-text <song name>
		
		File operations
		--add <file>
		--get <file>
		--del <file>
		
		Search
		--search-text <pattern>
		--search-song <pattern>
		
		Backup
		--do-backup
		--set-backup
		--unset-bacup
HEREDOC

}

#######
# ENtry point
#######
case $1 in
    --add)
        if [ $# -lt 2 ]; then
            printUsage
            exit
        fi
        if [ ! -d "$files_dir" ]; then
            echo "$files_dir is not present. Maybe you need to do --setup"
        fi
        addFile "$2"
        if [ "$g_wasCmdCmpl" -gt 0 ]; then
            journal "$1" "$2"
        fi
    ;;

    --get)
        if [ $# -lt 2 ]; then
            printUsage
            exit
        fi
        if [ ! -d "$files_dir" ]; then
            echo "$files_dir is not present. Maybe you need to do --setup"
        fi
        getFile "$2"
        if [ "$g_wasCmdCmpl" -gt 0 ]; then
            journal "$1" "$2"
        fi
    ;;

    --del)
        if [ $# -lt 2 ]; then
            printUsage
            exit
        fi
        if [ ! -d "$files_dir" ]; then
            echo "Directory $files_dir is not present. Maybe you need to do --setup?"
        fi
        deleteFile "$2"
        if [ "$g_wasCmdCmpl" -gt 0 ]; then
            journal "$1" "$2"
        fi
    ;;

    --add-text)
        if [ $# -lt 2 ]; then
            printUsage
            exit
        fi
        if [ ! -d "$files_dir" ]; then
            echo "$files_dir is not present. Maybe you need to do --setup"
        fi
        if [ ! -d "$texts_dir" ]; then
            echo "$texts_dir is not present. Maybe you need to do --setup"
        fi
        addText "$2"
    ;;

    --search-song)
        if [ $# -lt 2 ]; then
            printUsage
            exit
        fi
        if [ ! -d "$files_dir" ]; then
            echo "$files_dir is not present. Maybe you need to do --setup"
        fi
        searchSong "$2"
    ;;

    --search-text)
        if [ $# -lt 2 ]; then
            printUsage
            exit
        fi
        if [ ! -d "$texts_dir" ]; then
            echo "$texts_dir is not present. Maybe you need to do --setup"
        fi
        searchText "$2"
    ;;

    --unset-backup)
        unsetBackup
    ;;

    --set-backup)
        if [ ! -d "$files_dir" ]; then
            echo "$files_dir is not present. Maybe you need to do --setup"
        fi
        if [ ! -d "$backup_dir" ]; then
            echo "$backup_dir is not present. Maybe you need to do --setup"
        fi
        setBackup
    ;;

    --do-backup)
        if [ ! -d "$files_dir" ]; then
            echo "$files_dir is not present. Maybe you need to do --setup"
        fi
        if [ ! -d "$backup_dir" ]; then
            echo "$backup_dir is not present. Maybe you need to do --setup"
        fi
        doBackup
    ;;

    --setup)
        doSetup
    ;;

    *)
        printUsage
    ;;
esac
