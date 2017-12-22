#!/bin/bash

SCRIPT_NAME="$0"

print_usage(){
    echo "Usage: $SCRIPT_NAME { --remove \"<ipv4>\"; --add \"<ipv4>/<num_proc>\"; --list \"<ipv4>\"}"
    exit 0
}

declare -a args;

if [ "$#" -lt 1 ]; then
    read -a args;
else
    args=( $1 $2 )
fi

#check_entry_timeout() {

# скрипт filter_ips.awk фильтрует записи списка хостов, у которых таймаут больше period. 
# edit=1 - Выводит список вместе с timestamp: ip/jobs timestamp
# edit=0 - выводит список без timestamp: ip/jobs
# ip - если установлен - удаляет конкретный ip из списка (для параметра remove)
# now - текущее время в секундах с 1.01.1970
# awk -f ~/filter_ips.awk -v now="$(date +%s)" -v period="$(( 60*60*12 ))" -v edit=1 -v ip="" "$0" >> "$0"
# sed -ie '0,/^HOSTS_END$/ { /^HOSTS$/, /^HOSTS_END$/ d; };' "$0"

#}

op=${args[0]}
entry=${args[1]}

# Проверка корректности аргументов
[ -z "$( echo "$entry" | sed -nre '/^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]+)?$/p' )" ] && print_usage

case "$op" in
    --remove) # Удаление IP из списка
#        [ -z "$( echo "$entry" | sed -nre '/^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]+)?$/p' )" ] &&  print_usage

#        check_entry_timeout
        # Удаление
#        sed -ie "/^HOSTS\$/, /^HOSTS_END\$/ { /${entry%%/*}/d }" "$SCRIPT_NAME" 
#        awk -f ~/filter_ips.awk -v now="$(date +%s)" -v period="$(( 60*60*12 ))" -v edit=0  -v ip="$entry" "$0" >> "$0"
#        sed -ie '0,/^HOSTS_END$/ { /^HOSTS$/, /^HOSTS_END$/ d; };' "$0"

    ;;
    --add) # Добавление записи в список
        # Проверка корректности аргументов
        [ -z "$( echo "$entry" | sed -nre '/^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]+)?$/p' )" ] && print_usage

#        check_entry_timeout
#        awk -f ~/filter_ips.awk -v now="$(date +%s)" -v period="$(( 60*60*12 ))" -v edit=0  -v ip="" "$0" >> "$0"
#        sed -ie '0,/^HOSTS_END$/ { /^HOSTS$/, /^HOSTS_END$/ d; };' "$0"

        #sed -ie                          "s/\(192.168.238.103\(\/[0-9]\+\)\?\)\s\+[0-9]\+/\1    42/ " inplace.txt
        #sed -ie "/^HOSTS\$/, /^HOSTS_END\$/ { s/(${entry%%/*}[0-9\/]*)\s*[0-9]+/\1    ${NOW}/ p; }" "$SCRIPT_NAME"
        #sed -ire "/^HOSTS\$/, /^HOSTS_END\$/ { s/(${entry%%/*}(\/[0-9]+)?)[:[blank]:]*[0-9]+/\1    ${NOW}/g; }" "$SCRIPT_NAME"
        echo "$entry, ${entry%%/*}, $PERIOD, now: $NOW"

        # Не дублируется ли хост
        if [ -z "$( sed -ne "/^HOSTS\$/, /^HOSTS_END\$/ { /${entry%%/*}/p }" "$SCRIPT_NAME" )" ]; then
            entry+="   $(date +%s)"
            # Добавление (Здесь Табы не заменятЬ! иначе работать не будет)
            ed -s "$SCRIPT_NAME" <<-HEREDOC
				/^HOSTS$/a
				$entry
				.
				wq
			HEREDOC
        fi
    ;;

    --list) # Вывод списка хостов
        # awk -f ~/filter_ips.awk -v now="$(date +%s)" -v period="$(( 60*60*12 ))" -v edit=0  -v ip="" "$0" >> "$0"
# sed -ie '0,/^HOSTS_END$/ { /^HOSTS$/, /^HOSTS_END$/ d; };' "$0"
# sed -ne '/^HOSTS$/, /^$/ { /^HOSTS$/n; /^$/n; p }' "$SCRIPT_NAME"
#sed -nre "/^HOSTS$/, /^HOSTS_END$/ { s/(192.168.238.110(\/[0-9]+)?)\s*[0-9]+/\1    ${NOW}/ p; }" /SQL/wcs/trunk/dev_tools/store_distcc_hosts.sh
# WARNING! Удаление всех хостов!

#NOW=$( date +%s ) 
#PERIOD=$(( 60*60*12 )) # 12 часов
#
# для обновления timestamp конкретного узла
#sed -ie "/^HOSTS\$/, /^HOSTS_END\$/ { s/(${entry%%/*}(\/[0-9]+)?)\s*[0-9]+/\1    ${NOW}/ p; }" "$SCRIPT_NAME"
#
#LINES=$( sed -ne '/^HOSTS$/, /^HOSTS_END$/ { /^HOSTS$/n; /^HOSTS_END$/n; p; }' "$SCRIPT_NAME" )
#declare -a line;
#while read -a line; do
# Если последнее обновление происходило не больше, чем PERIOD времени назад,
# то узел считаем активным и передаём хосту в качестве сервера distcc
#   [ "$(( NOW - line[1] ))" -le "$PERIOD" ] && echo "${line[0]}"
#done <<< "${HOSTS}"

    ;;

    *) print_usage
    ;;
esac

exit 0

# host IP/jobs      update time

HOSTS
192.168.238.123/5  1425389878
192.168.238.119/6   1424948832
192.168.238.172/6   1424948832
192.168.238.110/6   1424948832
192.168.238.77/4    1424948832
192.168.238.103/3   1424948832
HOSTS_END

