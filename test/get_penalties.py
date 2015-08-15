#!/bin/bash

x=0
y=0

if [ -f full_pen.csv ]
then
	rm full.csv
fi

if [ ! -x match_penalty.py ]
then
	echo "ERROR: match_penalty.py missing."
	exit 1
fi

function get_penalties {
	for i in $(ls *.pdf)
	do
		((x++))	
		echo "processing $i"
		./match_penalty.py $i 2> $i.err && rm $i.err
	done
}

function cat_csv {
	for i in $(ls *penalty.csv | cut -f2 -d_ | sort -u)
	do
		for j in $(ls *_$i*csv | sort -n)
		do
       			((y++))	
			echo "writing $j"
			cat $j >> full_pen.csv 
			echo "removing $j"
			rm $j
		done
	done
}

function report {
	z=$(echo "scale=3; $y/$x" | bc -l)
	echo  "$y of $x ($z%) files parsed successfully."

	if [ $x -ne $y ]
	then
		echo "The following files did not parse:"
		ls *.err
	fi
}

get_penalties
cat_csv
report
rm *.txt
