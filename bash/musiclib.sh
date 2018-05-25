files_dir="${HOME}/muzlib"
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

	FileName=$(basename $1)

	if [ -f "${files_dir}/${FileName}" ]; then
		echo "[W] File exists, would you save current file with another name?"
		echo "TODO implement"
	
	else
		# cp $1 $files_dir
		echo "Adding file cp $1 $files_dir"
	fi
}

function addText() {

	FileName=$(basename $1)
	if [ -f "${files_dir}/${FileName}.txt" ]; then
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
}

function getFile() {
	echo "get file"
}

function searchSong() {
	find ./files -name "$1"
}

function searchText() {
	grep -Ri -e "$1"
}

function journal() {
	# 1 - action 2 - file
	printf "%s %s %s %s\n" $(whoami) $1 $2 $(date +"%s") >> $history_file
}

function setBackup() {
	echo "get file"
}

function doBackup() {
	echo "get file"
}

function printUsage() {
	echo "Usage: musiclib.sh [--add|--get|--del] & so on"
}

#######
# ENtry point
#######

if [ $# -lt 2 ]; then
	printUsage
fi

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
	;;
	--search-text)
	;;
	--set-backup)
	;;
	--do-backup)
	;;
	*)
	printUsage
	;;
esac