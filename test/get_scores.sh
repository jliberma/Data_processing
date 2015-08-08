#!/bin/bash

set -x

x=0
y=0

if [ -x full.csv ]
then
	rm full.csv
fi

if [ ! -x match_score.py ]
then
	echo "ERROR: match_score.py missing."
	exit 1
fi

function get_scores {
	for i in $(ls *.pdf)
	do
		((x++))	
		./match_score.py $i 2> $i.err && rm $i.err
	done
}

function cat_csv {
	for i in $(ls *.csv | grep -v full.csv | sort -n | cut -f1 -d.)
	do
       		((y++))	
		cat $i.csv >> full.csv 
		rm $i*
	done
}

function report {
	z=$(echo "scale=3; $y/$x" | bc -l)
	echo  "$x of $y ($z%) files parsed successfully."

	if [ $x -ne $y ]
	then
		echo "The following files did not parse:"
		ls *.err
	fi
}

get_scores
cat_csv
report

