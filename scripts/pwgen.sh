#!/usr/bin/env sh

passwd=''

for i in `seq 1 6`; do
	passwd=$passwd`pwgen -s`
done

echo $passwd
