# Data processing

Scripts to extract interesting data from IRB PDF match reports
and save it to CSV.

* [match_penalty.py](scripts/match_penalty.py) converts IRB penalty match report PDFs to csv format
* [match_score.py](scripts/match_score.py) converts IRB scoring match report PDFs to csv format
* [match_poss.py](scripts/match_poss.py) converts IRB time of possession match report PDFs to csv format
* [get_scores.sh](scripts/get_score.sh) executes match_score.py and concatenates results
* [get_penalties.sh](scripts/get_penalties.sh) executes match_penalty.py and concatenates results
* [get_possession.sh](scripts/get_possession.sh) executes match_poss.py and concatenates results
* [pandashells.examples.sh](data/pandashells.examples.sh) examples of data manipulation with [pandashells](https://github.com/robdmc/pandashells)

Results from 2014-2015 World Sevens Series:

* [full_score.csv](data/full_score.csv)
* [full_pen.csv](data/full_pen.csv)
