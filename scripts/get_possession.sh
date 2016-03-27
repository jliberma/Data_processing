#!/bin/bash

function get_possession {
	for i in $(ls *.pdf)
	do
		((x++))	
		echo "processing $i"
		#./match_poss.py $i 2> $i.err && rm $i.err
		./match_poss_single.py $i 2> $i.err && rm $i.err
	done
}

function cat_csv {
	echo "Match,Event,T1,T1p,T1t,T2,T2p,T2t" > full_poss.csv
	for i in $(ls *possession.csv | cut -f2 -d_ | sort -u)
	do
		for j in $(ls *_$i*csv | sort -n | grep -v full)
		do
       			((y++))	
			echo "writing $j"
			cat $j >> full_poss.csv 
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

x=0
y=0

if [ -f full_poss.csv ]
then
	rm full_poss.csv
fi

if [ ! -x match_poss.py ]
then
	echo "ERROR: match_poss.py missing."
	exit 1
fi

get_possession
cat_csv
report
rm *.txt
