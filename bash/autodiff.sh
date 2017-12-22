#!/bin/bash

function ensure_unique
{
    # printf "inside ensure unique::script name: %s\n" "$1"
    res=$(ps ax | grep "$1" | wc -l)
    return "$(( res - 1 ))"
}

# printf "ensure unique: %d \n" "$(ensure_unique \"$0\")"

. /root/functions.sh

HOME="/root"

# папка для хранения diff
DIFFS_DIR="${HOME}/autodiffs"
# префикс в имени файла diff
DIFFS_PREFIX="autodiff"
# папка для архивирования старых diff
ARCHIVE_DIR="${DIFFS_DIR}/arch"

printf "================ Autodiff script @ %s ===============\n" "$(date +%c)"

[ ! -d "$DIFFS_DIR" ] || mkdir -p "$DIFFS_DIR" ||  err_exit "Can not create diffs directory!"

[ ! -d "$ARCHIVE_DIR" ] || mkdir -p "$ARCHIVE_DIR" || err_exit "Can not create archive directory!"

# где код
[ -z "$1" ] && DEVEL_PATH="/SQL/wcs/trunk" || DEVEL_PATH="$1"

if [ ! -d ${DEVEL_PATH} ]
then
    printf "Wrong path: %s\n" "${DEVEL_PATH}"
    exit 1
fi

# забэкапить diff старше 2х недель
find "${DIFFS_DIR}" -maxdepth 1 -name "${DIFFS_PREFIX}_*.patch" -type f -mtime +14 -exec mv -t ${ARCHIVE_DIR} {} + 

# придумать имя для нового diff
DIFF_NAME="${DIFFS_PREFIX}_$(date +%d-%m-%y_%H%M%S).patch"

# перейти в директорию с рабочей копией репозитория
pushd "$DEVEL_PATH"

# сделать diff и сохранить в новый файл, если ошибка - нафик
printf "Saving diff to %s\n" "${DIFFS_DIR}/${DIFF_NAME}"
svn diff > "${DIFFS_DIR}/${DIFF_NAME}" || err_exit "Can't do svn diff"

if [ $(du -bs "${DIFFS_DIR}/${DIFF_NAME}" | cut -f1) -eq 0 ]
then
    printf "Diff size equals 0. Deleting %s\n" "${DIFFS_DIR}/${DIFF_NAME}"
    rm -f "${DIFFS_DIR}/${DIFF_NAME}" 
fi

# обновить рабочую копию, если ошибка - нафик
printf "Updating working copy\n"
svn update --accept theirs-full --quiet || err_exit "Can't do svn update"

# обновить базу данных cscope
cscope -Rbq

# остановить прожорливые сервисы
printf "Stopping services\n"
service sniffer stop >/dev/null; service db_agent_total stop >/dev/null; service db_agent stop >/dev/null

printf "Executing make clean\n"
make clean

#сделать
printf "Making all\n"
BUILD_TIME=$SECONDS
if ! make -j4 -k all 1>/dev/null
then
    printf "======================================== WARNING!!!! ========================================\n"
    printf "There were problems during build. Try to build working copy and update nodes independently...\n"
    printf "=============================================================================================\n"
    err_exit "Errors during build"
fi
BUILD_TIME=$(( SECONDS - BUILD_TIME ))
printf "Build WITHOUT distcc took %s \n" "$(print_time_nice $BUILD_TIME)"

# запустить сервисы
printf "Starting services\n"
service sniffer start > /dev/null
service db_agent_total start >/dev/null; service db_agent start >/dev/null

printf "Updating nodes\n"
. ${HOME}/update_nodes.sh

popd

printf "Autodiff done\n"

