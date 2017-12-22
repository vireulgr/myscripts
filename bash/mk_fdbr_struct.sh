#!/bin/bash

CUR_DIR="./temp"
mkdir -p "${CUR_DIR}/file_db_root"

NODES_QTY='2'
for (( c=0; c < NODES_QTY ; c++ )); do
    DIR=$( printf "%s/file_db_root/%03d" "${CUR_DIR}" "$c" )
    mkdir -p  "${DIR}/tasks"
done;

NODES_TASKS=$( find ./ -mindepth 2 -maxdepth 4 -path '*tasks*' -type d )

SESS_NR='5'
for cnt in {1..6}; do

    for (( c=0; c < NODES_QTY ; c++ )); do

        DIR=$( printf "%s/file_db_root/%03d/tasks/%d" "${CUR_DIR}" "$c" "$(( cnt + 200 ))" )
        mkdir -p  "${DIR}"

        echo "<?xml?>"      > "${DIR}/${SESS_NR}.xml"
        echo "shaverma"     > "${DIR}/shaverma.ext"
        echo "some_file"    > "${DIR}/some_file_${cnt}"

        if [ ${c} -eq '0' ]; then 
            echo "<?xml2?>" > "${DIR}/${SESS_NR}_IM.xml"
            echo "<?xml3?>" > "${DIR}/${SESS_NR}_MAIL.xml"
            echo "<?xml4?>" > "${DIR}/${SESS_NR}_WEB.xml"
            echo "<?xml5?>" > "${DIR}/report.xml"
        fi 
    done;
done;

#7z a -r -l -tzip $zip_file_name "${nodeit_second}/report.xml"

