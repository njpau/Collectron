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
	git log > ../${arr[3]}_log.txt
	cd $path
	rm -rf $appPath
	#read authors
	while read line
	do
		if [[ $line = "Author: "* ]]; then
			if [[ $(grep "$line" "Developers.txt") ]]; then
				echo "Developer name already saved"
			else
				echo "Writing Developer info to file"
				echo $line >> Developers.txt
			fi
		fi
	done < ${arr[3]}_log.txt

	done < gitlinks.txt
