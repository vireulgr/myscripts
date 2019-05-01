# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias pgsql='psql -U postgres -d sorm_psi -p 9999'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

INSTALL="/etc/install.cfg"
NET_SCRIPTS="/etc/sysconfig/network-scripts"
if [ -f "$INSTALL" ]; then
	ETH=$(cat $INSTALL | grep '\--eth' | cut -d= -f2)
	if [ -z "$ETH" ]; then
		ETH=eth0
	fi
else
	ETH=eth0
fi

if [ -f "$NET_SCRIPTS/ifcfg-$ETH" ]; then
	#OWN_IP=$(cat ${NET_SCRIPTS}/ifcfg-${ETH} | grep 'IPADDR' | cut -d= -f2)
    OWN_IP=$( sed -nre '/IPADDR/ s/^.*"([0-9a-fA-F\:\.]+)".*$/\1/p' "${NET_SCRIPTS}/ifcfg-${ETH}" )
	PS1='[\h-${OWN_IP} \W]\$ '
	export OWN_IP PS1
fi
alias l='ls -alF --color=auto --group-directories-first'
alias p='ps axf'
alias egrep='/bin/egrep --color=auto'
alias grep='/bin/grep --color=auto'
alias vi='vim'
export NLS_LANG=RUSSIAN_RUSSIA.AL32UTF8
export ORACLE_HOME=/usr/lib64/oracle/11.2/client64
PS1='[${OWN_IP} @ $(date +%H%M) \W]# '
EDITOR='vim'
set -o vi
