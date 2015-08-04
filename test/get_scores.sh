#!/bin/bash

x=0
y=0
rm *.err
rm full.csv

if [ ! -x match_score.py ]
then
	echo "ERROR: match_score.py missing."
	exit 1
fi

for i in $(ls *.pdf)
do
	((x++))	
	./match_score.py $i 2> $i.err && rm $i.err
done

for i in $(ls *.csv | sort -n | cut -f1 -d.)
do
       	((y++))	
	cat $i.csv >> full.csv 
	rm $i*
done

z=$(echo "scale=3; $y/$x" | bc -l)
echo  "$x of $y ($z%) files parsed successfully."
echo "The following files did not parse:"
ls *.err

