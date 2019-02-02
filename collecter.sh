#!/bin/bash
echo "=========Start Reading Files=========="
path=$(pwd)
echo "root path: $path"
while read gitLink
do
	cd $path
	arr=(` echo $gitLink | tr '/' ' ' ` )
	appPath="${path}/${arr[3]}"
	echo $appPath
	git clone $gitLink
	cd $appPath
	
