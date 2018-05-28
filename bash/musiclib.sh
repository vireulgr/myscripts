#!/bin/bash

files_dir="${HOME}/muzlib"
texts_dir="${files_dir}/texts"
backup_dir="${HOME}/muzbackup"
history_file="${files_dir}/history"

#######
# FUNCTIONS
#######
function addFile() {
    # 1 - filename
    if [ ! -f $1 ]; then
        echo "[E] file $1 not exists or is not a regular file!"
        return
    fi
    # check extension
    fileMime=$(file -b --mime-type $1)
    if [[ ! 'audio/mpeg audio/x-flac audio/x-wav' =~ $fileMime ]]; then 
        echo "[E] file $1 is $fileMime and cannot be put in library"
        return
    fi
    # check size
    fileSize=$(du -s $1 | cut -f1)
    if [ $fileSize -gt 10240 ]; then
        echo "[E] file $1 is $fileSize Kb is too large!"
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
            return;
        fi
    done
    
    cp $1 $newName
    echo "File $1 was added as $newName"
    
}


function addText() {

    newFile="${files_dir}/$(basename $1).txt"
    if [ -f "$newFile" ]; then
        echo "[W] File exists, want to overwrite current file?"
        echo "TODO implement"
    
    else
        # cp $1 $files_dir
        echo "Adding file cp $1 $files_dir"
    fi

    echo "Please enter song text; stop-word is 'end_of_song'"
    temp='';
    line='';
    while [ "$line" != "end_of_song" ]; do
        temp="$temp\r\n$line"   
        read line
    done
    echo "$temp" > $newFile

    echo "Text to file $1 was added as $newFile"
}

function getFile() {
    # 1 - filename
    FileName=$(basename $1)

    if [ ! -f "${files_dir}/${FileName}" ]; then
        echo "[E] File $FileName is not exists in library"
        return;
    else
        cp $1 .
    fi
}

function searchSong() {
    # $1 - quoted pattern
    find "$files_dir" -name "$1"
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
    tar czf "$backup_dir/bkup_$(date +%d%m%y_%s).tar.gz" "$files_dir"
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
		
		--add-text
		
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
    addFile "$2"
    journal "$1" "$2"
    ;;
    --get)
    getFile "$2"
    journal "$1" "$2"
    ;;
    --del)
    deleteFile "$2"
    journal "$1" "$2"
    ;;
    --add-text)
    addText "$2"
    ;;
    --search-song)
    searchSong "$1"
    ;;
    --search-text)
    searchText "$1"
    ;;
    --unset-backup)
    unsetBackup
    ;;
    --set-backup)
    setBackup
    ;;
    --do-backup)
    doBackup
    ;;
    --setup)
    doSetup
    ;;
    *)
    printUsage
    ;;
esac
