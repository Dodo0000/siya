#!/usr/bin/env sh
FILE_NAME=$1
header=$(head -n 1 $FILE_NAME)

echo "$header\n$(sed -n -e '/^$/d' -e '2,$p' $FILE_NAME | sort )"
