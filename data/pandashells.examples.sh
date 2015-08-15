#! /usr/bin/env bash

cat full_pen.csv | p.df 'df[df.Match==1]' 'df[df.Event=="Wellington"]' -o table
cat full_pen.csv | p.df 'df.groupby(by="Ref").Description.count()' -o table header index 
cat full_pen.csv | p.df 'df[df.Description.str.contains("defence")]' -o table 
cat full_pen.csv | p.df 'df[df.Event=="Wellington"]' 'df[df.Description.str.contains("defence")]' -o table 
# plot penalties per event
# plot penalties by ref
# plot attack vs defense penalties by ref
