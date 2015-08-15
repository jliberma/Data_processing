#!/bin/bash

x=0
y=0

if [ -x full_score.csv ]
then
	rm full_score.csv
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
		echo "processing $i"
		./match_score.py $i 2> $i.err && rm $i.err
	done
}

function cat_csv {
	echo "Match,Event,Half,Time,Team,Description" > full_score.csv
	for i in $(ls *.csv | cut -f2 -d_ | sort -u | grep -v full)
	do
		for j in $(ls *_$i | sort -n | grep -v full)
		do
       			((y++))	
			echo "writing $j"
			cat $j >> full_score.csv 
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

get_scores
cat_csv
report
#rm *.txt
