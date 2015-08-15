#! /usr/bin/env bash

# select rows from match 1 in Wellington
cat full_pen.csv | p.df 'df[df.Match==1]' 'df[df.Event=="Wellington"]' -o table
# count penalties by each ref
cat full_pen.csv | p.df 'df.groupby(by="Ref").Description.count()' -o table header index 
# only defensive penalties
cat full_pen.csv | p.df 'df[df.Description.str.contains("defence")]' -o table 
# defensive penalties from Wellington
cat full_pen.csv | p.df 'df[df.Event=="Wellington"]' 'df[df.Description.str.contains("defence")]' -o table 
# plot penalties per event
# plot penalties by ref
# plot attack vs defense penalties by ref
