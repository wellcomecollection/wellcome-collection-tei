#!/bin/bash
# count inodes for each directory
LIST=`ls`
for i in $LIST; do
echo $i
find $i -printf "%i\n" | sort -u | wc -l
done
