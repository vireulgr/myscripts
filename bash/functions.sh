#!/bin/bash

## ======================
G_LOG_FILE='/root/fncs.log'

G_RPMS_DIR='/SQL/distr/rpms'

function err_exit
{
    printf "ERROR MSG (%d sec; pid: %d) %s\n" "$SECONDS" "$$" "$1"
    exit 1
}

function print_time_nice
{
    if [ -z "$1" ]
    then 
        printf "argument required!\n" 
    else
        SECNDS=${1:-0}

        MINTS=$((SECNDS/60))
        SECNDS=$(( SECNDS - MINTS * 60 ))

        [ "$MINTS" -ne 0 ] && printf " %d minutes," "$MINTS"

        printf " %d seconds" "$SECNDS"
    fi
}

function print_spd_nice
{
    if [ -z "$1" ]
    then
        printf "argument required!\n"
    else
        BITS=${1:-0}

        MEGS=$(( BITS >> 20 ))
        KILOS=$(( ( BITS - (MEGS << 20 ) ) >> 10 ))
        BITS=$(( BITS - ( (MEGS << 20) + (KILOS << 10) ) ))

        [ "$MEGS" -ne 0 ] && printf " %d Mb," "$MEGS"
        [ "$KILOS" -ne 0 ] &&  printf " %d kb," "$KILOS"

        printf " %d bits per second" "$BITS"
    fi
}

function do_services
{
    # $1 - nodes list
    # $2 - services list
    # $# - action: start/stop/restart
    NODES="$1"
    SERVICES="$2"
    ACTION="$3"
    for remote_ip in $NODES; do
        [ "$remote_ip" == "$LOCAL_IP" ] && continue
        CMD_STRING=""
        for service in $SERVICES; do
            CMD_STRING+="service $service $ACTION  >/dev/null; "
        done
        #ssh "root@${remote_ip}" 'service db_agent stop; service xinetd stop; service pgpool stop;' >/dev/null
        #echo -e "node: $remote_ip\ncommand string: $CMD_STRING"
        ssh "root@${remote_ip}" "$CMD_STRING"

        sleep 2
    done
}

function install_rpm
{
    # $1 - rpm name
    # $2 - nodes ips
    RPM="$1"
    REMOTE_IPS="$2"
    STATUS='0'
    if [ -z "$RPM" ]; then
        #echo "Warning! can't find stats_collector rpm;"
        STATUS='1'
    else
        rpm -ihv "$RPM" >$G_LOG_FILE
        if [ $? -ne '0' ]; then
            #echo "Warning! can't install stats_collector rpm"
            STATUS='2'
        fi
        for remote_ip in $REMOTE_IPS; do
            ssh "root@${remote_ip}" "mkdir -p $G_RPMS_DIR " >$G_LOG_FILE
            scp "$RPM" "${remote_ip}:$G_RPMS_DIR" >$G_LOG_FILE
            ssh "root@${remote_ip}" "cd $G_RPMS_DIR && rpm -ihv ${RPM##*/}" >$G_LOG_FILE
        done
    fi
    return $STATUS
}
