#!/bin/sh
etc=/opt/Intel/Intel\(R\)\ Firmware\ Engine/etc/ToolsetInventory.pdo

if [ ! -f "$etc" ]
then
	echo Path:["$etc"] is an invalid path, please check.
	exit 1
fi

ToolPath=`cat "$etc" | grep "Path" | cut -d '=' -f 2`
ToolPath=`expr substr "$ToolPath" 2 ${#ToolPath}`

export PATH="$PATH":"$ToolPath"
. ~/.bash_profile

sudo python Main.py