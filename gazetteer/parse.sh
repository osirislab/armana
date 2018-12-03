#!/usr/bin/env sh

# Must run in the current directory

for i in *; do 
	filename=$(basename -- "$i")
	extension="${filename##*.}"
	filename="${filename%.*}"
	cat $i | sed 's/^ *//;s/ *$//' | sed 's/\t/,/g' > $filename.csv
done
