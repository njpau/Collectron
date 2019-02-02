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
	while read line
	do
		if [[ $line = "Author: "* ]]; then

				echo "Writing Developer info to file"
				echo $line >> Developers.txt
		fi
	done < ${arr[3]}_log.txt

done < gitlinks.txt
