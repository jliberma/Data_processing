#! /usr/bin/env bash

# select rows from match 1 in Wellington
cat ../data/full_pen.csv | p.df 'df[df.Match==1]' 'df[df.Event=="Wellington"]' -o table
# only defensive penalties
cat ../data/full_pen.csv | p.df 'df[df.Description.str.contains("defence")]' -o table 
# defensive penalties from Wellington
cat ../data/full_pen.csv | p.df 'df[df.Event=="Wellington"]' 'df[df.Description.str.contains("defence")]' -o table 

# event penalty statistics
cat ../data/full_pen.csv | p.df 'df.groupby(by="Event").Description.count().describe().T' -o table header index
# plot penalties per event
## how to put events in order (rather than alphabetical)
cat ../data/full_pen.csv | p.df 'df.groupby(by="Event").Description.count().plot()' -o table header index

# count penalties by each ref
cat ../data/full_pen.csv | p.df 'df.groupby(by="Ref").Description.count()' -o table header index 
# plot penalties by ref
cat ../data/full_pen.csv | p.df 'df.groupby(by="Ref").Description.count().plot()' -o table header index 
# plot attack vs defense penalties by ref

# ratio of adv to adv brought back
# move to scripts dir

# Attacking vs Defensive penalties by team
## Any way to save output from one command to a reusable variable?
#cat ../data/full_pen.csv | p.df 'df[df.Description.str.contains("defence")]' 'df.groupby(by="Team").Description.count()' -o index table header
#cat ../data/full_pen.csv | p.df 'df[df.Description.str.contains("attack")]' 'df.groupby(by="Team").Description.count()' -o index table header

# test combining these with regex
#p.merge <(cat ../data/full_pen.csv | p.df 'df[df.Description.str.contains("attack")]' 'df.groupby(by="Team").Description.count()' -o index) <(cat ../data/full_pen.csv | p.df 'df[df.Description.str.contains("defence")]' 'df.groupby(by="Team").Description.count()' -o index) --how left --on Team | p.df -o table 

#p.merge <(cat ../data/full_pen.csv | p.df 'df[df.Description.str.contains("attack")]' 'df.groupby(by="Team").Description.count()' -o index) <(cat ../data/full_pen.csv | p.df 'df[df.Description.str.contains("defence")]' 'df.groupby(by="Team").Description.count()' -o index) --how left --on Team | p.plot -x Description_x -y Description_y -s o --xlabel "Attack" --ylabel "Defence" --title "Penalties by team" --savefig ../images/penalties.png
# ratio of attacking penalties vs defensive penalties per match
## related to time of possession?

# count number of unique matches per team
# save as variable
# divide everything by that
