#!/bin/bash

INSTALL_PATH='/opt'
DEVEL_PATH='/SQL/wcs/trunk'

# TODO: время сравнивать с db_agent
TIMESTAMP_FILE="${INSTALL_PATH}/db_agent/tools/install.sh"

# функция для получения поддерева со скриптами в папке $1 в ветке $2. Аргумент $3 - учитывать ли время изменения или нет. 
function get_scripts_subtree {
    if [ "$#" -lt 2 ]; then
        printf "scripts subtree: 2 arguments required! given %d\nargs: %s\n" "$#" "$@" >&2
        return -1
    fi

    if [ -n "$3" ]; then 
        printf "%s" "$( cd "$1" && find "$2" -type f -not -wholename '*.svn*' \( -name '*.sh' -o -name '*.php' \) | sed -re 's/\.\///g' )"
    else # то же, но с -anewer
        printf "%s" "$( cd "$1" && find "$2" -type f -anewer "${TIMESTAMP_FILE}" -not -wholename '*.svn*' \( -name '*.sh' -o -name '*.php' \) | sed -re 's/\.\///g' )"
    fi
}

# Функция поглащает 3 параметра: 
# 1- список объектов, которые нужно заменить ссылками
# 2- директория с исходными файлами, на которые будут создаваться ссылки
# 3- директория, в которой будут создаваться символьные ссылки, соответствующие объектам из $1, содержащиеся в поддиректориях $2
function create_links {
    if [ "$#" -ne 3 ]
    then
        printf "3 arguments required! given %d\n" "$#"
        return
    fi
    OBJECTS=$1
    SRC=$2
    DEST=$3

    for obj in $OBJECTS 
    do
        INSTS=$(cd ${DEST} && find ./ -regex ".*\<${obj}" \( -type f -o -type l \) | sed -re 's/\.\///g')
        if [ $(echo $INSTS | wc -w) -ne 1 ]
        then
            printf "There are several or none instances of object %s: %s\nCreate link independently\n" "${obj}" "${INSTS:-<none>}"
            continue
        fi
        #printf "Creating link for %s in %s\n" "${SRC}/${obj}" "${DEST}/${INSTS}" 
        # if file is a link - delete it
        [ -L "${DEST}/${INSTS}"  ] && rm "${DEST}/${INSTS}" 
        # if this is binary file - rename it and create a link
        [ ! -e "${DEST}/${INSTS}" ] || mv -v "${DEST}/${INSTS}" "${DEST}/${INSTS}.OLD" && ln -s "${SRC}/${obj}" "${DEST}/${INSTS}"
    done
}

printf "============= Make links script ===============\nNode: %s\n" "${OWN_IP}"

# где код
#[ -z "$1" ] && DEVEL_PATH="/SQL/wcs/trunk" || DEVEL_PATH="$1"
# DEVEL_PATH as cmd line argument
# (в пути к директории обрезается последний слэш, если он есть)
[ -n "$1" ] && DEVEL_PATH="${1%%/}"
# check path
if [ ! -d "${DEVEL_PATH}" ]
then
    printf "Wrong path: %s\n" "${DEVEL_PATH}"
    exit 1
fi

# Имеющиеся скрипты для total и для db_agent
# Если --force - то не учитывать время доступа к файлу
#[ "$2" == "--force" ] || FORCE="$2" && FORCE=""
FORCE='--force'
TOOLS_SCRIPTS=$(get_scripts_subtree "${DEVEL_PATH}" './tools' "$FORCE" ) 
TOTAL_SCRIPTS=$(get_scripts_subtree "${DEVEL_PATH}/_total" './tools' "$FORCE" ) 
#[ -n "$FORCE" ] && touch -a ${TIMESTAMP_FILE} 

# бинари
EXECUTABLES=$(cd ${DEVEL_PATH} && find ./ -maxdepth 1 -not -name '*.*' -type f -perm -0100 | sed -re 's/\.\///g' )

echo Devel path: $DEVEL_PATH

# ссылки на скрипты tools из db_agent
create_links "$TOOLS_SCRIPTS" "${DEVEL_PATH}" "${INSTALL_PATH}/db_agent"
# ссылки на скрипты tools из total
create_links "$TOTAL_SCRIPTS" "${DEVEL_PATH}/_total" "${INSTALL_PATH}/total"
# ссылки на бинари
create_links "$EXECUTABLES" "$DEVEL_PATH" "$INSTALL_PATH"

printf "Make links done\n"

